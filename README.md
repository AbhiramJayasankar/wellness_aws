# Wellness Eye Tracker Application

A desktop application that tracks eye blinks and monitors wellness metrics to promote healthy computer usage habits.

## Features

- Real-time eye tracking and blink detection using computer vision
- User authentication and session management
- System performance monitoring
- Wellness notifications for blink rate
- System tray integration

## GDPR Compliance

### Current Implementation Status

**Completed:**
- Basic user authentication system with secure password hashing
- Session data collection with user consent through registration

**In Progress/Planned:**

### Data We Collect

1. **Account Information**
   - Username
   - Email address
   - Encrypted password hash
   - Account creation timestamp

2. **Session Data**
   - Session start/end times
   - Total blink counts per session
   - Session creation timestamps

3. **Technical Data**
   - System performance metrics (CPU, memory usage)
   - Camera feed processing (not stored, processed locally)

### GDPR Rights Implementation

#### Right to Access (Article 15)
- Users can request all personal data we hold
- **Status**: Planned - data export functionality needed

#### Right to Rectification (Article 16)
- Users can update their account information
- **Status**: Partial - profile editing needs implementation

#### Right to Erasure (Article 17)
- Users can request complete account deletion
- **Status**: Planned - account deletion functionality needed

#### Right to Data Portability (Article 20)
- Users can export their data in machine-readable format
- **Status**: Planned - JSON/CSV export functionality needed

### Privacy by Design

#### Data Minimization
- Only collect necessary data for app functionality
- Eye tracking processed locally, not transmitted to servers
- No unnecessary personal information collected

#### Purpose Limitation
- Data used only for wellness tracking and user account management
- No third-party data sharing

#### Storage Limitation
- **Planned**: Implement data retention policies
- **Planned**: Automatic deletion of old session data (configurable)

### Security Measures

- Password hashing using secure algorithms
- HTTPS communication with backend API
- Local processing of sensitive camera data
- Authentication tokens for API access

### Consent Management

**Current**: Implicit consent through registration
**Planned**: 
- Explicit consent checkboxes during registration
- Granular consent options for different data types
- Consent withdrawal mechanisms

### Data Protection Impact Assessment

**Low Risk Factors:**
- Wellness/health data is not medical data
- Local processing of camera feed
- Minimal personal data collection

**Medium Risk Factors:**
- Biometric data processing (eye tracking)
- User behavior tracking (blink patterns)

### Compliance Action Items

1. **Immediate (High Priority)**
   - Add explicit consent checkboxes to registration
   - Create privacy policy document
   - Implement user data export functionality

2. **Short Term (4-6 weeks)**
   - Add account deletion functionality
   - Implement data retention policies
   - Create user dashboard for data management

3. **Medium Term (2-3 months)**
   - Audit logging for data access
   - Enhanced security measures
   - Regular compliance reviews

### Contact for Data Protection

For data protection inquiries, contact: [Your contact information]

### Legal Basis for Processing

- **Legitimate Interest**: Wellness monitoring and application functionality
- **Consent**: User registration and data collection consent
- **Contract**: Service provision through user account

---

*Last Updated: August 30, 2025*
*GDPR Compliance Status: In Development*