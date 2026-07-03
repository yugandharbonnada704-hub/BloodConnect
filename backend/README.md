# Blood Donor Management System Backend

A professional, modular, secure, and clean Flask backend for a **Blood Donor Management System** built with **Python Flask** and **Supabase**. It is designed specifically for college CSP (Community Service Project) submissions, demonstrations, and vivas.

---

## Tech Stack
- **Python Flask**: Core web framework utilizing App Factories and Blueprints.
- **Supabase Authentication**: Secure token-based user signups, signins, verification, and email confirmation workflows.
- **Supabase PostgreSQL**: Database layer storing profiles, locations lookup, request logs, and donation history.
- **Flask-CORS**: Cross-Origin Resource Sharing handling for smooth frontend integration.
- **python-dotenv**: Local environment variables manager.
- **Gunicorn / Waitress**: Production-ready WSGI servers.

---

## Directory Structure

```
backend/
├── app/
│   ├── __init__.py           # Flask Application Factory & Middleware Registry
│   ├── config.py             # Configuration loader and environment validator
│   ├── middleware.py         # JWT security validation & RBAC (Role-Based Access Control)
│   ├── routes/               # Modular Routing Layer
│   │   ├── __init__.py
│   │   ├── auth.py           # User Register, Login, Recovery & Logout endpoints
│   │   ├── donor.py          # Profiles, Availability toggles, and Donation logs
│   │   ├── search.py         # Verified Donor search & Hierarchical location queries
│   │   ├── request.py        # Patient blood request creation, updates & lifecycle
│   │   └── admin.py          # Analytics dashboard, user verification, request approval
│   ├── services/             # Core Service Layer
│   │   ├── __init__.py
│   │   ├── supabase_service.py # Supabase Python Client initializer
│   │   ├── email_service.py  # SMTP and Mock email manager (system events)
│   │   └── location_service.py # Hierarchical location database retriever
│   └── utils/                # Utility Module
│       ├── __init__.py
│       ├── helpers.py        # Standardized API response formatters
│       └── validators.py     # Age, email, phone number & profile validator constraint rules
├── tests/
│   └── test_api.py           # Unit tests covering full API surface using mock tokens
├── .env.example              # Template config file
├── .env                      # Local environment configurations (ignored in git)
├── requirements.txt          # Python package dependencies
├── run.py                    # Server startup script
└── schema.sql                # Supabase database initialization script
```

---

## Setup & Installation

### 1. Supabase Database Configuration
1. Go to your **Supabase Dashboard** -> **SQL Editor**.
2. Copy the contents of [`schema.sql`](file:///c:/Users/karth/OneDrive/Desktop/POTTI/backend/schema.sql) and paste them into a new query tab.
3. Run the query. This will create:
   - Tables (`profiles`, `locations`, `blood_requests`, `blood_request_status_history`, `donation_history`).
   - Enable Row Level Security (RLS) on all tables.
   - Insert dummy location lookup values for Indian regions (States, Districts, Cities, Villages).
   - Configure a database function and **PostgreSQL trigger** that automatically inserts a profile row into `public.profiles` whenever a new user signs up via Supabase Auth.

### 2. Local Environment Setup
1. Open a terminal in the `backend` folder:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install package dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in your Supabase credentials:
   ```bash
   cp .env.example .env
   ```
   *Note: Set the `SUPABASE_KEY` to the **service_role** key to allow the Flask backend to bypass Row Level Security (RLS) and securely query database data on behalf of authenticated clients.*

---

## Running the Application

### Running Local Development Server
Execute `run.py` to start the local development server:
```bash
python run.py
```
By default, the server runs on `http://127.0.0.1:5000/`. You can perform a health check by visiting `http://127.0.0.1:5000/health`.

### Running Unit Tests
To run the automated API testing suite:
```bash
python -m unittest discover -s tests
```
*Note: The test suite runs automatically under mock conditions without making network calls to a live Supabase server.*

---

## API Documentation

### 1. Authentication (`/api/auth`)

#### Register User
- **Endpoint**: `POST /api/auth/register`
- **Request Body**:
  ```json
  {
    "full_name": "Karthik Potti",
    "email": "karthik@example.com",
    "phone_number": "+919876543210",
    "password": "SecurePassword123"
  }
  ```
- **Response (201 Created)**:
  ```json
  {
    "status": "success",
    "message": "Registration successful. Verification email has been sent.",
    "data": {
      "id": "user-uuid-string",
      "email": "karthik@example.com",
      "role": "donor"
    }
  }
  ```

#### Login User
- **Endpoint**: `POST /api/auth/login`
- **Request Body**:
  ```json
  {
    "email": "karthik@example.com",
    "password": "SecurePassword123"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "status": "success",
    "message": "Login successful.",
    "data": {
      "access_token": "supabase-jwt-access-token-string",
      "user": {
        "id": "user-uuid-string",
        "email": "karthik@example.com",
        "role": "donor"
      }
    }
  }
  ```
  *Note: Login will fail with HTTP 403 if the email has not been verified yet.*

#### Request Password Recovery
- **Endpoint**: `POST /api/auth/forgot-password`
- **Request Body**:
  ```json
  {
    "email": "karthik@example.com"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "status": "success",
    "message": "Password reset email has been sent."
  }
  ```

#### Reset Password (Authorized)
- **Endpoint**: `POST /api/auth/reset-password`
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "password": "NewSecurePassword456"
  }
  ```

---

### 2. Donor Profile Management (`/api/donors`)

#### Get Current Profile
- **Endpoint**: `GET /api/donors/profile`
- **Headers**: `Authorization: Bearer <access_token>`

#### Update Profile Details
- **Endpoint**: `PUT /api/donors/profile`
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "full_name": "Karthik Potti",
    "age": 22,
    "gender": "Male",
    "blood_group": "O+",
    "phone_number": "+919876543210",
    "state": "Maharashtra",
    "district": "Mumbai",
    "city": "Mumbai",
    "village": "Worli",
    "address": "Flat 402, Worli Heights"
  }
  ```

