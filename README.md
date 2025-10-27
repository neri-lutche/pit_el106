Django REST Framework JWT Authentication API

This repository contains a backend-focused Django project implementing JWT (JSON Web Token) authentication using Django REST Framework and Simple JWT. The project provides API endpoints for user registration, account verification, login, and accessing a protected resource.

Project Setup Instructions

Follow these steps to get the API server running locally.

1. Prerequisites
    Python (3.8+)
    pip (Python package installer)
    Git
2. Setup
    1. Clone the Repository:
       git clone https://github.com/neri-lutche/pit_el106.git
       cd PIT_EL106_Django_Auth
    2. Create and Activate Virtual Environment (Recommended):
       python -m venv venv
       # For Windows: .\venv\Scripts\activate
       # For macOS/Linux: source venv/bin/activate
    3. Install Dependencies:You will need Django, DRF, and Simple JWT.
       pip install django djangorestframework djangorestframework-simplejwt
    4. Apply Migrations:
       python manage.py makemigrations api
       python manage.py migrate
    5. Run the Server:
       python manage.py runserver
       
🔑 API Endpoint Documentation

The API uses JWT Bearer Tokens for authentication on protected routes. Use a tool like Postman to interact with these endpoints.

Authentication Flow (Using Postman)

1. User Registration (The Signup)

Detail:  Value
Method:  POST
URL:     http://127.0.0.1:8000/api/auth/register/

Body (JSON)
  {
    "username": "apitest",
    "email": "api@example.com",
    "password": "password123",
    "password2": "password123",
    "first_name": "API",
    "last_name": "Test"
  }
  
Expected Result: HTTP 201 Created. Crucial: Check your Django terminal for the email verification link and copy the entire URL.

2. Email Verification (The Activation)

Detail:  Value
Method:  GET
URL:     _Paste the full verification link from the console_
Expected Result: HTTP 200 OK with the message: "Email successfully verified. You can now log in."

3. Login (Token Generation)

Detail:  Value
Method:  POST
URL:     http://127.0.0.1:8000/api/auth/login/

Body (JSON)
  {
    "email": "api@example.com",
    "password": "password123"
  }

Expected Result: HTTP 200 OK with a JSON response containing the access and refresh tokens. Save the access token.
Expected Result: HTTP 200 OK with a JSON response containing the access and refresh tokens. Save the access token.

 Main Project EndpointsEndpoint NameMethodURLAuthenticationAPI RootGET/api/NoneRegistrationPOST/api/auth/register/NoneEmail VerificationGET/api/auth/verify-email/NoneLogin (Token Obtain)POST/api/auth/login/NoneProtected TestGET/api/auth/protected/Required (JWT)
