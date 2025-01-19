# Task Manager API

A robust Flask-based Task Management API that demonstrates modern Python web development practices. This project implements a RESTful API with features like user authentication, task management, file attachments, and task sharing capabilities.

## Features

- 🔐 JWT Authentication
- 📝 Task CRUD Operations
- 🎨 Task Categories with Custom Colors
- 📊 Task Statistics and Analytics
- 🔄 Task Sharing between Users
- 📎 File Attachments
- ⏰ Due Date Tracking
- 🎯 Priority Levels
- 📈 Progress Tracking

## Tech Stack

- Python 3.8+
- Flask 2.0.1
- Flask-SQLAlchemy 2.5.1
- Flask-JWT-Extended 4.3.1
- SQLite (configurable for other databases)
- Email-Validator 1.1.3
- Python-Magic 0.4.24

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/task-manager-api.git
```

2. Navigate to the project directory:

```bash
cd task-manager-api
``` 

3. Install dependencies:

```bash
pip install -r requirements.txt
``` 

4. Set up the database:

```bash
flask db init
flask db migrate
flask db upgrade
``` 

5. Run the development server:

```bash
flask run
``` 
