"""
Database Initialization and Management Utilities
"""
import sqlite3
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config

def init_database():
    """Initialize database with schema"""
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            failed_attempts INTEGER DEFAULT 0,
            locked_until DATETIME,
            mfa_secret TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            username TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            success INTEGER DEFAULT 0,
            blocked INTEGER DEFAULT 0,
            attack_type TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            attack_type TEXT,
            defense_config TEXT,
            total_attempts INTEGER,
            successful INTEGER,
            blocked INTEGER,
            duration_sec REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blocked_ips (
            ip TEXT PRIMARY KEY,
            blocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            reason TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("[+] Database initialized successfully")

def clear_database():
    """Clear all data from database"""
    if os.path.exists(config.DATABASE_PATH):
        os.remove(config.DATABASE_PATH)
        print("[+] Database cleared")
        init_database()
    else:
        print("[!] Database does not exist")

def show_stats():
    """Display database statistics"""
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()

    print("\n" + "=" * 60)
    print("  DATABASE STATISTICS")
    print("=" * 60)

    # Users
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"Users: {user_count}")

    # Login attempts
    cursor.execute("SELECT COUNT(*) FROM login_attempts")
    attempt_count = cursor.fetchone()[0]
    print(f"Login Attempts: {attempt_count}")

    cursor.execute("SELECT COUNT(*) FROM login_attempts WHERE success = 1")
    success_count = cursor.fetchone()[0]
    print(f"  - Successful: {success_count}")

    cursor.execute("SELECT COUNT(*) FROM login_attempts WHERE blocked = 1")
    blocked_count = cursor.fetchone()[0]
    print(f"  - Blocked: {blocked_count}")

    # Blocked IPs
    cursor.execute("SELECT COUNT(*) FROM blocked_ips")
    blocked_ip_count = cursor.fetchone()[0]
    print(f"Blocked IPs: {blocked_ip_count}")

    # Metrics
    cursor.execute("SELECT COUNT(*) FROM metrics")
    metrics_count = cursor.fetchone()[0]
    print(f"Experiment Metrics: {metrics_count}")

    print("=" * 60)

    conn.close()

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python db_utils.py init    - Initialize database")
        print("  python db_utils.py clear   - Clear all data")
        print("  python db_utils.py stats   - Show statistics")
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        init_database()
    elif command == "clear":
        confirm = input("Clear all data? (yes/no): ")
        if confirm.lower() == 'yes':
            clear_database()
    elif command == "stats":
        show_stats()
    else:
        print(f"Unknown command: {command}")
