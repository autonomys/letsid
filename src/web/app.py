import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, flash, session
from config import DevelopmentConfig, ProductionConfig
from flask_dance.contrib.google import google
from flask_dance.contrib.github import github
from flask_dance.contrib.discord import discord
import jwt
import datetime
from src.core.utils import generate_key_pair_and_csr
from src.core.registration import register_user_with_letsid
from src.core.issuance import issue_identity
from src.web.api import api
from src.web.authorize import authorize_bp
from src.web.oauth_routes import oauth_bp

load_dotenv()

app = Flask(__name__)

env = os.environ.get('FLASK_ENV', 'development')
if env == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)
    
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(authorize_bp, url_prefix='/authorize')
app.register_blueprint(oauth_bp)

app.secret_key = os.environ.get('SECRET_KEY', 'default_fallback_secret_key')  # Change this to a random secret key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Extract form data
        oidc_token = request.form['oidc_token']  # Placeholder for actual OIDC token handling
        
        # Generate key pair and CSR
        public_key_hex, private_key_hex, seed_hex, csr = generate_key_pair_and_csr()
        
        # Placeholder for actual signature generation
        digital_signature = "digital_signature_placeholder"
        
        # Register user with LetsID server
        registration_result = register_user_with_letsid(csr, digital_signature, oidc_token)
        
        if registration_result:
            flash('Registration successful.')
            return redirect(url_for('index'))
        else:
            flash('Registration failed. Please try again.')
    
    # Render the registration form template
    return render_template('register.html')

@app.route('/finalize-registration/google')
def finalize_registration_google():
    # This route handles the finalization for Google OAuth
    if not google.authorized:
        return redirect(url_for('authorize.authorize', provider_name='google'))
    resp = google.get("/oauth2/v2/userinfo")
    if resp.ok:
        user_info = resp.json()
        # Log the user info for debugging purposes
        print(user_info)
        
        # Payload for JWT with an expiration time of 5 minutes
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            'iat': datetime.datetime.utcnow(),
            'sub': str(user_info['id']),  # Subject is the user's ID
        }
        # Encode the payload to create the JWT token
        token = jwt.encode(payload, app.secret_key, algorithm='HS256')
        flash(f"Google: Logged in as: {user_info['name']} (Email: {user_info['email']})")
    else:
        flash("Failed to fetch user details from Google.")
    # Implement any specific logic for Google OAuth finalization here
    return render_template('finalize_registration.html', oidc_token="Your Google OIDC Token Here")

@app.route('/finalize-registration/github')
def finalize_registration_github():
    # Similar implementation for GitHub
    if not github.authorized:
        return redirect(url_for('authorize.authorize', provider_name='github'))
    resp = github.get("/user")
    if resp.ok:
        user_info = resp.json()
        # Log the user info for debugging purposes
        print(user_info)
        
        # Payload for JWT with an expiration time of 5 minutes
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            'iat': datetime.datetime.utcnow(),
            'sub': str(user_info['id']),  # Subject is the user's ID
        }
        # Encode the payload to create the JWT token
        token = jwt.encode(payload, app.secret_key, algorithm='HS256')
        flash(f"GitHub: Logged in as: {user_info['login']} (ID: {user_info['id']})")
    else:
        flash("Failed to fetch user details from GitHub.")
    return render_template('finalize_registration.html', oidc_token="Your GitHub OIDC Token Here")

@app.route('/finalize-registration/discord')
def finalize_registration_discord():
    # And for Discord
    if not discord.authorized:
        return redirect(url_for('authorize.authorize', provider_name='discord'))
    resp = discord.get("/api/users/@me")
    if resp.ok:
        user_info = resp.json()
        # Log the user info for debugging purposes
        print(user_info)
        
        # Payload for JWT with an expiration time of 5 minutes
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
            'iat': datetime.datetime.utcnow(),
            'sub': str(user_info['id']),  # Subject is the user's ID
        }
        # Encode the payload to create the JWT token
        token = jwt.encode(payload, app.secret_key, algorithm='HS256')
        # wrap both the user info and the token in a object
        oidc_token = {
            'user_info': user_info,
            'jwt_token': token
        }
        # Provide feedback to the user and return the JWT token
        flash(f"Discord: Logged in as: {user_info['username']}# {user_info['discriminator']} (ID: {user_info['id']})")
        return render_template('finalize_registration.html', oidc_token=oidc_token)
    else:
        flash("Failed to fetch user details from Discord.")
        return redirect(url_for('authorize.authorize', provider_name='discord'))

@app.route('/finalize-registration')
def finalize_registration():
    provider_name = session.get('oauth_provider')
    print(provider_name)
    user_info = None
    
    # Handling Google OAuth
    if provider_name == 'google':
        if not google.authorized:
            return redirect(url_for('authorize.authorize', provider_name='google'))
        
        resp = google.get("/oauth2/v2/userinfo")
        if resp.ok:
            user_info = resp.json()
            print(user_info)  # Console log the user info
            flash(f"Google: Logged in as: {user_info['name']} (Email: {user_info['email']})")
        else:
            flash("Failed to fetch user details from Google.")

    # Handling GitHub OAuth
    elif provider_name == 'github':
        if not github.authorized:
            return redirect(url_for('authorize.authorize', provider_name='github'))
        
        resp = github.get("/user")
        if resp.ok:
            user_info = resp.json()
            print(user_info)  # Console log the user info
            flash(f"GitHub: Logged in as: {user_info['login']} (ID: {user_info['id']})")
        else:
            flash("Failed to fetch user details from GitHub.")

    # Handling Discord OAuth
    elif provider_name == 'discord':
        if not discord.authorized:
            flash("You are not authorized via Discord. Please try again.")
            return redirect(url_for('authorize.authorize', provider_name='discord'))
        
        resp = discord.get("/api/users/@me")
        if resp.ok:
            user_info = resp.json()
            print(user_info)  # Console log the user info
            flash(f"Discord: Logged in as: {user_info['username']}# {user_info['discriminator']} (ID: {user_info['id']})")
        else:
            flash("Failed to fetch user details from Discord.")

    else:
        flash("Invalid OAuth provider.")
        
    oidc_token = "extracted_from_user_info_or_elsewhere"

    return render_template('finalize_registration.html', oidc_token=oidc_token)

@app.route('/issue-identity', methods=['GET', 'POST'])
def issue_identity_route():
    if request.method == 'POST':
        user_private_key_hex = request.form['user_private_key']
        user_identifier = request.form['user_identifier']
        csr = "csr_placeholder"  # Replace with actual CSR generation or retrieval
        
        # Create an x509 certificate for the controllee
        x509_certificate = "x509_certificate_placeholder"  # Replace with actual certificate creation
        
        issuance_result = issue_identity(x509_certificate, user_identifier)
        if issuance_result:
            flash('Identity issued successfully.')
            return redirect(url_for('index'))
        else:
            flash('Failed to issue identity. Please try again.')
    
    # Render the issue identity form template
    return render_template('issue_identity.html')