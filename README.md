# Blink Tracker

A comprehensive blink detection and tracking application with real-time monitoring, user authentication, and web dashboard.

## 🌐 Live Demo

**Website**: [https://eyetracker-dashboard.vercel.app/](https://eyetracker-dashboard.vercel.app/)

## 📋 Overview

Blink Tracker is a full-stack application that uses computer vision to detect and track eye blinks in real-time. The system consists of:

- **Desktop Application**: Real-time blink detection using MediaPipe
- **Backend API**: FastAPI-based REST API with PostgreSQL database
- **Web Dashboard**: Modern React-style web interface for data visualization
- **Cloud Infrastructure**: AWS EC2 + RDS deployment with CI/CD

## 🏗️ Architecture

### High-Level System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Desktop App   │    │   Web Dashboard │    │   CI/CD Pipeline│
│   (Python/CV)   │    │   (HTML/JS/CSS) │    │   (GitHub)      │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          │ HTTP/REST API        │ HTTP/REST API        │ Auto Deploy
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                         ┌───────▼───────┐
                         │  Backend API  │
                         │  (FastAPI)    │
                         │  on EC2       │
                         └───────┬───────┘
                                 │
                         ┌───────▼───────┐
                         │  PostgreSQL   │
                         │  Database     │
                         │  on RDS       │
                         └───────────────┘
```

### Component Interaction Flow

1. **Desktop App** → Captures blinks → Sends data to Backend API
2. **Web Dashboard** → Authenticates users → Displays blink statistics
3. **Backend API** → Validates requests → Stores/retrieves data from PostgreSQL
4. **CI/CD** → Auto-deploys backend to EC2 and frontend to Vercel

## 🚀 Features

### Desktop Application
- Real-time blink detection using MediaPipe
- Session-based tracking
- Automatic data synchronization with backend
- Executable packaging with PyInstaller

### Web Dashboard
- User authentication (register/login)
- Real-time session statistics
- Historical data visualization
- GDPR compliance features
- Responsive modern design

### Backend API
- JWT-based authentication
- RESTful API endpoints
- PostgreSQL database integration
- GDPR data export/deletion
- CORS-enabled for web integration

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- Node.js (for development)
- PostgreSQL database
- AWS account (for deployment)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd wellness_ssimple
   ```

2. **Set up Python environment**
   ```bash
   python -m venv eye
   eye\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create `test/.env` file:
   ```env
   DB_HOST=your-db-host
   DB_NAME=eyedatabase
   DB_USER=eyeuser
   DB_PASSWORD=eyepassword
   DB_PORT=5432
   SECRET_KEY=your-secret-key
   ```

4. **Run the backend**
   ```bash
   cd backend
   python backend_postgres.py
   ```

5. **Open the web dashboard**
   Open `webpage/index.html` in a browser or serve via local server

### PyInstaller Executable Creation

To create a standalone executable from the desktop application:

1. **Navigate to project root**
   ```bash
   cd wellness_ssimple
   ```

2. **Use the spec file from old directory**
   ```bash
   pyinstaller old/main_app.spec
   ```

3. **Requirements for spec file**
   - Ensure `main_app.py` exists in root directory
   - Include `icon.ico` file
   - MediaPipe data files are automatically collected
   - Output will be a single executable file

4. **Spec file configuration**
   ```python
   # Key configurations in main_app.spec:
   - console=False          # No console window
   - upx=True              # Compression enabled
   - icon=['icon.ico']     # Application icon
   - collect_data_files('mediapipe')  # Include MediaPipe assets
   ```

## 🌐 Deployment

### Backend (EC2)
- **Platform**: AWS EC2 instance
- **Database**: AWS RDS PostgreSQL
- **CI/CD**: GitHub Actions
- **Environment**: Production environment variables from `test/.env`

### Frontend (Vercel)
- **Platform**: Vercel hosting
- **Source**: `webpage/index.html`
- **CI/CD**: Auto-deployment on git push
- **URL**: [https://eyetracker-dashboard.vercel.app/](https://eyetracker-dashboard.vercel.app/)

### Database (RDS)
- **Engine**: PostgreSQL
- **Host**: `eyetracker-db.cuzmyoe2kikx.us-east-1.rds.amazonaws.com`
- **Port**: 5432
- **Security**: VPC-secured, encrypted connections

## 🔒 Security Implementation

### Current Security Measures

1. **Authentication & Authorization**
   - JWT tokens with 24-hour expiration
   - Password hashing using SHA-256
   - Bearer token authentication for API endpoints

2. **Database Security**
   - PostgreSQL with encrypted connections
   - Environment variable configuration
   - Input sanitization and parameterized queries

3. **API Security**
   - CORS configuration
   - Request validation with Pydantic models
   - Error handling without information leakage

### Security Improvements (Given More Time)

1. **Enhanced Authentication**
   - Implement bcrypt/Argon2 for password hashing
   - Add refresh tokens for better session management
   - Multi-factor authentication (MFA)
   - Rate limiting and brute force protection

2. **API Security**
   - Input validation and sanitization
   - SQL injection prevention (already partially implemented)
   - API versioning and deprecation strategies
   - Request/response logging and monitoring

3. **Infrastructure Security**
   - SSL/TLS certificates for all endpoints
   - VPN/Private subnets for database access
   - Security groups and firewall configurations
   - Regular security audits and penetration testing

4. **Data Security**
   - Database encryption at rest
   - Backup encryption
   - Data anonymization for development environments
   - Secure key management (AWS KMS)

## 🛡️ GDPR Compliance

### Current Implementation

1. **Data Rights**
   - **Right to Access**: Users can view all their data through the dashboard
   - **Right to Portability**: Export all user data in JSON format
   - **Right to Erasure**: Delete all sessions or entire account
   - **Right to Rectification**: Users can update their account information

2. **Data Processing**
   - Clear purpose limitation (blink tracking for wellness)
   - Data minimization (only necessary blink data collected)
   - Explicit consent through account registration

3. **Web Dashboard Features**
   - "Export Your Data" button - downloads complete data export
   - "Delete Sessions" - removes all tracking data while keeping account
   - "Delete Account" - complete account and data removal
   - Confirmation dialogs for destructive actions

### GDPR Improvements (Given More Time)

1. **Enhanced Consent Management**
   - Granular consent options for different data types
   - Cookie consent banners
   - Consent withdrawal mechanisms
   - Audit trail of consent changes

2. **Privacy by Design**
   - Data Protection Impact Assessments (DPIA)
   - Privacy-preserving analytics
   - Automatic data retention policies
   - Data pseudonymization techniques

3. **Legal Compliance**
   - Privacy policy and terms of service
   - Data Processing Agreements (DPA)
   - Breach notification procedures
   - Regular compliance audits

4. **Technical Measures**
   - Data anonymization for analytics
   - Automated data deletion workflows
   - Enhanced logging for compliance reporting
   - Geographic data residency controls

## 🧪 Testing Strategy

### Proposed Test Cases for CI Pipeline

#### Unit Tests
```python
# Backend API Tests
def test_user_registration():
    """Test user can register with valid credentials"""
    
def test_user_login():
    """Test user can login with correct credentials"""
    
def test_invalid_login():
    """Test login fails with invalid credentials"""
    
def test_token_expiration():
    """Test JWT token expiration handling"""
    
def test_blink_session_creation():
    """Test creation of new blink tracking session"""
    
def test_data_export():
    """Test GDPR data export functionality"""
```

#### Integration Tests
```python
def test_database_connection():
    """Test PostgreSQL database connectivity"""
    
def test_api_authentication_flow():
    """Test complete auth flow from registration to API access"""
    
def test_session_data_persistence():
    """Test blink session data is correctly stored and retrieved"""
```

#### Frontend Tests
```javascript
// Web Dashboard Tests
describe('Authentication', () => {
  test('User can register new account', async () => {});
  test('User can login to existing account', async () => {});
  test('Dashboard displays after successful login', async () => {});
});

describe('GDPR Compliance', () => {
  test('Export data functionality works', async () => {});
  test('Delete sessions removes data', async () => {});
  test('Account deletion works completely', async () => {});
});
```

#### End-to-End Tests
```python
def test_complete_blink_tracking_workflow():
    """Test complete flow from desktop app to web dashboard"""
    
def test_gdpr_data_lifecycle():
    """Test complete GDPR data lifecycle"""
```

### CI/CD Pipeline Configuration

```yaml
# Proposed GitHub Actions workflow
name: Test and Deploy
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run unit tests
        run: pytest tests/unit/
      - name: Run integration tests
        run: pytest tests/integration/
```

## 📊 API Documentation

### Authentication Endpoints
- `POST /register` - User registration
- `POST /login` - User authentication

### User Endpoints
- `GET /user` - Get user profile
- `GET /user/export` - Export user data (GDPR)
- `DELETE /user` - Delete account (GDPR)
- `DELETE /user/sessions` - Delete all sessions (GDPR)

### Session Endpoints
- `GET /sessions` - Get user sessions
- `POST /sessions` - Create new session

## 📁 Project Structure

```
wellness_ssimple/
├── backend/
│   └── backend_postgres.py    # FastAPI backend
├── webpage/
│   └── index.html            # Web dashboard
├── test/
│   └── .env                  # Environment configuration
├── old/
│   └── main_app.spec         # PyInstaller spec file
├── eye/                      # Python virtual environment
└── README.md
```

## 🔧 Configuration

### Environment Variables
```env
# Database
DB_HOST=eyetracker-db.cuzmyoe2kikx.us-east-1.rds.amazonaws.com
DB_NAME=eyedatabase
DB_USER=eyeuser
DB_PASSWORD=eyepassword
DB_PORT=5432

# Security
SECRET_KEY=your-secret-key-here
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation above
- Review the API endpoints for integration help

---

**Built with**: Python, FastAPI, PostgreSQL, MediaPipe, HTML/CSS/JavaScript, AWS EC2/RDS, Vercel