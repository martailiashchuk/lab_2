import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import dsa

class DSSService:
    def generate_dsa_keys(self, folder):
        """DSS вимагає використання DSA"""
        private_key = dsa.generate_private_key(key_size=2048)
        public_key = private_key.public_key()

        if not os.path.exists(folder):
            os.makedirs(folder)

        priv_path = os.path.join(folder, "dsa_private.pem")
        pub_path = os.path.join(folder, "dsa_public.pem")

        with open(priv_path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        with open(pub_path, "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        return priv_path, pub_path

    def sign_data(self, data, private_key_path):
        """Підписує байтові дані та повертає підпис у HEX"""
        with open(private_key_path, "rb") as k:
            private_key = serialization.load_pem_private_key(k.read(), password=None)

        # DSA підпис автоматично генерує (r, s) у форматі DER
        signature = private_key.sign(data, hashes.SHA256())
        return signature.hex()

    def verify_data(self, data, hex_signature, public_key_path):
        """Перевіряє підпис, наданий у HEX форматі"""
        try:
            with open(public_key_path, "rb") as k:
                public_key = serialization.load_pem_public_key(k.read())

            signature = bytes.fromhex(hex_signature)
            public_key.verify(signature, data, hashes.SHA256())
            return True
        except Exception:
            return False
