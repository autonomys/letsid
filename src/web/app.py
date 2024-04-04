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
import jwt

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

# JWT token creation with user ID and expiration
def create_jwt_token(user_id, secret_key):
    expiration_time = timedelta(minutes=5)
    payload = {
        'exp': datetime.utcnow() + expiration_time,
        'iat': datetime.utcnow(),
        'sub': str(user_id),
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

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
        token = create_jwt_token(user_info['id'], app.secret_key)

        key_pair = auto_identity.generate_ed25519_key_pair()
        ed25519_private_key, ed25519_public_key = key_pair
        
        print('ed25519_private_key', ed25519_private_key)
        
        private_hex = auto_identity.key_to_hex(ed25519_private_key)
        
        print('private_hex', private_hex)
       
        
        concatenated_uuid = provider + user_info['id']
        hashed_uuid = hashlib.sha3_256(concatenated_uuid.encode()).hexdigest()
        
        certificate = self_issue_certificate(hashed_uuid, ed25519_private_key)
        
        serial_number = certificate.serial_number

        registration_data = {
            'hashed_uuid': hashed_uuid,
            'public_key_hex': ed25519_public_key,
            'private_key_hex': ed25519_private_key,
            'auto_id': serial_number,
            'user_info': user_info
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
        user_private_key_hex = request.form.get('user_private_key')
        print('user_private_key_hex', user_private_key_hex)
        user_identifier = request.form.get('user_identifier')
        print('user_identifier', user_identifier)
        
        key_pair = auto_identity.generate_ed25519_key_pair()
        ed25519_private_key, ed25519_public_key = key_pair
        
        print('test', ed25519_private_key.hex())
        
        parent_certificate = auto_identity.self_issue_certificate(user_identifier, ed25519_private_key)
        certificate = auto_identity.issue_certificate(parent_certificate, ed25519_private_key)
        
        # if issue_identity("x509_placeholder", user_identifier):
        #     flash('Identity issued successfully.')
        #     return redirect(url_for('index'))
        # else:
        #     flash('Failed to issue identity. Please try again.')

    return render_template('issue_identity.html')