from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from contextlib import asynccontextmanager, contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib
import jwt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_database()
    yield

app = FastAPI(title="Eye Tracker Backend", version="1.0.0", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

security = HTTPBearer()

# Database configuration
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'eyetracker'),
    'user': os.getenv('DB_USER', 'eyeuser'),
    'password': os.getenv('DB_PASSWORD', 'eyepass'),
    'port': os.getenv('DB_PORT', '5432')
}

SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class SessionData(BaseModel):
    session_start_time: str
    session_end_time: str
    total_blinks: int

class Token(BaseModel):
    access_token: str
    token_type: str

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_token(username: str) -> str:
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=TOKEN_EXPIRE_HOURS)
    payload = {
        "sub": username,
        "exp": expire
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@contextmanager
def get_db_connection():
    conn = psycopg2.connect(**DATABASE_CONFIG, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()

def init_database():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            # Create users table with email column (only if it doesn't exist)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create sessions table (only if it doesn't exist)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    session_start_time VARCHAR(255) NOT NULL,
                    session_end_time VARCHAR(255) NOT NULL,
                    total_blinks INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
        conn.commit()

@app.get("/")
async def root():
    return {"message": "Eye Tracker Backend API - PostgreSQL"}

@app.post("/register", response_model=Token)
async def register(user: UserCreate):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            
            # Check if username already exists
            cursor.execute("SELECT id FROM users WHERE username = %s", (user.username,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Username already exists")
            
            # Check if email already exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (user.email,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Email already exists")
            
            password_hash = hash_password(user.password)
            
            cursor.execute("""
                INSERT INTO users (username, email, password_hash) 
                VALUES (%s, %s, %s)
            """, (user.username, user.email, password_hash))
            
        conn.commit()
        
        token = create_token(user.username)
        return {"access_token": token, "token_type": "bearer"}

@app.post("/login", response_model=Token)
async def login(user: UserLogin):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            
            cursor.execute("SELECT password_hash FROM users WHERE username = %s", 
                          (user.username,))
            result = cursor.fetchone()
            
            if not result or result['password_hash'] != hash_password(user.password):
                raise HTTPException(status_code=401, detail="Invalid credentials")
            
            token = create_token(user.username)
            return {"access_token": token, "token_type": "bearer"}

@app.get("/sessions")
async def get_sessions(username: str = Depends(verify_token)):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user_result = cursor.fetchone()
            if not user_result:
                raise HTTPException(status_code=404, detail="User not found")
            
            user_id = user_result['id']
            
            cursor.execute("""
                SELECT session_start_time, session_end_time, total_blinks, created_at
                FROM sessions 
                WHERE user_id = %s 
                ORDER BY created_at DESC
            """, (user_id,))
            
            results = cursor.fetchall()
            sessions = []
            for row in results:
                sessions.append({
                    "session_start_time": row['session_start_time'],
                    "session_end_time": row['session_end_time'],
                    "total_blinks": row['total_blinks'],
                    "created_at": row['created_at']
                })
            
            return {"sessions": sessions, "total_sessions": len(sessions)}

@app.post("/sessions")
async def add_session(session_data: SessionData, username: str = Depends(verify_token)):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user_result = cursor.fetchone()
            if not user_result:
                raise HTTPException(status_code=404, detail="User not found")
            
            user_id = user_result['id']
            
            cursor.execute("""
                INSERT INTO sessions (user_id, session_start_time, session_end_time, total_blinks) 
                VALUES (%s, %s, %s, %s)
            """, (user_id, session_data.session_start_time, session_data.session_end_time, session_data.total_blinks))
            
        conn.commit()
        
        return {"message": "Session added successfully"}

@app.get("/user")
async def get_user_data(username: str = Depends(verify_token)):
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            
            cursor.execute("SELECT username, email, created_at FROM users WHERE username = %s", (username,))
            user_result = cursor.fetchone()
            if not user_result:
                raise HTTPException(status_code=404, detail="User not found")
            
            user_data = {
                "username": user_result['username'],
                "email": user_result['email'],
                "created_at": user_result['created_at'].isoformat() if user_result['created_at'] else None
            }
            
            # Get session count and total blinks
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user_id_result = cursor.fetchone()
            user_id = user_id_result['id']
            
            cursor.execute("""
                SELECT COUNT(*), COALESCE(SUM(total_blinks), 0) 
                FROM sessions 
                WHERE user_id = %s
            """, (user_id,))
            session_stats = cursor.fetchone()
            
            user_data["total_sessions"] = session_stats['count']
            user_data["total_blinks_all_time"] = session_stats['coalesce']
            
            return user_data

# GDPR Compliance Endpoints

@app.delete("/user/sessions")
async def delete_user_sessions(username: str = Depends(verify_token)):
    """Delete all sessions for the current user (GDPR Right to Erasure)"""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user_result = cursor.fetchone()
            if not user_result:
                raise HTTPException(status_code=404, detail="User not found")
            
            user_id = user_result['id']
            
            cursor.execute("DELETE FROM sessions WHERE user_id = %s", (user_id,))
            deleted_count = cursor.rowcount
            
        conn.commit()
        
        return {
            "message": f"Deleted {deleted_count} sessions for user {username}",
            "deleted_sessions": deleted_count
        }

@app.delete("/user")
async def delete_user_account(username: str = Depends(verify_token)):
    """Delete user account and all associated data (GDPR Right to Erasure)"""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user_result = cursor.fetchone()
            if not user_result:
                raise HTTPException(status_code=404, detail="User not found")
            
            user_id = user_result['id']
            
            # Delete sessions first (due to foreign key constraint)
            cursor.execute("DELETE FROM sessions WHERE user_id = %s", (user_id,))
            deleted_sessions = cursor.rowcount
            
            # Delete user account
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            
        conn.commit()
        
        return {
            "message": f"Account {username} deleted successfully",
            "deleted_sessions": deleted_sessions,
            "account_deleted": True
        }

@app.get("/user/export")
async def export_user_data(username: str = Depends(verify_token)):
    """Export all user data in JSON format (GDPR Right to Data Portability)"""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            
            # Get user data
            cursor.execute("SELECT username, email, created_at FROM users WHERE username = %s", (username,))
            user_result = cursor.fetchone()
            if not user_result:
                raise HTTPException(status_code=404, detail="User not found")
            
            user_id = cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            user_id_result = cursor.fetchone()
            user_id = user_id_result['id']
            
            # Get all sessions
            cursor.execute("""
                SELECT session_start_time, session_end_time, total_blinks, created_at
                FROM sessions 
                WHERE user_id = %s 
                ORDER BY created_at DESC
            """, (user_id,))
            sessions = cursor.fetchall()
            
            # Format export data
            export_data = {
                "export_timestamp": datetime.datetime.utcnow().isoformat(),
                "user_data": {
                    "username": user_result['username'],
                    "email": user_result['email'],
                    "account_created": user_result['created_at'].isoformat() if user_result['created_at'] else None
                },
                "sessions": [
                    {
                        "session_start_time": session['session_start_time'],
                        "session_end_time": session['session_end_time'],
                        "total_blinks": session['total_blinks'],
                        "created_at": session['created_at'].isoformat() if session['created_at'] else None
                    }
                    for session in sessions
                ],
                "summary": {
                    "total_sessions": len(sessions),
                    "total_blinks_all_time": sum(session['total_blinks'] for session in sessions)
                }
            }
            
            return export_data

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)