#### Update Availability Status
- **Endpoint**: `PUT /api/donors/availability`
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "availability_status": "Available"
  }
  ```
  *(Options: `Available`, `Not Available`)*

#### Log Donation Event
- **Endpoint**: `POST /api/donors/donations`
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "donation_date": "2026-06-01",
    "hospital_name": "Lilavati Hospital",
    "units_donated": 1,
    "donation_type": "Voluntary",
    "notes": "Felt great, healthy screening."
  }
  ```

#### Get Donor Dashboard Stats
- **Endpoint**: `GET /api/donors/dashboard`
- **Headers**: `Authorization: Bearer <access_token>`
- **Response (200 OK)**:
  ```json
  {
    "status": "success",
    "message": "Donor dashboard stats retrieved.",
    "data": {
      "profile_status": "verified",
      "availability_status": "Available",
      "donation_count": 3,
      "donation_history": [...]
    }
  }
  ```

---

### 3. Public Searches (`/api/search`)

#### Find Verified Donors
- **Endpoint**: `GET /api/search/donors`
- **Query Parameters**: `blood_group`, `state`, `district`, `city`, `village`, `availability_status` (All optional)
- **Response**: Returns only verified donor profiles, sorted with `Available` donors first.

#### Fetch States
- **Endpoint**: `GET /api/search/locations/states`

#### Fetch Districts in State
- **Endpoint**: `GET /api/search/locations/districts?state=Maharashtra`

---

### 4. Blood Request Management (`/api/requests`)

#### Create Blood Request
- **Endpoint**: `POST /api/requests`
- **Headers**: `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "patient_name": "Ramesh Potti",
    "blood_group": "A+",
    "hospital_name": "Apollo Hospital",
    "state": "Maharashtra",
    "district": "Mumbai",
    "city": "Mumbai",
    "village": "Worli",
    "contact_number": "+919988776655",
    "units_required": 2,
    "urgency_level": "Critical"
  }
  ```
  *(Urgency levels: `Critical`, `High`, `Medium`, `Low`)*

#### List/Filter Requests
- **Endpoint**: `GET /api/requests`
- **Query Parameters**: `blood_group`, `state`, `city`, `status`

#### Cancel Request
- **Endpoint**: `PUT /api/requests/<request_id>/cancel`
- **Headers**: `Authorization: Bearer <access_token>`

---

### 5. Admin Panel Operations (`/api/admin`)

#### Admin Dashboard Analytics
- **Endpoint**: `GET /api/admin/dashboard`
- **Headers**: `Authorization: Bearer <admin_access_token>`
- **Response (200 OK)**:
  ```json
  {
    "status": "success",
    "message": "Admin dashboard stats retrieved.",
    "data": {
      "total_users": 150,
      "total_donors": 120,
      "verified_donors": 95,
      "available_donors": 72,
      "pending_verifications": 15,
      "total_requests": 34,
      "pending_requests": 12,
      "fulfilled_requests": 18
    }
  }
  ```

#### Review & Verify Donor Profile
- **Endpoint**: `PUT /api/admin/donors/<donor_id>/verify`
- **Headers**: `Authorization: Bearer <admin_access_token>`
- **Request Body**:
  ```json
  {
    "verification_status": "verified"
  }
  ```
  *(Options: `verified`, `rejected`, `pending`)*
  *Note: Approving or rejecting triggers an email notification to the donor's address.*

#### Update Request Status (Lifecycle)
- **Endpoint**: `PUT /api/admin/requests/<request_id>/status`
- **Headers**: `Authorization: Bearer <admin_access_token>`
- **Request Body**:
  ```json
  {
    "status": "Fulfilled",
    "notes": "Verified donor completed donation at hospital."
  }
  ```
  *(Options: `Pending`, `Approved`, `Fulfilled`, `Cancelled`)*
  *Note: Updates are logged to status history and email notification is sent to the request owner.*
