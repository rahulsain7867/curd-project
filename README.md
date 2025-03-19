# Django CRUD API Project

This is a Django-based CRUD (Create, Read, Update, Delete) API project designed for managing users and their tasks (To-Dos). The API includes authentication, user management, and task management with proper validations.

## Features
- **User Authentication** using JWT (JSON Web Token)
- **CRUD Operations** for managing user tasks
- **Role-Based Access Control** (Users can only modify their own tasks)
- **Best Practices** including `.env` configuration, structured API responses, and optimized queries

## Tech Stack
- **Backend:** Django, Django REST Framework (DRF)
- **Authentication:** JWT Authentication
- **Database:** SQLite (or any relational DB)

## Installation & Setup
1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd <repo-folder>
   ```
2. **Create a virtual environment & activate it:**
   ```sh
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Run database migrations:**
   ```sh
   python manage.py migrate
   ```
5. **Create a superuser (for admin access):**
   ```sh
   python manage.py createsuperuser
   ```
6. **Run the server:**
   ```sh
   python manage.py runserver
   ```
   The project will be available at `http://127.0.0.1:8000/`.

## API Documentation
You can find the full API collection in **Postman:**
👉 [Postman Collection](https://documenter.getpostman.com/view/41954240/2sAYkEqztu)

## API Endpoints
### User Authentication
- **Register User** - `POST /api/auth/register/`
- **Login User** - `POST /api/auth/login/`

### Todo Management
- **Create Todo** - `POST /api/users/{user_id}/todos/`
- **Get All Todos** - `GET /api/users/{user_id}/todos/`
- **Update Todo** - `PUT /api/users/{user_id}/todos/{todo_id}/update/`
- **Partial Update Todo** - `PATCH /api/users/{user_id}/todos/{todo_id}/partial-update/`
- **Delete Todo** - `DELETE /api/users/{user_id}/todos/{todo_id}/`

## Redirecting to Admin Panel
By default, when you visit `http://127.0.0.1:8000/`, you will be redirected to `http://127.0.0.1:8000/admin/`.

## License
This project is open-source and can be modified as needed.

---
🚀 **Happy Coding!**

