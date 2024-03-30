# src/core/client.py
import os
import requests
from typing import Tuple, Optional, Dict

class LetsIDClient:
    def __init__(self, server_url: str = os.getenv("LETSID_SERVER_URL", "https://letsid.ai/api/")):
        self.server_url = server_url

    def generate_key_pair_and_csr(self) -> Tuple[str, str, str, str]:
        """
        Generates a key pair and CSR. This method is a placeholder and should be
        replaced with actual calls to the Auto SDK or equivalent library.
        """
        public_key_hex = os.getenv("PUBLIC_KEY_HEX", "public_key_hex_placeholder")
        private_key_hex = os.getenv("PRIVATE_KEY_HEX", "private_key_hex_placeholder")
        seed_hex = os.getenv("SEED_HEX", "seed_hex_placeholder")
        csr = os.getenv("CSR", "csr_placeholder")

        return public_key_hex, private_key_hex, seed_hex, csr

    def sign_csr_with_private_key(self, csr: str, private_key_hex: str) -> str:
        """
        Signs the CSR with the user's private key. Placeholder function.
        """
        digital_signature = os.getenv("DIGITAL_SIGNATURE", "digital_signature_placeholder")
        return digital_signature

    def send_data_to_letsid(self, endpoint: str, data: Dict) -> Optional[Dict]:
        """
        Sends data to the LetsID server for a specific endpoint.
        """
        full_url = self.server_url + endpoint
        response = requests.post(full_url, json=data)

        if response.status_code == 200:
            return response.json()
        else:
            return None

# Example usage within the same module (could also be used by importing this class in other modules)
if __name__ == "__main__":
    client = LetsIDClient()

    # Example of generating a key pair and CSR
    pub_key, priv_key, seed, csr = client.generate_key_pair_and_csr()
    print(f"Generated CSR: {csr}")

    # Example of signing a CSR
    signature = client.sign_csr_with_private_key(csr, priv_key)
    print(f"Digital Signature: {signature}")

    # Example of sending data to LetsID for registration
    registration_data = {
        "csr": csr,
        "digital_signature": signature,
        "oidc_token": os.getenv("OIDC_TOKEN", "oidc_token_placeholder")
    }
    registration_result = client.send_data_to_letsid("register", registration_data)
    print(f"Registration Result: {registration_result}")
