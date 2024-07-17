import os

from src.config import config as default_config
from src.config_loader import load_config


def test_default_config():
    assert default_config.SECRET_KEY == 'secret-key'
    assert default_config.SESSION_ID_ROTATION_INTERVAL == 1800


def test_dummy_app_config():
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '')
    dummy_config = load_config('dummy_app', base_dir=base_dir).config
    assert dummy_config['SECRET_KEY'] == 'dummy-app-secret-key'
    assert dummy_config['SESSION_ID_ROTATION_INTERVAL'] == 1800  # Default value as it's not overridden
