# src/web/authorize.py
import os
from flask import Blueprint, flash, redirect, url_for, session
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.contrib.discord import make_discord_blueprint
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create blueprints for OAuth providers
google_bp = make_google_blueprint(
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    scope=["profile", "email"],
    redirect_to="finalize_registration_google"
)

github_bp = make_github_blueprint(
    client_id=os.environ.get("GITHUB_CLIENT_ID"),
    client_secret=os.environ.get("GITHUB_CLIENT_SECRET"),
    scope="user",
    redirect_to="finalize_registration_github"
)

discord_bp = make_discord_blueprint(
    client_id=os.environ.get("DISCORD_CLIENT_ID"),
    client_secret=os.environ.get("DISCORD_CLIENT_SECRET"),
    scope=["identify", "email"],
    redirect_to="finalize_registration_discord"
)

# Define the blueprint for authorization routes
authorize_bp = Blueprint('authorize', __name__)

# Register OAuth blueprints with the authorize blueprint
authorize_bp.register_blueprint(google_bp, url_prefix="/google")
authorize_bp.register_blueprint(github_bp, url_prefix="/github")
authorize_bp.register_blueprint(discord_bp, url_prefix="/discord")

# Route to initiate OAuth login for different providers
@authorize_bp.route('/<provider_name>')
def authorize(provider_name):
    session['oauth_provider'] = provider_name
    if provider_name == 'google':
        return redirect(url_for('authorize.google.login'))
    elif provider_name == 'github':
        return redirect(url_for('authorize.github.login'))
    elif provider_name == 'discord':
        return redirect(url_for('authorize.discord.login'))
    else:
        flash("Invalid provider name.")
        return redirect(url_for('register'))

# Define the callback route for Discord OAuth
@discord_bp.route('/callback')
def discord_callback():
    if not discord_bp.authorized:
        flash('Failed to authorize with Discord.', 'error')
        return redirect(url_for('index'))
    
    resp = discord_bp.get('/api/users/@me')
    if resp.ok:
        user_data = resp.json()
        session['discord_user'] = user_data
        return redirect(url_for('authenticated_route'))
    else:
        flash('Failed to fetch user data from Discord API.', 'error')
        return redirect(url_for('index'))