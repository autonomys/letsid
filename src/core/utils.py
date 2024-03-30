# src/core/utils.py
import requests

def generate_key_pair_and_csr():
    """
    Generates a key pair and CSR. This function is a placeholder and should be
    replaced with actual calls to the Auto SDK or equivalent library.
    """
    public_key_hex = "public_key_hex_placeholder"
    private_key_hex = "private_key_hex_placeholder"
    seed_hex = "seed_hex_placeholder"
    csr = "csr_placeholder"
    
    return public_key_hex, private_key_hex, seed_hex, csr

def send_data_to_letsid(endpoint, data):
    """
    Sends data to the LetsID server. The specific endpoint and data structure
    are provided by the calling function.
    """
    letsid_server_url = f"https://letsid.server/api/{endpoint}"
    
    response = requests.post(letsid_server_url, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None
