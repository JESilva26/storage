# Storage

Storage is a full-stack file storage web application built with FastAPI, SQLAlchemy, and Jinja2.

The project was created to practice building and deploying a complete web application, including authentication, persistent data storage, file management, automated testing, and continuous integration.

## Live Demo

https://storage-azt0.onrender.com

> Note: The application currently uses SQLite and free-tier hosting. Stored data may be reset when the service is restarted.

## Features

- User account creation and login
- Password hashing with bcrypt
- Per-user file storage
- File upload, download, and deletion
- Server-rendered pages using Jinja2
- SQLAlchemy-backed user and file records
- Custom HTTP error pages
- Automated tests with pytest
- GitHub Actions CI on repository pushes

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Jinja2
- Bootstrap
- pytest
- GitHub Actions
- Uvicorn

## Project Structure

```text
storage/
├── .github/
│   └── workflows/
│       └── actions.yml
├── routes/
│   ├── auth.py
│   ├── files.py
│   └── pages.py
├── templates/
│   ├── account.html
│   ├── error.html
│   ├── home.html
│   ├── layout.html
│   ├── login.html
│   └── signup.html
├── tests/
│   └── test_app.py
├── database.py
├── main.py
├── models.py
├── schemas.py
└── requirements.txt
