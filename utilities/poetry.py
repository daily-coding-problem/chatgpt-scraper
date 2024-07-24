import os

import toml
import yaml


def get_attribute_from_pyproject(attribute_name: str) -> str:
    """
    Get the specified attribute from pyproject.toml
    :param attribute_name: The attribute name to retrieve (e.g., "version" or "name")
    :return: The value of the specified attribute
    """

    data = toml.load("pyproject.toml")

    return data.get("tool", {}).get("poetry", {}).get(attribute_name, "")


def get_version():
    """
    Get the version from pyproject.toml
    :return: The version of this project
    """

    return get_attribute_from_pyproject("version")


def get_name():
    """
    Get the name from pyproject.toml
    :return: The name of this project
    """

    return get_attribute_from_pyproject("name")


def get_authors():
    """
    Get the author from pyproject.toml
    :return: The author of this project
    """

    authors = get_attribute_from_pyproject("authors")

    # return a comma separated list of authors
    return ", ".join(authors)


def get_description():
    """
    Get the description from pyproject.toml
    :return: The description of this project
    """

    return get_attribute_from_pyproject("description")


def load_config(config_path):
    """
    load the config file
    :param config_path: The path to the config file
    :return: The config file
    """

    # check if the config file exists
    if not os.path.isfile(config_path):
        print(f"{config_path} does not exist")

        exit(1)

    with open(config_path, "r") as config_file:
        content = config_file.read()
        return yaml.safe_load(content)
