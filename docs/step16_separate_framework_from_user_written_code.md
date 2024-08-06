# Separate Framework from User-Written Code

## Notes
- Install sqlalchemy
```bash
pip install SQLAlchemy==2.0.31
```

- TODO: check that SQLAlchemy integrates well, there are tests for those purposes

## Registry Pattern
The `AppRegistry` class manages application instances, ensuring that each application can be uniquely 
identified and accessed.
    ```python
    class AppRegistry:
        def __init__(self):
            self._apps: Dict[str, App] = {}
    
        def create_app(self, name: str) -> App:
            if name in self._apps:
                raise ValueError(f'App with {name} already exists')
            app = App()
            self._apps[name] = app
            return app
    
        def get_app(self, name: str) -> App:
            return self._apps.get(name)
    
        def list_apps(self) -> Dict[str, App]:
            return self._apps
    ```

Note: SQLAlchemy integration has not being tested at all.
