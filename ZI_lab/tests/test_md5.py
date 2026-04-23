import unittest
from backend.md5_service import MD5Service

class TestMD5(unittest.TestCase):

    def setUp(self):
        self.service = MD5Service()

    def test_rfc_empty_string(self):
        """Тест на порожній рядок (RFC 1321)"""
        expected = "D41D8CD98F00B204E9800998ECF8427E"
        self.assertEqual(self.service.hash_text(""), expected)

    def test_rfc_single_char(self):
        """Тест на один символ 'a' (RFC 1321)"""
        expected = "0CC175B9C0F1B6A831C399E269772661"
        self.assertEqual(self.service.hash_text("a"), expected)

    def test_rfc_abc(self):
        """Тест на рядок 'abc' (RFC 1321)"""
        expected = "900150983CD24FB0D6963F7D28E17F72"
        self.assertEqual(self.service.hash_text("abc"), expected)

    def test_rfc_message_digest(self):
        """Тест на рядок 'message digest' (RFC 1321)"""
        expected = "F96B697D7CB7938D525A2F31AAF161D0"
        self.assertEqual(self.service.hash_text("message digest"), expected)

    def test_avalanche_effect(self):
        """Тест лавиноподібного ефекту: зміна одного символу має повністю змінити хеш"""
        hash1 = self.service.hash_text("Hello World")
        hash2 = self.service.hash_text("Hello world")
        self.assertNotEqual(hash1, hash2)

    def test_case_insensitivity_not_allowed(self):
        """MD5 чутливий до регістру вводу"""
        self.assertNotEqual(
            self.service.hash_text("ABC"),
            self.service.hash_text("abc")
        )

if __name__ == '__main__':
    unittest.main()