import pytest
from src.database.orm import ORM
from src.tests.model_for_testing import ModelForTesting
from user_app.database.database import database


@pytest.fixture
def orm():
    orm = ORM()
    orm.register(ModelForTesting)
    return orm


@pytest.fixture(autouse=True)
def reset_database():
    for key in database:
        database[key] = []


def test_register_model(orm):
    assert 'modelfortesting' in orm.models


def test_create_user(orm):
    user = orm.create(ModelForTesting, username='john_doe', password='password123')
    assert user.username == 'john_doe'
    assert user.password == 'password123'
    assert user.id is not None  # Ensure ID is set


def test_all_instances(orm):
    orm.create(ModelForTesting, username='john_doe', password='password123')
    orm.create(ModelForTesting, username='jane_doe', password='password123')
    users = orm.all(ModelForTesting)
    assert len(users) == 2
    assert users[0].username == 'john_doe'
    assert users[1].username == 'jane_doe'


def test_filter_instances(orm):
    orm.create(ModelForTesting, username='john_doe', password='password123')
    orm.create(ModelForTesting, username='jane_doe', password='password123')
    filtered_users = orm.filter(ModelForTesting, username='john_doe')
    assert len(filtered_users) == 1
    assert filtered_users[0].username == 'john_doe'


def test_get_by_id(orm):
    user1 = orm.create(ModelForTesting, username='john_doe', password='password123')
    user2 = orm.create(ModelForTesting, username='jane_doe', password='password123')
    retrieved_user1 = orm.get_by_id(ModelForTesting, user1.id)
    retrieved_user2 = orm.get_by_id(ModelForTesting, user2.id)
    assert retrieved_user1.username == 'john_doe'
    assert retrieved_user2.username == 'jane_doe'
    assert orm.get_by_id(ModelForTesting, 999) is None  # Ensure non-existent ID returns None


def test_get_all(orm):
    user1 = orm.create(ModelForTesting, username='user1', password='password1')
    user2 = orm.create(ModelForTesting, username='user2', password='password2')

    users = orm.all(ModelForTesting)
    assert len(users) == 2
    assert users[0].username == 'user1'
    assert users[1].username == 'user2'

