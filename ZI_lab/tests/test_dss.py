import unittest
import os
import shutil
from backend.dss_service import DSSService


class TestSignature(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Налаштування середовища перед усіма тестами"""
        cls.sig_service = DSSService()
        cls.test_dir = "temp_test_data"
        if not os.path.exists(cls.test_dir):
            os.makedirs(cls.test_dir)

    def setUp(self):
        """Підготовка перед кожним окремим тестом"""
        # 1. Генеруємо свіжі DSA ключі (DSS стандарт)
        self.priv_key, self.pub_key = self.sig_service.generate_dsa_keys(self.test_dir)

        # 2. Створюємо тестовий файл з даними
        self.file_path = os.path.join(self.test_dir, "test_file.bin")
        self.original_data = b"Secret academic data for Lab 5"
        with open(self.file_path, "wb") as f:
            f.write(self.original_data)

    def test_signature_generation_and_verification(self):
        """ТЕСТ 1: Перевірка успішного підпису та верифікації"""
        # Підписуємо дані
        hex_signature = self.sig_service.sign_data(self.original_data, self.priv_key)

        # Перевіряємо, що підпис не порожній і є HEX-рядком
        self.assertIsInstance(hex_signature, str)
        self.assertGreater(len(hex_signature), 0)

        # Верифікуємо підпис за допомогою публічного ключа
        result = self.sig_service.verify_data(self.original_data, hex_signature, self.pub_key)
        self.assertTrue(result, "Верифікація мала пройти успішно для коректних даних.")

    def test_tamper_data_fails_verification(self):
        """ТЕСТ 2: Перевірка, що зміна даних робить підпис недійсним"""
        hex_signature = self.sig_service.sign_data(self.original_data, self.priv_key)

        # Змінюємо дані (імітація втручання)
        tampered_data = self.original_data + b"modified"

        result = self.sig_service.verify_data(tampered_data, hex_signature, self.pub_key)
        self.assertFalse(result, "Підпис повинен бути недійсним, якщо дані змінено.")

    def test_tamper_signature_fails_verification(self):
        """ТЕСТ 3: Перевірка, що зміна самого HEX-підпису робить його недійсним"""
        hex_signature = self.sig_service.sign_data(self.original_data, self.priv_key)

        # Змінюємо один символ у HEX-рядку
        modified_sig = "a" + hex_signature[1:] if hex_signature[0] != "a" else "b" + hex_signature[1:]

        result = self.sig_service.verify_data(self.original_data, modified_sig, self.pub_key)
        self.assertFalse(result, "Верифікація повинна провалитися при зміненому HEX-коді.")

    def test_wrong_key_verification_fails(self):
        """ТЕСТ 4: Перевірка підпису чужим публічним ключем"""
        # Створюємо іншу пару ключів
        other_dir = os.path.join(self.test_dir, "other_keys")
        _, other_pub_key = self.sig_service.generate_dsa_keys(other_dir)

        hex_signature = self.sig_service.sign_data(self.original_data, self.priv_key)

        # Намагаємось перевірити підпис ключем, який не відповідає приватному
        result = self.sig_service.verify_data(self.original_data, hex_signature, other_pub_key)
        self.assertFalse(result, "Підпис не повинен бути підтверджений чужим публічним ключем.")

    def tearDown(self):
        """Очищення після кожного тесту (необов'язково, якщо файли перезаписуються)"""
        pass

    @classmethod
    def tearDownClass(cls):
        """Видалення тимчасової папки після завершення всіх тестів"""
        if os.path.exists(cls.test_dir):
            shutil.rmtree(cls.test_dir)


if __name__ == '__main__':
    unittest.main()