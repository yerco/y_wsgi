# user_app README.md

## Create users
From terminal, run the following command to create
```bash
curl -X POST http://localhost:8000/create_user \
     -H "Content-Type: application/json" \
     -d '{"username": "new_user", "password": "password123"}'
```

