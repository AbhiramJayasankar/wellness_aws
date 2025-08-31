# Eye Tracker - Cross Platform Desktop App

## GDPR Compliance

This application implements comprehensive GDPR (General Data Protection Regulation) compliance features to protect user privacy and data rights.

### Backend Implementation (backend/backend_postgres.py)

The FastAPI backend includes the following GDPR compliance endpoints:

#### Right to Data Portability
- **Endpoint**: `GET /user/export`
- **Description**: Allows users to export all their personal data in JSON format
- **Includes**: User account information, all session data, and summary statistics
- **Format**: Structured JSON with timestamp for audit purposes

#### Right to Erasure (Right to be Forgotten)
- **Delete Sessions**: `DELETE /user/sessions`
  - Permanently removes all eye tracking sessions for the user
  - Maintains user account while clearing all session history
  - Returns count of deleted sessions for confirmation

- **Delete Account**: `DELETE /user`
  - Complete account deletion including all associated data
  - Removes user account and all related sessions (respects foreign key constraints)
  - Irreversible operation with proper cascade deletion

### Frontend Implementation (webpage/index.html)

The web dashboard provides user-friendly GDPR controls:

#### Data Management Section
- **Export Your Data**: Download complete data export in JSON format
- **Delete Sessions**: Clear all eye tracking history while preserving account
- **Delete Account**: Complete account removal with multiple confirmation steps

#### User Experience Features
- Multi-step confirmation for destructive actions
- Clear warnings about irreversible operations
- Immediate feedback on successful operations
- Automatic dashboard refresh after data modifications

#### Security Measures
- JWT token authentication for all GDPR operations
- Confirmation prompts with typed verification for account deletion
- User must type "DELETE" to confirm account removal
- Clear distinction between session deletion and account deletion

### GDPR Rights Addressed
1. **Right to Access**: Users can view all their data through the dashboard
2. **Right to Data Portability**: Complete data export functionality
3. **Right to Rectification**: Users can manage their account information
4. **Right to Erasure**: Granular deletion options (sessions only or complete account)
5. **Data Minimization**: Only necessary data is collected and stored
6. **Consent**: Clear user interface for data management decisions

## Security

### Current Security Implementation (backend/backend_postgres.py)

#### Authentication & Authorization
- **JWT Token Authentication**: Secure token-based authentication using HS256 algorithm
  - 24-hour token expiration for session security
  - Proper token verification with error handling for expired/invalid tokens
- **Password Security**: SHA256 hashing for password storage (lines 65-66)
- **Bearer Token Protection**: All sensitive endpoints protected with HTTPBearer security

#### Database Security
- **Environment Variables**: Database credentials stored in `.env` file, not hardcoded
- **SQL Injection Prevention**: Parameterized queries using psycopg2 with `%s` placeholders
- **Connection Management**: Proper database connection handling with context managers

#### API Security
- **CORS Configuration**: Currently allows all origins (line 26) - acceptable for development
- **Input Validation**: Pydantic models for request validation
- **Error Handling**: Structured error responses without exposing sensitive information

### Security Improvements Planned (Given More Time)

#### Enhanced Password Security
- **Upgrade to bcrypt/scrypt**: Replace SHA256 with more secure password hashing algorithms
- **Salt Implementation**: Add unique salts for each password hash
- **Password Strength Requirements**: Implement minimum complexity requirements

#### Advanced Authentication
- **Multi-Factor Authentication (MFA)**: Add TOTP/SMS-based 2FA
- **Refresh Tokens**: Implement refresh token rotation for better session management
- **Rate Limiting**: Add request rate limiting to prevent brute force attacks
- **Account Lockout**: Temporary lockout after failed login attempts

#### Infrastructure Security
- **HTTPS Enforcement**: Ensure all communications are encrypted in production
- **CORS Hardening**: Restrict allowed origins to specific domains in production
- **Security Headers**: Add security headers (HSTS, CSP, X-Frame-Options)
- **Input Sanitization**: Enhanced input validation and sanitization

