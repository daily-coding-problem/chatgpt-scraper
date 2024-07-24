import pyotp


def generate_otp(secret_key):
    """
    Generates a TOTP using the secret key.
    :param secret_key: The secret key used to generate the TOTP. This is taken from the OTPAuth -> secret property.
    :return: The TOTP generated using the secret key.
    """
    # Create a TOTP object with the secret key.
    totp = pyotp.TOTP(secret_key)

    # Generate an OTP with the TOTP object.
    return totp.now()
