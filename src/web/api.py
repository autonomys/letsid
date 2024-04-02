# src/web/api.py
import os
import json
import jwt
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from config import DevelopmentConfig, ProductionConfig
from src.core.registration import register_user_with_letsid
from src.core.issuance import issue_identity

# Load environment variables
load_dotenv()

api = Blueprint('api', __name__)

# Configuration setup based on the environment
config = ProductionConfig() if os.getenv('FLASK_ENV') == 'production' else DevelopmentConfig()

def validate_and_extract_jwt(token: str):
    """
    Validates and decodes a JWT token. Returns the decoded token if valid,
    otherwise raises the respective jwt exceptions.
    """
    return jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])

@api.route('/register', methods=['POST'])
def register():
    data = request.get_json(force=True, silent=True) or {}
    
    print('data', data)
    
    public_key = data.get('public_key')
    private_key = data.get('private_key')
    seed = data.get('seed')
    auto_id = data.get('auto_id')
    jwt_token = data.get('jwt_token')
    print('jwt_token', jwt_token)

    try:
        decoded_jwt = validate_and_extract_jwt(jwt_token)
        print('decoded_jwt', decoded_jwt)
        # Place for additional JWT checks if necessary
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        return jsonify({"status": "error", "message": str(e)}), 401
    except Exception as e:
        return jsonify({"status": "error", "message": "JWT validation failed"}), 400

    registration_result = register_user_with_letsid(auto_id, public_key, jwt_token, decoded_jwt)
    if registration_result:
        return jsonify({"status": "success", "data": registration_result}), 200
    return jsonify({"status": "error", "message": "Registration failed"}), 400

@api.route('/issue-identity', methods=['POST'])
def issue():
    data = request.get_json(force=True, silent=True) or {}
    
    issuance_result = issue_identity(data.get('x509_certificate'), data.get('user_identifier'))
    if issuance_result:
        return jsonify({"status": "success", "data": issuance_result}), 200
    return jsonify({"status": "error", "message": "Issuance failed"}), 400