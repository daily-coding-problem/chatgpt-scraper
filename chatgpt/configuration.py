class Configuration:
    def __init__(self,  use_temporary_chat: bool = False, accounts: dict = None, headless: bool = False):
        self.use_temporary_chat = use_temporary_chat
        self.accounts = accounts
        self.headless = False

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
