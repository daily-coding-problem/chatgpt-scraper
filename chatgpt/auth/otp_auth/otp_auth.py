from urllib.parse import urlparse, unquote, parse_qs


class OTPAuth:
    """
    Parses the OTP Auth URI and extracts the environment, talent_id, secret, and issuer.
    e.g. otpauth://totp/Example:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example
    """

    def __init__(self, uri):
        result = urlparse(uri)

        self.talent_id = None
        self.user = None

        # Get the path and split it to extract the environment and user
        path_parts = result.path.strip("/").split(":")
        if len(path_parts) != 2 or not path_parts[1]:
            raise ValueError("Invalid URI format")

        if "@" in path_parts[1]:
            self.talent_id = path_parts[1].split("@")[0]
        else:
            self.user = unquote(path_parts[1])

        self.environment = path_parts[0]

        # Extract the query parameters
        parameters = parse_qs(result.query)

        if 'secret' not in parameters or 'issuer' not in parameters:
            raise ValueError("Missing required query parameters")

        self.secret = parameters['secret'][0]
        self.issuer = parameters['issuer'][0]

    def get_environment(self):
        return self.environment

    def get_user(self):
        return self.user

    def get_talent_id(self):
        return self.talent_id

    def get_secret(self):
        return self.secret

    def get_issuer(self):
        return self.issuer

    def __str__(self):
        return f"Environment: {self.environment}, User: {self.user}, Talent ID: {self.talent_id}, Secret: {self.secret}, Issuer: {self.issuer}"
