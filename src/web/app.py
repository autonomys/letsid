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
from auto_identity import CertificateManager, generate_ed25519_key_pair, key_to_pem, pem_to_private_key
        
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

# Route for self registration
def finalize_registration(provider, user_info_endpoint):
    """Finalize OAuth registration."""
    try:
        provider_auth = globals().get(provider)
        if not provider_auth or not provider_auth.authorized:
            return redirect(url_for('authorize.authorize', provider_name=provider))
        
        response = provider_auth.get(user_info_endpoint)
        if response.ok:
            user_info = response.json()

            key_pair = generate_ed25519_key_pair()
            ed25519_private_key, _ = key_pair
            
            user_keyring = key_to_pem(ed25519_private_key).decode()
            
            concatenated_uuid = os.getenv('LETSID_SERVER_AUTO_ID') + provider + user_info['id']
            auto_id = hashlib.sha3_256(concatenated_uuid.encode()).hexdigest()
            
            certificate = CertificateManager(None, ed25519_private_key).self_issue_certificate(auto_id)

            registration_data = {
                'auto_id': auto_id,
                'user_keyring': user_keyring,
                'certificate': CertificateManager.certificate_to_pem(certificate).decode(),
            }

            return render_template('show_auto_id.html', **registration_data)
        else:
            flash(f"Failed to fetch user details from {provider.capitalize()}.")
            return redirect(url_for('authorize.authorize', provider_name=provider))
            
    except Exception as e:
        # Log the error for debugging purposes
        print(f"An error occurred during registration finalization: {e}")
        
        # Optionally, flash a message to the user
        flash("An unexpected error occurred. Please try again later.")

        # Render the error template with the error message
        return render_template('error.html', error_message=str(e))

# Route for identity issuance
@app.route('/issue-identity', methods=['GET', 'POST'])
def issue_identity_route():
    """Route for issuing identity."""
    try:
        if request.method == 'POST':
            auto_id = hashlib.sha3_256((request.form.get('user_identifier') + os.urandom(32).hex()).encode()).hexdigest()
            certificate = CertificateManager.pem_to_certificate(request.form.get('user_certificate').encode())
            print('certificate', certificate)

            user_keyring = request.form.get('user_keyring').encode()
            print('user_keyring', user_keyring)
            private_key = pem_to_private_key(user_keyring)

            print('private_key', private_key)

            certificate = CertificateManager(certificate, private_key)
            csr = certificate.create_csr(auto_id)
            certificate = certificate.issue_certificate(csr)

            certificate_data = {
                'auto_id': auto_id,
                'user_keyring': user_keyring.decode(),
                'certificate': CertificateManager.certificate_to_pem(certificate).decode(),
            }
            return render_template('show_auto_id.html', **certificate_data)
        
        # If it's not a POST request, just show the identity issue form
        return render_template('issue_identity.html')

    except Exception as e:
        # Log the error for debugging purposes
        print(f"An error occurred: {e}")

        # Render the error template with the error message
        return render_template('error.html', error_message=str(e))

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