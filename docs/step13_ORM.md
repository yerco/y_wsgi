# ORM

## 1. Aggregate (Domain Pattern)
- **Aggregate**: A cluster of associated objects that we treat as a unit for the purpose of data changes. 
- Each aggregate has a root and a boundary. The boundary defines what is inside the aggregate. 
- The root is a single, specific entity contained in the aggregate.

Application to Our ORM:
- Aggregate Root: In our simplified ORM, each `Model` class (e.g., `User`) can be seen as an aggregate root.
- Boundaries: Aggregates define clear boundaries and ownership of objects, 
ensuring that changes are made in a controlled manner through the aggregate root.

Example
```python
class Order(Model):
    id = IntegerField()
    customer_id = IntegerField()
    total_amount = FloatField()
    # OrderItem is part of the Order aggregate
    items = []

class OrderItem:
    product_id = IntegerField()
    quantity = IntegerField()
    price = FloatField()
```

## 2. Factory (Design Pattern)
Factories are used to encapsulate the creation of objects. They provide a way to create objects without exposing
the instantiation logic to the client.
Application to Our ORM:

- Factory Method: We are already using a **simple factory** method pattern in the `ORM.create` method to handle
the creation of model instances.
- Encapsulation: This pattern helps in keeping the instantiation logic encapsulated and centralized.

```python
class UserFactory:
    @staticmethod
    def create_user(username: str, password: str) -> User:
        # Additional logic to hash password or other setup can go here
        return User(username=username, password=password)
```

## 3. Repositories (Design Pattern)
Repositories provide a way to access and manage aggregates. They act as a collection-like interface 
to access domain objects, abstracting the details of data storage and retrieval.

Application to Our ORM:

- Repository Pattern: We can create repository classes to manage the retrieval and persistence of aggregates, 
providing a clear separation between the domain model and data access logic.

```python
class UserRepository:
    def __init__(self, orm: ORM):
        self.orm = orm

    def add(self, user: User) -> None:
        self.orm.create('user', **user.__dict__)

    def get_by_username(self, username: str) -> User:
        users = self.orm.filter('user', username=username)
        return users[0] if users else None

    def get_all(self) -> List[User]:
        return self.orm.all('user')
```

## Example of usage at main.py
```python
# Example usage
user_repo = UserRepository(orm)
user_repo.add(User(username='johnny_marx', password='123password'))

# Create a user using the factory and add it via the repository
user = orm.create(User, username='john_doe', password='password123')
print(user)
user = orm.create(User, username='jane_doe', password='password123')
print(user)

users = orm.all(User)
print("All of them:\n", users)
```
