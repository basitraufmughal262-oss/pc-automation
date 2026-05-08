import sqlite3
from ..config import get_settings

class SkillRegistry:
    def __init__(self):
        self.settings = get_settings()

    def get_skill(self, intent: str):
        """Fetches a skill mapping from the database."""
        conn = sqlite3.connect(self.settings.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "SELECT target, action_type, version, is_auto_generated FROM mappings WHERE intent = ? AND is_active = 1", 
                (intent,)
            )
            row = cursor.fetchone()
            if row:
                return {
                    "target": row[0],
                    "action_type": row[1],
                    "version": row[2],
                    "is_auto_generated": row[3]
                }
            return None
        finally:
            conn.close()

    def register_skill(self, intent: str, target: str, action_type: str, is_auto: bool = False):
        """Registers a new skill (or updates existing)."""
        conn = sqlite3.connect(self.settings.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO mappings (intent, target, action_type, is_auto_generated, updated_at)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (intent, target, action_type, 1 if is_auto else 0))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error registering skill: {e}")
            return False
        finally:
            conn.close()
