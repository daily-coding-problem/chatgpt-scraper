class Configuration:
    def __init__(self,  use_temporary_chat: bool = False, accounts: dict = None):
        self.use_temporary_chat = use_temporary_chat
        self.accounts = accounts

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
