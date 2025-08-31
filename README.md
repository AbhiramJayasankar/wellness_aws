# Wellness Simple

```
╔═════════════════════════════════════════════════════════════════════════╗
║                           Eye Tracker System                            ║
╠═════════════════════════════════════════════════════════════════════════╣
║                                                                         ║
║    ╭─────────────────────────╮      ╭─────────────────────────╮         ║
║    │      Desktop App        │      │     Web Frontend        │         ║
║    │     (main_app.py)       │      │     (index.html)        │         ║
║    │                         │      │                         │         ║
║    │  Eye Tracking           │      │  User Authentication    │         ║
║    │  Real-time Analysis     │      │  Interactive Dashboard  │         ║
║    │  Session Management     │      │  GDPR Compliance Tools  │         ║
║    │  System Tray Control    │      │  Data Visualization     │         ║
║    ╰───────────┬─────────────╯      ╰───────────┬─────────────╯         ║
║                │                                │                       ║
║                │                                │                       ║
║                └─────────► HTTP/REST API ◄──────┘                       ║
║                                  │                                      ║
║                                  ▼                                      ║
║                ╭───────────────────────────────────╮                    ║
║                │      Backend API Server           │                    ║
║                │    (backend_postgres.py)          │                    ║
║                │         AWS EC2                   │                    ║
║                │                                   │                    ║
║                │      JWT Authentication           │                    ║
║                │      RESTful Endpoints            │                    ║
║                │      GDPR Compliance APIs         │                    ║
║                │      Session Lifecycle Mgmt       │                    ║
║                ╰─────────────────┬─────────────────╯                    ║
║                                  │                                      ║
║                                  │ SQL Queries                          ║
║                                  ▼                                      ║
║        ╔═══════════════════════════════════════════════╗                ║
║        ║            PostgreSQL RDS                     ║                ║
║        ║                                               ║                ║
║        ║  users        - Authentication & GDPR         ║                ║
║        ║  sessions     - Eye tracking metrics          ║                ║
║        ║  constraints  - Data integrity rules          ║                ║
║        ║  security    - API-only access                ║                ║
║        ╚═══════════════════════════════════════════════╝                ║
║                                                                         ║
╚═════════════════════════════════════════════════════════════════════════╝
```

## Setup

```bash
git clone https://github.com/AbhiramJayasankar/wellness_aws
cd wellness_ssimple
cd app
python -m venv venv
pip install -r requirements.txt
python main_app.py
```

## Build Executable

```bash
cd wellness_ssimple
cd app
pyinstaller main_app.spec
```

Executable will be in `app/dist/` directory.

## App Structure

```
wellness_ssimple/
├── app/                    # Desktop Application
│   ├── main_app.py        # Main GUI application
│   ├── main_app.spec      # PyInstaller build spec
│   ├── config.py          # Configuration settings
│   ├── eye_tracker.py     # Eye tracking logic
│   ├── video_capture.py   # Camera interface
│   ├── login.py           # Login widget
│   ├── register.py        # Registration widget
│   ├── requirements.txt   # Python dependencies
│   └── dist/              # Built executable
│
├── backend/               # API Backend
│   ├── backend_postgres.py # FastAPI server
│   └── .env              # Environment variables
│
├── webpage/              # Web Frontend
│   └── index.html        # Dashboard interface
│
│ Live Demo: https://eyetracker-dashboard.vercel.app/
│
└── README.md            # This file
```

## Security

**Authentication & Authorization:**
- JWT token-based authentication with 24-hour expiration
- SHA-256 password hashing
- Bearer token verification for protected endpoints

**Database Security:**
- Parameterized queries prevent SQL injection
- Foreign key constraints for data integrity
- User isolation - users access only their own data

**GDPR Compliance:**
- Data export, session deletion, and account deletion endpoints
- Multiple confirmation prompts for destructive actions
- Consent required before account creation

**Web Security:**
- CORS middleware configured
- Environment variables for sensitive configuration
- Input validation on forms
- Proper session cleanup and network timeouts

## Test Cases for CI Pipeline

**Authentication Tests:**
- User registration with valid/invalid data
- User login with correct/incorrect credentials
- JWT token validation and expiration
- Password hashing verification

**API Endpoint Tests:**
- Session creation and retrieval
- User data access with/without authentication
- GDPR compliance endpoints (export, delete sessions, delete account)
- Database connection and query validation

**Security Tests:**
- SQL injection prevention validation
- Unauthorized access attempts
- Token manipulation tests
- CORS policy verification

**Integration Tests:**
- Desktop app to backend API communication
- Web frontend to backend API integration
- Database schema integrity checks
- Error handling and logging validation