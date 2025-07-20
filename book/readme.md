# 📚 Book Management System - Django REST API

A RESTful API built using Django and Django REST Framework to manage users, books, and personalized reading lists.

---

## ✨ Features

### 👤 User Management
- User registration with email and username (both unique)
- Secure login using token-based authentication (JWT recommended)
- User profile management (update profile details)

### 📘 Book Management
- Authenticated users can:
  - Create, update, and delete books
  - Upload books with title, author(s), genre, publication date, and optional description
- All users can view all available books

### 📂 Reading List
- Users can:
  - Create and manage multiple reading lists
  - Add books to their reading lists in a preferred order
  - Remove books from reading lists

### ⚙️ Error Handling
- Well-structured validation and error messages
- Returns meaningful HTTP status codes and error responses

---

## 🛠️ Tech Stack

- **Backend**: Django, Django REST Framework
- **Authentication**: JWT or Token Authentication (via `djangorestframework-simplejwt` or DRF tokens)
- **Database**: SQLite (dev), PostgreSQL (prod-ready)
- **Serialization**: Django REST Framework Serializers
- **Image Uploads**: Django `ImageField` with proper media handling

---

## 📦 Installation

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/book-management.git
cd book-management

2. Create virtual environment and activate it

    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Apply migrations
bash
Copy
Edit
python manage.py migrate
5. Run the server
bash
Copy
Edit
python manage.py runserver
🔐 API Authentication
This project uses token-based authentication (you can switch to JWT).

Obtain token:

bash
Copy
Edit
POST /api/token/
{
  "email": "user@example.com",
  "password": "yourpassword"
}
Use the token in headers for authenticated requests:

makefile
Copy
Edit
Authorization: Bearer <your_token>
🔀 API Endpoints (Sample)
Users
Method	Endpoint	Description
POST	/users/signup/	Register new user
POST	/users/login/	Login and get token
GET	/users/me/	Get current user info
PUT	/users/me/	Update profile

Books
Method	Endpoint	Description
GET	/books/	List all books
POST	/books/	Create a new book
PUT	/books/{id}/	Update a book
DELETE	/books/{id}/	Delete a book

Reading List
Method	Endpoint	Description
POST	/reading-lists/	Create new reading list
GET	/reading-lists/	List user's reading lists
PUT	/reading-lists/{id}/	Update reading list name
DELETE	/reading-lists/{id}/	Delete a reading list
POST	/reading-lists/{id}/add/	Add a book to reading list
POST	/reading-lists/{id}/remove/	Remove book from list

📁 Folder Structure (Suggested)
bash
Copy
Edit
book_management/
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
├── readinglists/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── media/
├── requirements.txt
├── manage.py
└── README.md