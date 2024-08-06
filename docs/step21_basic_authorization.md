# Basic Authorization

- Added a kinda hardcoded authorization
```
    def _authorize(self, user: Dict, route: str) -> bool:
        role = user.get("role")
        # Define role-based access control logic here
        if role == "admin":
            return True  # admin have access to everything
        if role == "user":
            if route not in self.public_routes:
                return False
            return True
        return False
```

- Added a basic README.md
