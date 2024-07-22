class AnotherDummyAppConfig:
    SECRET_KEY = 'another-dummy-app-secret-key'
    SESSION_ID_ROTATION_INTERVAL = 3600  # Overridden value


config = AnotherDummyAppConfig()
