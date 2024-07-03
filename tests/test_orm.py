import pytest
from src.database.orm import ORM
from src.database.models import User
from src.database.database import database


@pytest.fixture
def orm():
    orm = ORM()
    orm.register(User)
    return orm


@pytest.fixture(autouse=True)
def reset_database():
    for key in database:
        database[key] = []


def test_register_model(orm):
    assert 'user' in orm.models


def test_create_user(orm):
    user = orm.create(User, username='john_doe', password='password123')
    assert user.username == 'john_doe'
    assert user.password == 'password123'
    assert user.id is not None  # Ensure ID is set


def test_all_instances(orm):
    orm.create(User, username='john_doe', password='password123')
    orm.create(User, username='jane_doe', password='password123')
    users = orm.all(User)
    assert len(users) == 2
    assert users[0].username == 'john_doe'
    assert users[1].username == 'jane_doe'


def test_filter_instances(orm):
    orm.create(User, username='john_doe', password='password123')
    orm.create(User, username='jane_doe', password='password123')
    filtered_users = orm.filter(User, username='john_doe')
    assert len(filtered_users) == 1
    assert filtered_users[0].username == 'john_doe'


def test_get_by_id(orm):
    user1 = orm.create(User, username='john_doe', password='password123')
    user2 = orm.create(User, username='jane_doe', password='password123')
    retrieved_user1 = orm.get_by_id(User, user1.id)
    retrieved_user2 = orm.get_by_id(User, user2.id)
    assert retrieved_user1.username == 'john_doe'
    assert retrieved_user2.username == 'jane_doe'
    assert orm.get_by_id(User, 999) is None  # Ensure non-existent ID returns None


def test_get_all(orm):
    user1 = orm.create(User, username='user1', password='password1')
    user2 = orm.create(User, username='user2', password='password2')

    users = orm.all(User)
    assert len(users) == 2
    assert users[0].username == 'user1'
    assert users[1].username == 'user2'

