import os
import sys

from src.config import config as default_config
from src.config_loader import load_config


def test_default_config():
    assert default_config.SECRET_KEY == 'secret-key'
    assert default_config.SESSION_ID_ROTATION_INTERVAL == 1800


def test_load_default_config():
    config = load_config()
    assert config.DEBUG is False
    assert config.SECRET_KEY == 'secret-key'


def test_load_app_specific_config():
    # Set up the base directory where the apps are located
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'apps')
    # Set up the app name
    app_name = 'dummy_app'
    # Add the base directory to sys.path to ensure importlib can find the modules
    sys.path.insert(0, base_dir)
    # Load the config for the app
    config = load_config(app_name, base_dir)
    # Remove the base directory from sys.path after the test to avoid side effects
    sys.path.pop(0)

    assert config.DEBUG is False
    assert config.SECRET_KEY == 'dummy-app-secret-key'
    assert config.APP_NAME == app_name
    assert config.BASE_DIR == base_dir


def test_load_another_app_specific_config():
    # Set up the base directory where the apps are located
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'apps')
    # Set up the app name
    app_name = 'another_dummy_app'
    # Add the base directory to sys.path to ensure importlib can find the modules
    sys.path.insert(0, base_dir)
    # Load the config for the app
    config = load_config(app_name, base_dir)
    # Remove the base directory from sys.path after the test to avoid side effects
    sys.path.pop(0)

    assert config.SECRET_KEY == 'another-dummy-app-secret-key'
    assert config.APP_NAME == app_name
    assert config.BASE_DIR == base_dir


def test_multiple_app_configs():
    # Set up the base directory where the apps are located
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'apps')
    # Set up the app names
    app_names = ['dummy_app', 'another_dummy_app']
    # Prepare a dictionary to hold the configs
    configs = {}
    # Add the base directory to sys.path to ensure importlib can find the modules
    sys.path.insert(0, base_dir)
    # Load the config for each app and store in the dictionary
    for app_name in app_names:
        configs[app_name] = load_config(app_name, base_dir)
    # Remove the base directory from sys.path after the test to avoid side effects
    sys.path.pop(0)

    # Assertions for dummy_app
    dummy_app_config = configs['dummy_app']
    assert dummy_app_config.SECRET_KEY == 'dummy-app-secret-key'
    assert dummy_app_config.APP_NAME == 'dummy_app'
    assert dummy_app_config.BASE_DIR == base_dir

    # Assertions for another_dummy_app
    another_dummy_app_config = configs['another_dummy_app']
    assert another_dummy_app_config.SECRET_KEY == 'another-dummy-app-secret-key'
    assert another_dummy_app_config.APP_NAME == 'another_dummy_app'
    assert another_dummy_app_config.BASE_DIR == base_dir
