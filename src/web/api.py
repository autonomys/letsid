# src/web/api.py
from flask import Blueprint, request, jsonify
from src.core.registration import register_user_with_letsid
from src.core.issuance import issue_identity

api = Blueprint('api', __name__)

@api.route('/register', methods=['POST'])
def register():
    # Extract data from request
    data = request.get_json()
    print('Data:', data)
    # Assuming data contains 'csr', 'digital_signature', and 'oidc_token'
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
