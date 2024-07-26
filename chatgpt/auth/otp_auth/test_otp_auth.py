import unittest
from chatgpt.auth.otp_auth import OTPAuth


class TestOTPAuth(unittest.TestCase):

    def test_parse_with_talent_id(self):
        self.assert_parsed_values(
            "otpauth://totp/Example:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example",
            None,
            "alice",
        )

    def test_parse_with_user(self):
        self.assert_parsed_values(
            "otpauth://totp/Example:alice?secret=JBSWY3DPEHPK3PXP&issuer=Example",
            "alice",
            None,
        )

    def assert_parsed_values(self, uri, expected_user, expected_talent_id):
        otpauth = OTPAuth(uri)
        self.assertEqual(otpauth.get_environment(), "Example")
        self.assertEqual(otpauth.get_user(), expected_user)
        self.assertEqual(otpauth.get_talent_id(), expected_talent_id)
        self.assertEqual(otpauth.get_secret(), "JBSWY3DPEHPK3PXP")
        self.assertEqual(otpauth.get_issuer(), "Example")

    def test_invalid_uri(self):
        with self.assertRaises(ValueError):
            uri = "otpauth://totp/Example:?secret=JBSWY3DPEHPK3PXP&issuer=Example"
            OTPAuth(uri)

    def test_missing_secret(self):
        with self.assertRaises(ValueError):
            uri = "otpauth://totp/Example:alice?issuer=Example"
            OTPAuth(uri)

    def test_missing_issuer(self):
        with self.assertRaises(ValueError):
            uri = "otpauth://totp/Example:alice?secret=JBSWY3DPEHPK3PXP"
            OTPAuth(uri)

    def test_to_string(self):
        uri = "otpauth://totp/Example:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example"
        otpauth = OTPAuth(uri)
        expected_str = "Environment: Example, User: None, Talent ID: alice, Secret: JBSWY3DPEHPK3PXP, Issuer: Example"
        self.assertEqual(str(otpauth), expected_str)
