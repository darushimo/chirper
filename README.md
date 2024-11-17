# Chirper

A Twitter clone built with Flask and SQLite.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

4. Run the application:
```bash
flask run
```

Visit http://localhost:5000 to use the application.

## Features

- User authentication (signup/login)
- Create and view posts
- Follow/unfollow other users
- Personal timeline of followed users' posts
- User profiles
