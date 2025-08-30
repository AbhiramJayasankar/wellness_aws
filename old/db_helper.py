#!/usr/bin/env python3
"""
Database Helper Utility for Eye Tracker PostgreSQL Database

This utility provides functions to manage the PostgreSQL database,
including clearing tables, resetting schema, and viewing data.
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import os
import sys
from contextlib import contextmanager

# Database configuration (same as backend)
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'eyetracker'),
    'user': os.getenv('DB_USER', 'eyeuser'),
    'password': os.getenv('DB_PASSWORD', 'eyepass'),
    'port': os.getenv('DB_PORT', '5432')
}

@contextmanager
def get_db_connection():
    """Get database connection with proper error handling"""
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG, cursor_factory=RealDictCursor)
        yield conn
    except psycopg2.OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        print("Make sure PostgreSQL is running and credentials are correct.")
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()

def clear_all_tables():
    """Drop all tables in the database"""
    print("🧹 Clearing all tables from PostgreSQL database...")
    
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            # Drop tables in correct order (foreign key dependencies)
            tables_to_drop = ['sessions', 'users']
            
            for table in tables_to_drop:
                try:
                    cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                    print(f"✅ Dropped table: {table}")
                except Exception as e:
                    print(f"⚠️  Warning dropping {table}: {e}")
            
        conn.commit()
        print("✅ All tables cleared successfully!")

def create_tables():
    """Create fresh tables with updated schema"""
    print("🔨 Creating fresh database schema...")
    
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            # Create users table
            cursor.execute("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255) UNIQUE NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ Created users table")
            
            # Create sessions table
            cursor.execute("""
                CREATE TABLE sessions (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    session_start_time VARCHAR(255) NOT NULL,
                    session_end_time VARCHAR(255) NOT NULL,
                    total_blinks INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            """)
            print("✅ Created sessions table")
            
        conn.commit()
        print("✅ Database schema created successfully!")

def reset_database():
    """Clear all tables and recreate fresh schema"""
    print("🔄 Resetting entire database...")
    clear_all_tables()
    create_tables()
    print("🎉 Database reset complete!")

def view_users():
    """View all users in the database"""
    print("👥 Current users in database:")
    
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, username, email, created_at FROM users ORDER BY created_at DESC")
            users = cursor.fetchall()
            
            if not users:
                print("   No users found.")
                return
            
            print("─" * 80)
            print(f"{'ID':<4} {'Username':<20} {'Email':<30} {'Created':<20}")
            print("─" * 80)
            
            for user in users:
                created_at = user['created_at'].strftime('%Y-%m-%d %H:%M:%S') if user['created_at'] else 'N/A'
                print(f"{user['id']:<4} {user['username']:<20} {user['email']:<30} {created_at:<20}")
            
            print("─" * 80)
            print(f"Total users: {len(users)}")

def view_sessions():
    """View all sessions in the database"""
    print("📊 Current sessions in database:")
    
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT s.id, u.username, s.session_start_time, s.session_end_time, 
                       s.total_blinks, s.created_at
                FROM sessions s
                JOIN users u ON s.user_id = u.id
                ORDER BY s.created_at DESC
            """)
            sessions = cursor.fetchall()
            
            if not sessions:
                print("   No sessions found.")
                return
            
            print("─" * 100)
            print(f"{'ID':<4} {'User':<15} {'Start Time':<20} {'End Time':<20} {'Blinks':<8} {'Created':<20}")
            print("─" * 100)
            
            for session in sessions:
                created_at = session['created_at'].strftime('%Y-%m-%d %H:%M:%S') if session['created_at'] else 'N/A'
                print(f"{session['id']:<4} {session['username']:<15} {session['session_start_time']:<20} "
                      f"{session['session_end_time']:<20} {session['total_blinks']:<8} {created_at:<20}")
            
            print("─" * 100)
            print(f"Total sessions: {len(sessions)}")

def check_database_status():
    """Check database connection and show table info"""
    print("🔍 Checking database status...")
    
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                # Check if tables exist
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    ORDER BY table_name
                """)
                tables = cursor.fetchall()
                
                if tables:
                    print("✅ Database connection successful!")
                    print("📋 Existing tables:")
                    for table in tables:
                        cursor.execute(f"SELECT COUNT(*) FROM {table['table_name']}")
                        count = cursor.fetchone()['count']
                        print(f"   - {table['table_name']}: {count} records")
                else:
                    print("✅ Database connection successful!")
                    print("📋 No tables found in database")
                    
    except Exception as e:
        print(f"❌ Database check failed: {e}")

def main():
    """Interactive menu for database operations"""
    print("🗄️  PostgreSQL Database Helper for Eye Tracker")
    print("=" * 50)
    
    while True:
        print("\nChoose an operation:")
        print("1. Clear all tables")
        print("2. Create fresh schema")
        print("3. Reset database (clear + create)")
        print("4. View users")
        print("5. View sessions") 
        print("6. Check database status")
        print("0. Exit")
        print("-" * 30)
        
        choice = input("Enter your choice (0-6): ").strip()
        
        if choice == "1":
            confirm = input("⚠️  This will delete ALL data. Continue? (y/N): ")
            if confirm.lower() == 'y':
                clear_all_tables()
            else:
                print("Operation cancelled.")
                
        elif choice == "2":
            create_tables()
            
        elif choice == "3":
            confirm = input("⚠️  This will delete ALL data and recreate tables. Continue? (y/N): ")
            if confirm.lower() == 'y':
                reset_database()
            else:
                print("Operation cancelled.")
                
        elif choice == "4":
            view_users()
            
        elif choice == "5":
            view_sessions()
            
        elif choice == "6":
            check_database_status()
            
        elif choice == "0":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()