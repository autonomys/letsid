# src/web/app.py
import os
from datetime import datetime, timedelta
import hashlib
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, flash
from config import DevelopmentConfig, ProductionConfig
from flask_dance.contrib.google import google
from flask_dance.contrib.github import github
from flask_dance.contrib.discord import discord
from src.web.authorize import authorize_bp
import auto_identity
        
# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure app based on environment
config_class = ProductionConfig if os.getenv('FLASK_ENV') == 'production' else DevelopmentConfig
app.config.from_object(config_class)

# Register blueprints
app.register_blueprint(authorize_bp, url_prefix='/authorize')

# Secure secret key setup
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))

# Main route
@app.route('/')
def index():
    """Render the index template."""
    return render_template('index.html')

@app.route('/autoID/<user_auto_id>')
def show_auto_id(user_auto_id):
    """Render the template to show auto ID."""
    return render_template('show_auto_id.html', auto_id=user_auto_id)

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Render the authorize template."""
    return render_template('authorize.html')

# Simplified OAuth registration finalization
def finalize_registration(provider, user_info_endpoint):
    """Finalize OAuth registration."""
    provider_auth = globals().get(provider)
    if not provider_auth or not provider_auth.authorized:
        return redirect(url_for('authorize.authorize', provider_name=provider))
    response = provider_auth.get(user_info_endpoint)
    if response.ok:
        user_info = response.json()

        key_pair = auto_identity.generate_ed25519_key_pair()
        ed25519_private_key, ed25519_public_key = key_pair
        
        user_keyring = auto_identity.key_to_pem(ed25519_private_key).decode()
        
        concatenated_uuid = provider + user_info['id']
        user_identifier = hashlib.sha3_256(concatenated_uuid.encode()).hexdigest()
        
        certificate = auto_identity.self_issue_certificate(user_identifier, ed25519_private_key)
        
        auto_id = certificate.serial_number

        registration_data = {
            'auto_id': auto_id,
            'user_identifier': user_identifier,
            'user_keyring': user_keyring,
        }

        return render_template('show_auto_id.html', **registration_data)
    else:
        flash(f"Failed to fetch user details from {provider.capitalize()}.")
        return redirect(url_for('authorize.authorize', provider_name=provider))

# Provider-specific routes for finalizing registration
@app.route('/finalize-registration/google')
def finalize_registration_google():
    """Finalize registration with Google OAuth."""
    return finalize_registration('google', "/oauth2/v2/userinfo")

@app.route('/finalize-registration/github')
def finalize_registration_github():
    """Finalize registration with GitHub OAuth."""
    return finalize_registration('github', "/user")

@app.route('/finalize-registration/discord')
def finalize_registration_discord():
    """Finalize registration with Discord OAuth."""
    return finalize_registration('discord', "/api/users/@me")

# Route for identity issuance
@app.route('/issue-identity', methods=['GET', 'POST'])
def issue_identity_route():
    """Route for issuing identity."""
    if request.method == 'POST':
        user_identifier = request.form.get('user_identifier')
        print('user_identifier', user_identifier)
        user_keyring = request.form.get('user_keyring')
        print('user_keyring', user_keyring)
        user_keyring = user_keyring.encode()
        print('user_keyring', user_keyring)
        
        private_key = auto_identity.pem_to_private_key(user_keyring)
        print('private_key', private_key)
        
        csr = auto_identity.create_csr(user_identifier, private_key)
        
        certificate = auto_identity.issue_certificate(csr, private_key)
        print('certificate', certificate)
        
        auto_id = certificate.serial_number

        certificate_data = {
            'auto_id': auto_id,
            'user_identifier': user_identifier,
            'user_keyring': user_keyring,
        }
        return render_template('show_auto_id.html', **certificate_data)
    return render_template('issue_identity.html')