# 📚 Book Management System - Django REST API

A RESTful API built using Django and Django REST Framework to manage users, books, and personalized reading lists.

---

## ✨ Features

### 👤 User Management
- User registration with email and username (both unique)
- Secure login using token-based authentication (JWT)
- User profile management (update profile details)

### 📘 Book Management
- Authenticated users can:
  - Create, update, and delete books
  - Upload books with title, author(s), genre, publication date, and optional description
- All users can view all available books

### 📂 Reading List
- Users can:
  - Create and manage reading lists
  - Add books to their reading list in a preferred order
  - Remove books from reading lists

### ⚙️ Error Handling
- Well-structured validation and error messages
- Returns meaningful HTTP status codes and error responses

---

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework
- **Authentication**: JWT or Token Authentication (via `djangorestframework-simplejwt` )
- **Database**: SQLite (dev), PostgreSQL (prod-ready)
- **Serialization**: Django REST Framework Serializers
- **Image Uploads**: Django `ImageField` with proper media handling

---

## 📦 Installation

### 1. Clone the repo
```bash
git clone https://github.com/mebinmathew006/BookManagementSystem.git
cd BookManagementSystem

2. Create virtual environment and activate it

    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
3. Install dependencies

pip install -r requirements.txt
4. Apply migrations

python manage.py migrate
5. Run the server

python manage.py runserver
🔐 API Authentication
This project uses jwt-based authentication .


Use the token in headers for authenticated requests:


Authorization: Bearer <your_token>

🔀 API Endpoints 
Users

Method	Endpoint	Description
POST	/users/signup/	Register new user
POST	/users/login/	Login and get token
GET	/users/profile/	Get current user info
PUT	/users/profile/	Update profile

Books

Method	Endpoint	Description
GET	/books/upload	List all books
POST	/books/upload	Create a new book
PUT	/books/upload/{id}/	Update a book
DELETE	/books/upload/{id}/	Delete a book

Reading List

Method	Endpoint	Description
POST	/books/readinglist	Create new reading list
GET	/books/readinglist	List users reading lists
PUT	/books/readinglist/{id}/	Update reading list
DELETE	/books/{id}/	Delete a reading list

Reading List Items

Method	Endpoint	Description
POST	/books/readingitem/{id}/	Add new book to list
GET	/books/readingitem/{id}/	List users reading books
PATCH	/books/readingitem/{id}/	Update reading list order
DELETE	/books/readingitem/{id}/	Delete a book from reading list



📁 Folder Structure (Suggested)
book_management/
└─book/
  │
  ├── users/
  │   ├── models.py
  │   ├── serializers.py
  │   ├── views.py
  │   └── urls.py
  │
  ├── books/
  │   ├── models.py
  │   ├── serializers.py
  │   ├── views.py
  │   └── urls.py
  │
  ├── requirements.txt
  ├── manage.py
  └── README.md
  




### 📂 sample env strcture


SECRET_KEY = ''
DEBUG = True
DATABASES_NAME=''
DATABASES_HOST=127.0.0.1
DATABASES_PORT= ''
DATABASES_USER =''
DATABASES_PASSWORD=' '
CLOUDINARY_API_KEY=''
CLOUDINARY_SECRET_KEY=''
CLOUD_NAME=' '