#### Database Security
- **Database Connection Encryption**: SSL/TLS for database connections
- **Database User Permissions**: Principle of least privilege for database user
- **Audit Logging**: Comprehensive logging of all database operations
- **Backup Encryption**: Encrypted database backups

#### Monitoring & Compliance
- **Security Monitoring**: Real-time security event monitoring
- **Penetration Testing**: Regular security assessments
- **Compliance Audits**: Regular GDPR and security compliance reviews
- **Incident Response Plan**: Documented security incident procedures

## High-Level Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                          Eye Tracker System                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐              ┌─────────────────┐              │
│  │   Desktop App   │              │   Web Frontend  │              │
│  │  (main_app.py)  │              │ (index.html)    │              │
│  │                 │              │                 │              │
│  │  • Eye Tracking │              │  • User Auth    │              │
│  │  • Real-time    │              │  • Dashboard    │              │
│  │  • Session Data │              │  • GDPR Tools   │              │
│  │  • System Tray  │              │  • Data Viz     │              │
│  └─────────┬───────┘              └─────────┬───────┘              │
│            │                                │                      │
│            │           HTTP/REST API        │                      │
│            └────────────────┬───────────────┘                      │
│                             │                                      │
│                             ▼                                      │
│                  ┌─────────────────┐                               │
│                  │   Backend API   │                               │
│                  │(backend_postgres│                               │
│                  │    .py)         │                               │
│                  │                 │                               │
│                  │  • JWT Auth     │                               │
│                  │  • REST Endpoints│                              │
│                  │  • GDPR APIs    │                               │
│                  │  • Session Mgmt │                               │
│                  └─────────┬───────┘                               │
│                            │                                       │
│                            │ SQL Queries                           │
│                            ▼                                       │
│          ┌─────────────────────────────────────────────┐           │
│          │                PostgreSQL RDS              │           │
│          │                                             │           │
│          │  • Users table (auth data, GDPR compliance)│           │
│          │  • Sessions table (eye tracking data)      │           │
│          │  • Foreign key constraints for data integrity│         │
│          │  • Only accessible via Backend API         │           │
│          └─────────────────────────────────────────────┘           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

1. **Desktop Application (app/main_app.py)**
   - Built with PySide6 for cross-platform GUI
   - Uses OpenCV + MediaPipe for real-time eye tracking
   - Authenticates with backend using JWT tokens
   - Sends session data to backend on app close
   - Packaged as standalone executable using PyInstaller (main_app.spec)

2. **Web Frontend (webpage/index.html)**
   - Single-page application with vanilla JavaScript
   - Responsive design with glassmorphism UI
   - Handles user authentication (login/register)
   - Provides data visualization and session management
   - Implements GDPR compliance controls (export/delete data)
   - Hosted on Vercel for global CDN distribution

3. **Backend API (backend/backend_postgres.py)**
   - FastAPI REST API with automatic OpenAPI documentation
   - JWT-based authentication with token expiration
   - PostgreSQL database with RDS for scalability
   - GDPR compliance endpoints (export, delete sessions, delete account)
   - Deployed on AWS EC2 with RDS database

### Deployment Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Device   │    │   Vercel CDN    │    │   AWS Cloud     │
│                 │    │                 │    │                 │
│  Desktop App ───┼────┼─── Web App ─────┼────┼─── EC2 + RDS   │
│  (PyInstaller)  │    │  (index.html)   │    │  (FastAPI +     │
│                 │    │                 │    │   PostgreSQL)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Test Cases for CI Pipeline

### 1. Backend API Tests (backend/backend_postgres.py)

#### Authentication Tests
```python
def test_user_registration():
    # Test valid user registration
    # Test duplicate username/email rejection
    # Test password hashing

def test_user_login():
    # Test valid login credentials
    # Test invalid credentials rejection
    # Test JWT token generation

def test_jwt_token_validation():
    # Test valid token authentication
    # Test expired token rejection
    # Test invalid token rejection
```

