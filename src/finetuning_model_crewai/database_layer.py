"""
Database Layer - Patient and Consultation Data Management
Handles all database operations for the clinical consultation system.

Database Schema (4 tables):
1. patients_table: Basic patient demographics
2. history_table: Medical history per patient
3. visit_table: Each consultation visit
4. plan_table: Treatment plans (future use)
"""

import sqlite3
import json
import os
from datetime import datetime


# Database path - from src/finetuning_model_crewai/ up 2 levels to project root
DB_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "database", "clinical_system.db"
))

# Ensure database directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def get_patient_history(patient_id):
    """
    Retrieve complete patient history from history_table.
    
    Args:
        patient_id (str): Unique patient identifier
    
    Returns:
        dict: Patient history data or None if not found
    """
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM history_table
            WHERE patient_id = ?
        """, (patient_id,))
        
        result = cursor.fetchone()
        return dict(result) if result else None
    finally:
        conn.close()


def get_patient_visits(patient_id):
    """
    Retrieve all visit records for a patient.
    
    Args:
        patient_id (str): Unique patient identifier
    
    Returns:
        list: List of visit records (dicts)
    """
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT * FROM visit_table
            WHERE patient_id = ?
            ORDER BY visit_date DESC
        """, (patient_id,))
        
        results = cursor.fetchall()
        return [dict(row) for row in results]
    finally:
        conn.close()



def search_patient_direct(name, birth_date):
    """
    Direct database search for patient records.
    
    Args:
        name (str): Patient's full name
        birth_date (str): Date of birth in YYYY-MM-DD format
    
    Returns:
        tuple: (patient_id, patient_status, existing_record)
            - patient_id: Unique patient identifier
            - patient_status: 'new' or 'returning'
            - existing_record: Patient data dictionary (None for new patients)
    """
    # Set timeout to avoid "database is locked" error
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Search for patient in patients_table
        cursor.execute("""
            SELECT * FROM patients_table 
            WHERE LOWER(name) = LOWER(?) AND date_of_birth = ?
        """, (name, birth_date))
        
        result = cursor.fetchone()
        
        if result:
            # Patient exists - returning patient
            patient_info = dict(result)
            existing_patient_id = patient_info.get('patient_id')
            patient_past_visits = get_patient_visits(existing_patient_id)
            patient_history = get_patient_history(existing_patient_id)

            patient_data = {
                'patient_info': patient_info,
                'patient_past_visits': patient_past_visits,
                'patient_history': patient_history,
                'last_visit_date': patient_past_visits[0]['visit_date'] if patient_past_visits else None
            }

            return existing_patient_id, 'returning', patient_data
        else:
            # Create record for new patient
            # Generate patient_id (format: P20260104123456 - P + YYYYMMDDHHmmss)
            patient_id = f"P{datetime.now().strftime('%Y%m%d%H%M%S')}"
            registration_date = datetime.now().strftime("%Y-%m-%d")
            
            # Insert into patients_table
            cursor.execute("""
                INSERT INTO patients_table (patient_id, name, date_of_birth, registration_date)
                VALUES (?, ?, ?, ?)
            """, (patient_id, name, birth_date, registration_date))
            
            # Initialize empty history_table record
            cursor.execute("""
                INSERT INTO history_table (patient_id, medical_history, current_medications, 
                                          allergies, family_history, social_history)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (patient_id, 
                  json.dumps({"conditions": [], "surgeries": []}),
                  json.dumps([]),
                  json.dumps([]),
                  json.dumps([]),
                  json.dumps({"smoking": "", "alcohol": "", "drugs": "", "occupation": "", "living_situation": ""})))
            
            conn.commit()
            
            return patient_id, 'new', None
    finally:
        # Always close connection
        conn.close()


def save_visit_direct(patient_id, chief_complaint, Subjective_assessment_result, 
                     objective_findings, patient_status):
    """
    Saves consultation visit data to database.
    
    For NEW patients:
        - Updates history_table with extracted medical history from assessment
        - Saves visit record to visit_table
        - Updates last_visit_date in patients_table
    
    For RETURNING patients:
        - Saves visit record to visit_table
        - Updates last_visit_date in patients_table
    
    Args:
        patient_id (str): Unique patient identifier
        chief_complaint (str): Primary reason for visit
        Subjective_assessment_result: AI agent output with clinical assessment
        objective_findings (str): Physical exam and vital signs data (empty for now)
        patient_status (str): 'new' or 'returning'
    
    Returns:
        tuple: (success, conversation_id)
            - success (bool): True if successful
            - conversation_id (int): ID of the visit record
    """
    # Set timeout to avoid "database is locked" error
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    cursor = conn.cursor()
    
    try:
        visit_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Insert visit record into visit_table
        cursor.execute("""
            INSERT INTO visit_table 
            (patient_id, visit_date, patient_chief_complaint, 
             objective_findings, assessment_summary)
            VALUES (?, ?, ?, ?, ?)
        """, (
            patient_id,
            visit_date,
            chief_complaint,
            objective_findings,  # Empty string for now
            json.dumps({
                "summary": str(Subjective_assessment_result)
            })
        ))
        
        conversation_id = cursor.lastrowid
        
        # Update last_visit_date in patients_table
        cursor.execute("""
            UPDATE patients_table 
            SET last_visit_date = ?
            WHERE patient_id = ?
        """, (visit_date, patient_id))
        
        # For NEW patients: Update history_table with extracted data from assessment
        if patient_status == 'new':
            # Parse Subjective_assessment_result to extract medical history
            # For now, store the full assessment as medical_history
            cursor.execute("""
                UPDATE history_table 
                SET medical_history = ?
                WHERE patient_id = ?
            """, (
                json.dumps({
                    "conditions": [],
                    "surgeries": [],
                    "initial_consultation": str(Subjective_assessment_result)
                }),
                patient_id
            ))

        conn.commit()
        return True, conversation_id
    finally:
        # Always close connection
        conn.close()


