import sqlite3
import os
from datetime import datetime

# Database Configuration
DB_NAME = "remote_controller.db"

def initialize_database():
    """Initializes the SQLite database with Schema v2.1 tables."""
    print(f"[*] Initializing Database: {DB_NAME}...")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # 1. Mappings Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mappings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                intent TEXT UNIQUE NOT NULL,
                target TEXT NOT NULL,
                action_type TEXT CHECK(action_type IN ('app', 'url', 'system_cmd', 'python_script')) NOT NULL,
                version INTEGER DEFAULT 1,
                is_auto_generated BOOLEAN DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 2. App Settings Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                description TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 3. Sessions Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                start_time DATETIME NOT NULL,
                end_time DATETIME,
                duration INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 4. Command Logs Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS command_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                skill_id INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                intent TEXT NOT NULL,
                action TEXT NOT NULL,
                status TEXT CHECK(status IN ('SUCCESS', 'FAILED', 'BUILDING', 'TESTING', 'RETRYING')) NOT NULL,
                retry_count INTEGER DEFAULT 0,
                error_details TEXT,
                execution_time_ms INTEGER,
                FOREIGN KEY (session_id) REFERENCES sessions(id),
                FOREIGN KEY (skill_id) REFERENCES mappings(id)
            )
        ''')

        # 5. Auth Keys Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS auth_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_value TEXT UNIQUE NOT NULL,
                label TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_used DATETIME
            )
        ''')

        # Seed Initial Data
        print("[*] Seeding default settings and dev key...")
        
        # Default Settings
        cursor.execute("INSERT OR IGNORE INTO app_settings (key, value, description) VALUES (?, ?, ?)", 
                       ('privacy_mode', 'false', 'Disable Auto-Build Agentic capability if true'))
        
        # Dev API Key
        cursor.execute("INSERT OR IGNORE INTO auth_keys (key_value, label) VALUES (?, ?)", 
                       ('DEV-SECRET-KEY-123', 'Default Development Key'))

        conn.commit()
        print("[+] Database initialized successfully! [DONE]")

    except sqlite3.Error as e:
        print(f"[!] Error during initialization: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    initialize_database()
