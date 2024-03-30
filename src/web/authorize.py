# src/web/authorize.py
import os
from flask import Blueprint, flash, redirect, url_for, session
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.contrib.discord import make_discord_blueprint
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Dictionary mapping provider names to their corresponding Flask-Dance blueprint factories
oauth_providers = {
    "google": make_google_blueprint(
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        scope=["profile", "email"],
        redirect_to="finalize_registration_google"
    ),
    "github": make_github_blueprint(
        client_id=os.getenv("GITHUB_CLIENT_ID"),
        client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
        scope="user",
        redirect_to="finalize_registration_github"
    ),
    "discord": make_discord_blueprint(
        client_id=os.getenv("DISCORD_CLIENT_ID"),
        client_secret=os.getenv("DISCORD_CLIENT_SECRET"),
        scope=["identify", "email"],
        redirect_to="finalize_registration_discord"
    )
}

# Create a unified authorization blueprint
authorize_bp = Blueprint('authorize', __name__)

# Dynamically register OAuth blueprints based on the defined providers
for provider, bp in oauth_providers.items():
    authorize_bp.register_blueprint(bp, url_prefix=f"/{provider}")

# Generalized route to initiate OAuth login
@authorize_bp.route('/<provider_name>')
def authorize(provider_name):
    provider_bp = oauth_providers.get(provider_name)
    if provider_bp:
        session['oauth_provider'] = provider_name
        return redirect(url_for(f'authorize.{provider_name}.login'))
    else:
        flash("Invalid provider name.", 'error')
        return redirect(url_for('index'))

# Discord-specific callback handling
@oauth_providers['discord'].route('/callback')
def discord_callback():
    if not oauth_providers['discord'].authorized:
        flash('Failed to authorize with Discord.', 'error')
        return redirect(url_for('index'))

    resp = oauth_providers['discord'].get('/api/users/@me')
    if resp.ok:
        session['discord_user'] = resp.json()
        return redirect(url_for('authenticated_route'))
    else:
        flash('Failed to fetch user data from Discord API.', 'error')
        return redirect(url_for('index'))