#### GDPR Compliance Tests
```python
def test_user_data_export():
    # Test complete data export functionality
    # Verify all user data is included
    # Test export timestamp generation

def test_session_deletion():
    # Test deletion of all user sessions
    # Verify user account remains intact
    # Test deletion count accuracy

def test_account_deletion():
    # Test complete account deletion
    # Verify cascade deletion of sessions
    # Test referential integrity
```

#### Database Tests
```python
def test_database_connection():
    # Test PostgreSQL connection establishment
    # Test connection pooling
    # Test connection error handling

def test_sql_injection_protection():
    # Test parameterized queries
    # Verify no SQL injection vulnerabilities
    # Test input sanitization
```

### 2. Frontend Tests (webpage/index.html)

#### UI Functionality Tests
```javascript
describe('Authentication Flow', () => {
    test('login form validation', () => {
        // Test required field validation
        // Test form submission
        // Test error message display
    });

    test('registration form validation', () => {
        // Test email format validation
        // Test password requirements
        // Test form submission
    });
});

describe('Dashboard Features', () => {
    test('session data display', () => {
        // Test data loading and rendering
        // Test empty state handling
        // Test statistics calculation
    });

    test('GDPR compliance controls', () => {
        // Test data export functionality
        // Test session deletion confirmation
        // Test account deletion workflow
    });
});
```

#### Security Tests
```javascript
describe('Security Measures', () => {
    test('token storage and handling', () => {
        // Test localStorage token management
        // Test automatic token cleanup
        // Test authentication header inclusion
    });

    test('XSS protection', () => {
        // Test input sanitization
        // Test content security policy
        // Test DOM manipulation safety
    });
});
```

### 3. Desktop Application Tests (app/main_app.py)

#### Core Functionality Tests
```python
def test_eye_tracker_initialization():
    # Test camera detection and initialization
    # Test MediaPipe model loading
    # Test configuration validation

def test_session_data_collection():
    # Test blink detection accuracy
    # Test session timing
    # Test data aggregation

def test_backend_integration():
    # Test authentication with backend
    # Test session data transmission
    # Test network error handling
```

#### PyInstaller Build Tests
```python
def test_executable_creation():
    # Test main_app.spec configuration
    # Verify all dependencies are included
    # Test icon and resource embedding

def test_cross_platform_compatibility():
    # Test Windows executable
    # Test macOS application bundle
    # Test Linux AppImage/binary
```

### 4. Integration Tests

#### End-to-End User Flow
```python
def test_complete_user_journey():
    # Register new user via web frontend
    # Login to desktop application
    # Record eye tracking session
    # View session data on web dashboard
    # Export user data (GDPR compliance)
    # Delete account and verify data removal

def test_cross_platform_data_sync():
    # Create session on desktop app
    # Verify data appears on web dashboard
    # Test real-time synchronization
```

#### Performance Tests
```python
def test_api_response_times():
    # Test authentication endpoints (< 200ms)
    # Test data retrieval endpoints (< 500ms)
    # Test GDPR export endpoints (< 2000ms)

def test_desktop_app_performance():
    # Test real-time eye tracking (30 FPS)
    # Test memory usage over time
    # Test CPU usage optimization
```

### 5. Security Tests

#### Vulnerability Assessment
```python
def test_authentication_security():
    # Test password hashing strength
    # Test JWT token security
    # Test session management

def test_data_protection():
    # Test GDPR compliance implementation
    # Test data encryption at rest
    # Test secure data transmission
```

### CI Pipeline Configuration

```yaml
# Example GitHub Actions workflow
name: Eye Tracker CI/CD
on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: pip install -r backend/requirements.txt
      - name: Run backend tests
        run: pytest backend/tests/

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node.js
        uses: actions/setup-node@v2
      - name: Run frontend tests
        run: npm test

  desktop-app-tests:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: pip install -r app/requirements.txt
      - name: Run app tests
        run: pytest app/tests/
      - name: Build executable
        run: pyinstaller app/main_app.spec

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Security vulnerability scan
        run: |
          # SAST tools for code analysis
          # Dependency vulnerability scanning
          # GDPR compliance verification
```