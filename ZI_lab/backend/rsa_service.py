import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


class RSAService:
    def __init__(self):
        self.key_size = 2048

    def save_keys_to_dir(self, directory):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size
        )
        public_key = private_key.public_key()

        priv_path = os.path.join(directory, "private_key.pem")
        pub_path = os.path.join(directory, "public_key.pem")

        with open(priv_path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        with open(pub_path, "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        return priv_path, pub_path

    def encrypt_file(self, file_path, public_key_path):
        with open(public_key_path, "rb") as k:
            public_key = serialization.load_pem_public_key(k.read())

        max_chunk = (self.key_size // 8) - 2 * hashes.SHA256.digest_size - 2

        output_path = file_path + ".rsa"
        with open(file_path, "rb") as f_in, open(output_path, "wb") as f_out:
            while True:
                chunk = f_in.read(max_chunk)
                if not chunk: break
                encrypted_chunk = public_key.encrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                f_out.write(encrypted_chunk)
        return output_path

    def decrypt_file(self, file_path, private_key_path):
        with open(private_key_path, "rb") as k:
            private_key = serialization.load_pem_private_key(k.read(), password=None)

        chunk_size = self.key_size // 8
        output_path = file_path.replace(".rsa", ".dec_rsa")

        with open(file_path, "rb") as f_in, open(output_path, "wb") as f_out:
            while True:
                chunk = f_in.read(chunk_size)
                if not chunk: break
                decrypted_chunk = private_key.decrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                f_out.write(decrypted_chunk)
        return output_path