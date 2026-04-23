import unittest
import os
import shutil
from backend.rsa_service import RSAService


class TestRSAService(unittest.TestCase):
    def setUp(self):
        """Налаштування перед кожним тестом"""
        self.rsa = RSAService()
        self.test_dir = "temp_test_keys"
        self.test_files_dir = "temp_test_files"

        # Створюємо тимчасові папки
        for folder in [self.test_dir, self.test_files_dir]:
            if not os.path.exists(folder):
                os.makedirs(folder)

        # Шляхи до ключів
        self.priv_key_path = os.path.join(self.test_dir, "private_key.pem")
        self.pub_key_path = os.path.join(self.test_dir, "public_key.pem")

    def tearDown(self):
        """Очищення після кожного тесту"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        if os.path.exists(self.test_files_dir):
            shutil.rmtree(self.test_files_dir)

    def test_key_generation(self):
        """Тест 1: Перевірка створення та збереження ключів"""
        priv, pub = self.rsa.save_keys_to_dir(self.test_dir)
        self.assertTrue(os.path.exists(priv))
        self.assertTrue(os.path.exists(pub))
        self.assertEqual(priv, self.priv_key_path)

    def test_small_file_encryption(self):
        """Тест 2: Шифрування файлу, меншого за розмір блоку (RSA OAEP)"""
        self.rsa.save_keys_to_dir(self.test_dir)
        data = b"Hello, RSA! This is a short message."
        file_path = os.path.join(self.test_files_dir, "small.txt")

        with open(file_path, "wb") as f:
            f.write(data)

        enc_file = self.rsa.encrypt_file(file_path, self.pub_key_path)
        dec_file = self.rsa.decrypt_file(enc_file, self.priv_key_path)

        with open(dec_file, "rb") as f:
            decrypted_data = f.read()

        self.assertEqual(data, decrypted_data)

    def test_large_file_multiblock(self):
        """Тест 3: Шифрування великого файлу (кілька блоків по 190 байт)"""
        # Створюємо дані розміром 1000 байт (це приблизно 6 блоків)
        self.rsa.save_keys_to_dir(self.test_dir)
        data = os.urandom(1000)
        file_path = os.path.join(self.test_files_dir, "large.bin")

        with open(file_path, "wb") as f:
            f.write(data)

        enc_file = self.rsa.encrypt_file(file_path, self.pub_key_path)
        dec_file = self.rsa.decrypt_file(enc_file, self.priv_key_path)

        with open(dec_file, "rb") as f:
            decrypted_data = f.read()

        self.assertEqual(data, decrypted_data)

    def test_decryption_failure(self):
        """Тест 4: Спроба розшифрувати невірним ключем (Покриття помилок)"""
        self.rsa.save_keys_to_dir(self.test_dir)
        file_path = os.path.join(self.test_files_dir, "fail.txt")
        with open(file_path, "wb") as f: f.write(b"Sensitive data")

        enc_file = self.rsa.encrypt_file(file_path, self.pub_key_path)

        # Створюємо іншу пару ключів (чужу)
        other_dir = "other_keys"
        os.makedirs(other_dir)
        other_priv, _ = self.rsa.save_keys_to_dir(other_dir)

        # Спроба розшифрувати чужим ключем має викликати помилку
        with self.assertRaises(Exception):
            self.rsa.decrypt_file(enc_file, other_priv)

        shutil.rmtree(other_dir)


if __name__ == '__main__':
    unittest.main()
