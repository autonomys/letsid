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
    redirect_to="authorize.google.authorized"
)

github_bp = make_github_blueprint(
    client_id=os.environ.get("GITHUB_CLIENT_ID"),
    client_secret=os.environ.get("GITHUB_CLIENT_SECRET"),
    scope="user",
    redirect_to="authorize.github.authorized"
)

discord_bp = make_discord_blueprint(
    client_id=os.environ.get("DISCORD_CLIENT_ID"),
    client_secret=os.environ.get("DISCORD_CLIENT_SECRET"),
    scope=["identify", "email"],
    redirect_to="authorize.discord.authorized"
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
    # Upon successful authentication, the user will be redirected back to this route
    if not discord_bp.authorized:
        # If the authorization failed, flash a message and redirect to the index page
        flash('Failed to authorize with Discord.', 'error')
        return redirect(url_for('index'))
    
    # Get the OAuth token from the Discord OAuth response
    resp = discord_bp.get('/api/users/@me')
    if resp.ok:
        # If the request to Discord API is successful, get user data
        user_data = resp.json()
        
        # Do something with user data, like store it in the session
        session['discord_user'] = user_data
        
        # Redirect to a page where you want to handle authenticated users
        return redirect(url_for('authenticated_route'))
    else:
        # If the request to Discord API fails, flash an error message and redirect to index
        flash('Failed to fetch user data from Discord API.', 'error')
        return redirect(url_for('index'))
