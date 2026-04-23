import unittest
import os
import struct
from backend.rc5_service import RC5Service
from backend.md5_service import MD5Service
from backend.lcg_service import LCGService


class TestRC5Complex(unittest.TestCase):
    def setUp(self):
        self.rc5 = RC5Service(w=64, r=8, b=32)
        self.md5 = MD5Service()
        self.lcg = LCGService()
        self.password = "MySecurePassword123"
        self.test_file = "test_data.txt"
        self.enc_file = "test_data.txt.enc"
        self.dec_file = "test_data.txt.dec"

    def tearDown(self):
        for f in [self.test_file, self.enc_file, self.dec_file]:
            if os.path.exists(f):
                os.remove(f)

    def test_block_consistency(self):
        """Тест: чи блок після дешифрування повертається до оригіналу (ECB рівень)"""
        S = self.rc5._expand_key(self.password, self.md5)
        original_block = struct.pack('<2Q', 0x123456789ABCDEF0, 0x0FEDCBA987654321)

        encrypted = self.rc5._encrypt_block(original_block, S)
        decrypted = self.rc5._decrypt_block(encrypted, S)

        self.assertEqual(original_block, decrypted, "Блок не збігається після розшифрування!")

    def test_file_encryption_decryption(self):
        """Тест: повний цикл шифрування файлу (CBC + Padding + IV)"""
        content = b"This is a secret message for Lab 3 Var 9!"
        with open(self.test_file, "wb") as f:
            f.write(content)

        self.rc5.encrypt_file(self.test_file, self.enc_file, self.password, self.md5, self.lcg)

        self.assertTrue(os.path.exists(self.enc_file))
        self.assertNotEqual(os.path.getsize(self.enc_file), 0)

        self.rc5.decrypt_file(self.enc_file, self.dec_file, self.password, self.md5)

        with open(self.dec_file, "rb") as f:
            decrypted_content = f.read()

        self.assertEqual(content, decrypted_content, "Вміст файлу після дешифрування пошкоджений!")


if __name__ == '__main__':
    unittest.main()