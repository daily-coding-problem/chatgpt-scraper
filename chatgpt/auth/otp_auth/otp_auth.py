from enum import Enum
from urllib.parse import urlparse, unquote, parse_qs, urlencode


class Providers(Enum):
    GOOGLE = "google"
    CHATGPT = "chatgpt"


class OTPAuth:
    """
    Parses the OTP Auth URI and extracts the environment, talent_id, secret, issuer, algorithm, digits, and period.
    E.g., otpauth://totp/Example:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example
    """

    def __init__(self, uri: str):
        self.uri = uri
        self.environment = None
        self.talent_id = None
        self.user = None
        self.secret = None
        self.issuer = None
        self.algorithm = "SHA1"  # Default value
        self.digits = 6  # Default value
        self.period = 30  # Default value
        self._parse_uri()

    def _parse_uri(self):
        result = urlparse(self.uri)

        # Get the path and split it to extract the environment and user
        path_parts = result.path.strip("/").split(":")
        if len(path_parts) != 2 or not path_parts[1]:
            raise ValueError("Invalid URI format: Path must be 'environment:user'")

        self.environment = path_parts[0]

        if "@" in path_parts[1]:
            self.talent_id = path_parts[1].split("@")[0]
        else:
            self.user = unquote(path_parts[1])

        # Extract the query parameters
        parameters = parse_qs(result.query)

        if 'secret' not in parameters or 'issuer' not in parameters:
            raise ValueError("Missing required query parameters: 'secret' and 'issuer' are required")

        self.secret = parameters['secret'][0]
        self.issuer = parameters['issuer'][0]

        # Optional parameters
        if 'algorithm' in parameters:
            self.algorithm = parameters['algorithm'][0]
        if 'digits' in parameters:
            self.digits = int(parameters['digits'][0])
        if 'period' in parameters:
            self.period = int(parameters['period'][0])

    def get_environment(self) -> str:
        return self.environment

    def get_user(self) -> str:
        return self.user

    def get_talent_id(self) -> str:
        return self.talent_id

    def get_secret(self) -> str:
        return self.secret

    def get_issuer(self) -> str:
        return self.issuer

    def get_algorithm(self) -> str:
        return self.algorithm

    def get_digits(self) -> int:
        return self.digits

    def get_period(self) -> int:
        return self.period

    def __str__(self) -> str:
        return (
            f"Environment: {self.environment}, "
            f"User: {self.user}, "
            f"Talent ID: {self.talent_id}, "
            f"Secret: {self.secret}, "
            f"Issuer: {self.issuer}, "
            f"Algorithm: {self.algorithm}, "
            f"Digits: {self.digits}, "
            f"Period: {self.period}"
        )

    @staticmethod
    def construct_otp_uri(email: str, secret: str, issuer: str = "OpenAI", algorithm: str = "SHA1", digits: int = 6, period: int = 30) -> str:
        """
        Construct an OTP URI.
        """
        label = f"{issuer}:{email}"
        params = {
            'secret': secret,
            'issuer': issuer,
            'algorithm': algorithm,
            'digits': digits,
            'period': period
        }
        return f"otpauth://totp/{label}?{urlencode(params)}"

    @staticmethod
    def derive_issuer_by_provider(provider: str) -> str:
        """
        Derive the issuer name based on the provider.
        """
        if provider == "google":
            return "Google"

        return "OpenAI"

