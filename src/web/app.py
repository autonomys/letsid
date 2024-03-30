import os
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, flash
from config import DevelopmentConfig, ProductionConfig
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

@app.route('/finalize-registration', methods=['GET', 'POST'])
def finalize_registration():
    if request.method == 'POST':
        # Extract form data
        csr = request.form.get('csr')
        digital_signature = request.form.get('digital_signature')
        oidc_token = request.form.get('oidc_token')
        
        # Registration logic goes here
        
        flash('Registration finalized successfully.')
        return redirect(url_for('index'))  # Redirect to the home page or a confirmation page

    # For GET requests, retrieve OIDC token from URL parameters
    oidc_token = request.args.get('oidc_token', '')  # Default to empty string if not found

    # Pass the OIDC token to the template
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