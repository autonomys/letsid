# src/web/oauth_routes.py
from flask import Blueprint, request, redirect, url_for, flash

oauth_bp = Blueprint('oauth', __name__)

@oauth_bp.route('/finalize_registration', methods=['GET'])
def finalize_registration():
    # Here, you'll handle the OIDC token received from the OAuth provider
    # For demonstration purposes, let's assume you extract the OIDC token from the query parameters
    oidc_token = request.args.get('oidc_token')
    
    # Now you have the OIDC token, you can redirect to the registration route (/register)
    # You can pass the OIDC token as a query parameter to the registration route
    return redirect(url_for('register', oidc_token=oidc_token))
