import platform


def is_linux():
    """
    Returns True if the OS is Linux.
    :return: True if the OS is Linux.
    """

    return 'nux' in platform.system().lower()
