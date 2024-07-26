import json
import base64
import os


class AccountsDeserializer:
    def __init__(self, base64_string=None):
        """
        Initialize the AccountsDeserializer with a base64 string.
        If no base64 string is provided, it will attempt to read from the 'TEST_ACCOUNTS' environment variable.
        """
        if base64_string is None:
            base64_string = os.environ.get('TEST_ACCOUNTS', '')
        self.accounts = self._deserialize(base64_string)

    @staticmethod
    def _deserialize(base64_string) -> dict:
        """
        Deserialize a base64 string to a dictionary.
        """
        if not base64_string:
            return {}

        try:
            decoded_bytes = base64.b64decode(base64_string)
            decoded_string = decoded_bytes.decode('utf-8')
            return json.loads(decoded_string)
        except (base64.binascii.Error, json.JSONDecodeError) as e:
            raise ValueError(f"Invalid base64 string or JSON format: {e}") from e

    def get_account(self, email):
        """
        Get the account details for a specific email.
        """
        return self.accounts.get(email)

    def get_all_accounts(self):
        """
        Get all accounts.
        """
        return self.accounts

    def __str__(self):
        """
        Return a string representation of the accounts.
        """
        return json.dumps(self.accounts, indent=4)
