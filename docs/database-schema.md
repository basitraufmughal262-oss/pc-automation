<!-- 
FILE_TYPE: Project Documentation (DB Schema)
CATEGORY: Database Design
ENTRIES: 5 Tables (SQLite)
DATE_RANGE: 2026-05-08
KEYWORDS: SQL, DDL, SQLite, Mappings, Versions, Agentic, Settings
SUMMARY: Updated schema v2.0 to support autonomous skill generation, version rollback, and privacy settings.
-->
# Database Schema v2.0 - AI-Powered Remote PC Controller

**Engine:** SQLite
**File:** `remote_controller.db`

---

## 1. Tables (SQL DDL)

### 1.1 Mappings Table (Updated)
Stores both static and auto-generated intent actions.
```sql
CREATE TABLE mappings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    intent TEXT UNIQUE NOT NULL,
    target TEXT NOT NULL,
    action_type TEXT CHECK(action_type IN ('app', 'url', 'system_cmd', 'python_script')) NOT NULL,
    version INTEGER DEFAULT 1,          -- REQ-DATA-03: Rollback support
    is_auto_generated BOOLEAN DEFAULT 0, -- Track AI-built skills
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 1.2 App Settings Table (NEW)
Stores global configurations like Privacy Mode.
```sql
CREATE TABLE app_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Default Seed Data
-- INSERT INTO app_settings (key, value, description) VALUES ('privacy_mode', 'false', 'Disable Auto-Build if true');
```

### 1.3 Sessions Table
Tracks work sessions for the timer.
```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    duration INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 1.4 Command Logs Table (Updated)
Audit trail with detailed status for AI building process.
```sql
CREATE TABLE command_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER,
    skill_id INTEGER,                    -- Link to mappings.id
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    intent TEXT NOT NULL,
    action TEXT NOT NULL,
    status TEXT CHECK(status IN ('SUCCESS', 'FAILED', 'BUILDING', 'TESTING', 'RETRYING')) NOT NULL,
    retry_count INTEGER DEFAULT 0,       -- REQ-AI-04 Tracking
    error_details TEXT,
    execution_time_ms INTEGER,           -- Performance tracking
    FOREIGN KEY (session_id) REFERENCES sessions(id),
    FOREIGN KEY (skill_id) REFERENCES mappings(id)
);
```

### 1.5 Auth Keys Table
API Key storage for security.
```sql
CREATE TABLE auth_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key_value TEXT UNIQUE NOT NULL,
    label TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_used DATETIME
);
```

---

## 2. Decision Notes
- **Python Script Action:** Added `python_script` to `action_type` for REQ-CMD-03 (UI Automation).
- **Rollback Logic:** The `version` column allows the server to keep historical scripts and revert if needed.
- **Privacy Enforcement:** The `app_settings` table will be checked by the `SkillGenerator` before initiating any AI build.
