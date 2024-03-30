# src/web/api.py
import os
import jwt
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from config import DevelopmentConfig, ProductionConfig
from src.core.registration import register_user_with_letsid
from src.core.issuance import issue_identity
import json

load_dotenv()

api = Blueprint('api', __name__)

env = os.environ.get('FLASK_ENV', 'development')
if env == 'production':
    config = ProductionConfig()
else:
    config = DevelopmentConfig()
    
@api.route('/register', methods=['POST'])
def register():
    # Extract data from request
    data = request.get_json()
    print('Data:', data)

    try:
        # Parse oidc_token, which is a JSON string, to extract the jwt_token
        oidc_data = json.loads(data['oidc_token'])
        jwt_token = oidc_data.get('jwt_token')

        # Verify the JWT token
        decoded_jwt = jwt.decode(jwt_token, config.SECRET_KEY, algorithms=["HS256"])
        
        # You can add additional sanity checks here based on decoded JWT payload if needed

    except jwt.ExpiredSignatureError:
        return jsonify({"status": "error", "message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"status": "error", "message": "Invalid token"}), 401
    except Exception as e:
        # Handle other exceptions such as JSON parsing errors
        return jsonify({"status": "error", "message": str(e)}), 400

    # Proceed with registration if JWT token is valid
    registration_result = register_user_with_letsid(data['csr'], data['digital_signature'], data['oidc_token'])

    if registration_result:
        return jsonify({"status": "success", "data": registration_result}), 200
    else:
        return jsonify({"status": "error", "message": "Registration failed"}), 400

@api.route('/issue-identity', methods=['POST'])
def issue():
    data = request.get_json()
    # Assuming data contains 'x509_certificate' and 'user_identifier'
    issuance_result = issue_identity(data['x509_certificate'], data['user_identifier'])

    if issuance_result:
        return jsonify({"status": "success", "data": issuance_result}), 200
    else:
        return jsonify({"status": "error", "message": "Issuance failed"}), 400
