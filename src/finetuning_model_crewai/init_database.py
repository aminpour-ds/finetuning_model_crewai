"""
Database Initialization Script
Creates the clinical consultation database with 4 tables from scratch.
Run this once to set up the database structure.
"""

import sqlite3
import os

# Database path
DB_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "database", "clinical_system.db"
))

def initialize_database():
    """
    Create database tables from scratch.
    """
    
    # Ensure database directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🗄️  Initializing database...")
    
    # Drop existing tables if they exist
    cursor.execute("DROP TABLE IF EXISTS plan_table")
    cursor.execute("DROP TABLE IF EXISTS visit_table")
    cursor.execute("DROP TABLE IF EXISTS history_table")
    cursor.execute("DROP TABLE IF EXISTS patients_table")

    print("✅ Dropped old tables (if existed)")
    
    # 1. CREATE patients_table
    cursor.execute("""
        CREATE TABLE patients_table (
            patient_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            registration_date TEXT NOT NULL,
            last_visit_date TEXT
        )
    """)
    print("✅ Created patients_table")
    
    # 2. CREATE history_table
    cursor.execute("""
        CREATE TABLE history_table (
            patient_id TEXT PRIMARY KEY,
            medical_history TEXT,
            current_medications TEXT,
            allergies TEXT,
            family_history TEXT,
            social_history TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients_table(patient_id)
        )
    """)
    print("✅ Created history_table")
    
    # 3. CREATE visit_table
    cursor.execute("""
        CREATE TABLE visit_table (
            conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            visit_date TEXT NOT NULL,
            patient_chief_complaint TEXT NOT NULL,
            objective_findings TEXT,
            assessment_summary TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients_table(patient_id)
        )
    """)
    print("✅ Created visit_table")
    
    # 4. CREATE plan_table (for future use)
    cursor.execute("""
        CREATE TABLE plan_table (
            conversation_id INTEGER PRIMARY KEY,
            plan TEXT,
            FOREIGN KEY (conversation_id) REFERENCES visit_table(conversation_id)
        )
    """)
    print("✅ Created plan_table")
    
    conn.commit()
    conn.close()
    
    print("\n✅ Database initialized successfully!")
    print(f"📍 Location: {DB_PATH}")


if __name__ == "__main__":
    initialize_database()
