# Y-WSGI
A Femto framework for learning purposes

## Tools of the trade
- Python 3.11.8

## How to run
1. Install the required packages
```bash
$ pip install -r requirements.txt
```

2. Run the server
2.1 Using gunicorn
```bash
$ gunicorn src.app:application [--reload]
```
2.2 Using uWSGI
```bash
$ uwsgi --http :8000 --wsgi-file src/app.py --callable application [--py-autoreload=1]
```
And go to http://127.0.0.1:8000

