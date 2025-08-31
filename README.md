# Eye Tracker - Cross Platform Desktop App

A comprehensive eye tracking application with real-time blink detection, web dashboard, and GDPR-compliant data management.

## 🚀 Quick Start Guide

### For End Users

#### 1. **Download & Install Desktop App**
- Download the latest release for your platform (Windows/macOS/Linux)
- Run the executable - no installation required
- Grant camera permissions when prompted

#### 2. **Create Account**
- Launch the app and click "Sign up"
- Enter username, email, and password
- You'll be automatically logged in

#### 3. **Start Eye Tracking**
- Position yourself in front of your camera
- The app will automatically detect and track your blinks
- Session data is recorded in real-time
- Use system tray to minimize/hide the app

#### 4. **View Your Data**
- Visit the web dashboard at [your-frontend-url]
- Login with the same credentials
- View session history, statistics, and analytics
- Export or delete your data (GDPR compliance)

### For Developers

#### 1. **Clone Repository**
```bash
git clone https://github.com/your-username/wellness_ssimple.git
cd wellness_ssimple
```

#### 2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python backend_postgres.py
```

#### 3. **Frontend Setup**
```bash
cd webpage
# Open index.html in browser or serve with local server
python -m http.server 3000
```

#### 4. **Desktop App Setup**
```bash
cd app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main_app.py
```

#### 5. **Build Executable**
```bash
cd app
pyinstaller main_app.spec
# Find executable in dist/ folder
```

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

## CI/CD Deployment Architecture

### Current Deployment Setup

The project uses a multi-platform CI/CD approach:

#### 🌐 **Frontend CI/CD (Vercel)**
- **Platform**: Vercel (automatic deployments)
- **Trigger**: Git push to main branch
- **Process**: 
  - Automatic build and deployment of `webpage/index.html`
  - Global CDN distribution
  - Preview deployments for pull requests
  - Custom domain support with HTTPS

#### 🚀 **Backend CI/CD (AWS EC2)**
- **Platform**: AWS EC2 with simple deployment script
- **Trigger**: Cron job or manual execution
- **Process**:
  - Simple script checks if HEAD of main branch is new
  - If new commits detected, pulls latest code from repository
  - Restarts FastAPI application
  - Basic health verification

#### 📦 **Desktop App Distribution**
- **Build Process**: PyInstaller with `main_app.spec`
- **Platforms**: Windows, macOS, Linux
- **Distribution**: Manual releases or automated GitHub Actions

### Current Simple Deployment Script (EC2)

Your actual backend deployment uses a simple script that runs on EC2:

```bash
#!/bin/bash
# Simple deployment script running on EC2
# File: /opt/eye-tracker-backend/deploy.sh

set -e  # Exit on any error

# Configuration
REPO_DIR="/opt/eye-tracker-backend"
REPO_URL="https://github.com/your-username/wellness_ssimple.git"
BRANCH="main"
SERVICE_NAME="eye-tracker-backend"

# Function to get current HEAD
get_current_head() {
    git ls-remote origin $BRANCH | cut -f1
}

# Function to get local HEAD
get_local_head() {
    cd $REPO_DIR
    git rev-parse HEAD
}

# Main deployment logic
echo "Checking for updates..."

# Get remote and local HEAD
REMOTE_HEAD=$(get_current_head)
LOCAL_HEAD=$(get_local_head)

echo "Remote HEAD: $REMOTE_HEAD"
echo "Local HEAD:  $LOCAL_HEAD"

# Compare HEADs
if [ "$REMOTE_HEAD" != "$LOCAL_HEAD" ]; then
    echo "New commits detected. Starting deployment..."
    
    # Navigate to repo directory
    cd $REPO_DIR
    
    # Pull latest changes
    echo "Pulling latest changes..."
    git pull origin $BRANCH
    
    # Install/update dependencies
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -r backend/requirements.txt
    
    # Restart the service
    echo "Restarting FastAPI service..."
    sudo systemctl restart $SERVICE_NAME
    
    # Basic health check
    echo "Waiting for service to start..."
    sleep 5
    
    # Check if service is running
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Deployment successful! Service is healthy."
    else
        echo "❌ Deployment failed! Service health check failed."
        exit 1
    fi
    
    echo "Deployment completed successfully!"
else
    echo "No new commits. Nothing to deploy."
fi
```

### Cron Job Setup

The script runs automatically via cron job:

```bash
# Crontab entry (runs every 5 minutes)
# crontab -e
*/5 * * * * /opt/eye-tracker-backend/deploy.sh >> /var/log/eye-tracker-deploy.log 2>&1
```

### Systemd Service Configuration

```ini
# /etc/systemd/system/eye-tracker-backend.service
[Unit]
Description=Eye Tracker Backend API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/eye-tracker-backend/backend
Environment=PATH=/opt/eye-tracker-backend/venv/bin
ExecStart=/opt/eye-tracker-backend/venv/bin/python -m uvicorn backend_postgres:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### Test Structure Organization

```
project/
├── backend/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py              # pytest fixtures
│   │   ├── test_auth.py             # Authentication tests
│   │   ├── test_gdpr.py             # GDPR compliance tests
│   │   ├── test_database.py         # Database tests
│   │   ├── test_security.py         # Security tests
│   │   └── test_api_endpoints.py    # API endpoint tests
│   └── requirements-test.txt        # Test dependencies
│
├── webpage/
│   ├── tests/
│   │   ├── auth.test.js            # Authentication tests
│   │   ├── dashboard.test.js       # Dashboard functionality
│   │   ├── gdpr.test.js            # GDPR compliance tests
│   │   └── security.test.js        # Security tests
│   ├── package.json                # Test scripts and dependencies
│   └── jest.config.js              # Jest configuration
│
├── app/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_eye_tracker.py     # Eye tracking tests
│   │   ├── test_ui.py              # UI component tests
│   │   ├── test_integration.py     # Backend integration tests
│   │   └── test_build.py           # PyInstaller build tests
│   └── requirements-test.txt       # Test dependencies
│
├── tests/
│   ├── integration/                # End-to-end integration tests
│   │   ├── test_user_journey.py    # Complete user flow tests
│   │   ├── test_data_sync.py       # Cross-platform data sync tests
│   │   └── test_performance.py     # Performance tests
│   └── scripts/
│       ├── gdpr_compliance_check.py
│       └── deploy_health_check.py
│
└── .github/
    └── workflows/
        ├── ci-cd.yml               # Main CI/CD pipeline
        ├── security-scan.yml       # Security scanning
        └── performance-test.yml    # Performance testing
```

### Optional: Enhanced GitHub Actions CI/CD

If you want to upgrade from your simple script to full GitHub Actions CI/CD in the future, here's a sample structure:

<details>
<summary>Click to expand GitHub Actions configuration</summary>

```yaml
name: Eye Tracker CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: test_eyetracker
    
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
          pip install pytest
      - name: Run tests
        run: |
          cd backend
          pytest tests/
  
  deploy-backend:
    needs: backend-tests
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Deploy to EC2
        uses: appleboy/ssh-action@v0.1.5
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ${{ secrets.EC2_USERNAME }}
          key: ${{ secrets.EC2_PRIVATE_KEY }}
          script: |
            cd /opt/eye-tracker-backend
            ./deploy.sh
```

</details>