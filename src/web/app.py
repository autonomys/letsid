# src/web/app.py
import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, flash
from config import DevelopmentConfig, ProductionConfig
from flask_dance.contrib.google import google
from flask_dance.contrib.github import github
from flask_dance.contrib.discord import discord
import jwt
from bip39 import bip39
import sr25519
from datetime import datetime, timedelta
from src.core.utils import generate_key_pair_and_csr
from src.core.registration import register_user_with_letsid
from src.core.issuance import issue_identity
from src.web.api import api
from src.web.authorize import authorize_bp

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure app based on environment
config_class = ProductionConfig if os.getenv('FLASK_ENV') == 'production' else DevelopmentConfig
app.config.from_object(config_class)

# Register blueprints
app.register_blueprint(api, url_prefix='/api')
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
    return render_template('index.html')

@app.route('/autoID/<user_auto_id>')
def show_auto_id(user_auto_id):
    # Here you can add any processing you need with user_auto_id
    # For now, we just pass it to the template
    return render_template('show_auto_id.html', auto_id=user_auto_id)

# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        oidc_token = request.form.get('oidc_token')  # Improved form data extraction
        public_key_hex, private_key_hex, seed_hex, csr = generate_key_pair_and_csr()
        digital_signature = "signature_placeholder"  # Placeholder for signature
        
        if register_user_with_letsid(csr, digital_signature, oidc_token):
            flash('Registration successful.')
            return redirect(url_for('index'))
        else:
            flash('Registration failed. Please try again.')

    return render_template('authorize.html')

# Simplified OAuth registration finalization
def finalize_registration(provider, user_info_endpoint):
    provider_auth = globals().get(provider)
    if not provider_auth or not provider_auth.authorized:
        return redirect(url_for('authorize.authorize', provider_name=provider))
    response = provider_auth.get(user_info_endpoint)
    if response.ok:
        user_info = response.json()
        token = create_jwt_token(user_info['id'], app.secret_key)
        
        # Generate a random BIP39 mnemonic seed
        mnemonic = bip39.encode_bytes(os.urandom(16))
        seed_bytes = bip39.phrase_to_seed(mnemonic)
        sr25519_seed = seed_bytes[:32]
        
        # Derive public and private keys from the mnemonic
        keypair = sr25519.pair_from_seed(sr25519_seed)
        
        seed_hex = seed_bytes.hex()
        public_key_hex = keypair[0].hex()
        private_key_hex = keypair[1].hex()
        
        # Generate a random Auto ID - you could use a UUID for this purpose
        auto_id = os.urandom(16).hex()

        # Packaging the OIDC token and mock values into a dictionary to pass to the template
        registration_data = {
            'oidc_token': token,  # Assuming this is the token to be passed as a hidden input
            'public_key_hex': public_key_hex,
            'private_key_hex': private_key_hex,
            'seed_hex': seed_hex,
            'auto_id': auto_id,
            'user_info': user_info  # Include user_info if needed in the template for display or further processing
        }

        return render_template('register.html', **registration_data)
    else:
        flash(f"Failed to fetch user details from {provider.capitalize()}.")
        return redirect(url_for('authorize.authorize', provider_name=provider))

# Provider-specific routes for finalizing registration
@app.route('/finalize-registration/google')
def finalize_registration_google():
    return finalize_registration('google', "/oauth2/v2/userinfo")

@app.route('/finalize-registration/github')
def finalize_registration_github():
    return finalize_registration('github', "/user")

@app.route('/finalize-registration/discord')
def finalize_registration_discord():
    return finalize_registration('discord', "/api/users/@me")

# Route for identity issuance
@app.route('/issue-identity', methods=['GET', 'POST'])
def issue_identity_route():
    if request.method == 'POST':
        user_private_key_hex = request.form.get('user_private_key')
        user_identifier = request.form.get('user_identifier')
        csr = "csr_placeholder"  # Placeholder for CSR
        
        if issue_identity("x509_placeholder", user_identifier):
            flash('Identity issued successfully.')
            return redirect(url_for('index'))
        else:
            flash('Failed to issue identity. Please try again.')

    return render_template('issue_identity.html')