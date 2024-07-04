from src.tests.model_for_testing import ModelForTesting


class UserFactory:
    @staticmethod
    def create_user(username: str, password: str) -> ModelForTesting:
        # Add complex logic here if needed
        return ModelForTesting(username=username, password=password)


# Usage
# user = UserFactory.create_user('john_doe', 'password123')
