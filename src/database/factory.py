from src.database.models import User


class UserFactory:
    @staticmethod
    def create_user(username: str, password: str) -> User:
        # Add complex logic here if needed
        return User(username=username, password=password)


# Usage
# user = UserFactory.create_user('john_doe', 'password123')
