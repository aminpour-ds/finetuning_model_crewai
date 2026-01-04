"""
View Database Tables and Contents
Updated for new 4-table schema
"""
import sqlite3
import json

# Connect to database
conn = sqlite3.connect('database/clinical_system.db')
conn.row_factory = sqlite3.Row  # Return rows as dictionaries
cursor = conn.cursor()

print("=" * 70)
print("DATABASE SCHEMA - 4 TABLES")
print("=" * 70)

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("\nTables in database:")
for table in tables:
    print(f"  📁 {table['name']}")

print("\n" + "=" * 70)
print("1. PATIENTS_TABLE (Demographics)")
print("=" * 70)

cursor.execute("SELECT * FROM patients_table ORDER BY registration_date DESC")
patients = cursor.fetchall()
print(f"\nTotal patients: {len(patients)}\n")

for patient in patients:
    print(f"🆔 Patient ID: {patient['patient_id']}")
    print(f"👤 Name: {patient['name']}")
    print(f"📅 DOB: {patient['date_of_birth']}")
    print(f"📝 Registered: {patient['registration_date']}")
    print(f"🕒 Last Visit: {patient['last_visit_date'] or 'Never'}")
    print("-" * 70)

print("\n" + "=" * 70)
print("2. HISTORY_TABLE (Medical History)")
print("=" * 70)

cursor.execute("SELECT * FROM history_table")
histories = cursor.fetchall()
print(f"\nTotal history records: {len(histories)}\n")

for history in histories:
    print(f"🆔 Patient ID: {history['patient_id']}")
    
    if history['medical_history']:
        med_hist = json.loads(history['medical_history'])
        print(f"🏥 Medical History:")
        print(f"   {json.dumps(med_hist, indent=3)}")
    
    if history['current_medications']:
        meds = json.loads(history['current_medications'])
        print(f"💊 Medications: {len(meds)} items")
        if meds:
            for med in meds:
                print(f"   - {med}")
    
    if history['allergies']:
        allergies = json.loads(history['allergies'])
        print(f"⚠️  Allergies: {len(allergies)} items")
        if allergies:
            for allergy in allergies:
                print(f"   - {allergy}")
    
    print("-" * 70)

print("\n" + "=" * 70)
print("3. VISIT_TABLE (Consultation Visits)")
print("=" * 70)

cursor.execute("SELECT * FROM visit_table ORDER BY visit_date DESC")
visits = cursor.fetchall()
print(f"\nTotal visits: {len(visits)}\n")

for visit in visits:
    print(f"🔢 Conversation ID: {visit['conversation_id']}")
    print(f"🆔 Patient ID: {visit['patient_id']}")
    print(f"📅 Visit Date: {visit['visit_date']}")
    print(f"💬 Chief Complaint: {visit['patient_chief_complaint']}")
    
    if visit['objective_findings']:
        print(f"🩺 Objective Findings: {visit['objective_findings'][:100]}...")
    else:
        print(f"🩺 Objective Findings: (empty)")
    
    if visit['assessment_summary']:
        assessment = json.loads(visit['assessment_summary'])
        print(f"📊 Assessment Summary:")
        print(f"   {json.dumps(assessment, indent=3)[:300]}...")
    
    print("-" * 70)

print("\n" + "=" * 70)
print("4. PLAN_TABLE (Treatment Plans - Future Use)")
print("=" * 70)

cursor.execute("SELECT * FROM plan_table")
plans = cursor.fetchall()
print(f"\nTotal treatment plans: {len(plans)}")

if plans:
    for plan in plans:
        print(f"🔢 Conversation ID: {plan['conversation_id']}")
        print(f"📋 Plan: {plan['plan']}")
        print("-" * 70)
else:
    print("(No treatment plans yet - this table is for future use)")

print("\n" + "=" * 70)
print("DATABASE SUMMARY")
print("=" * 70)
print(f"Total Patients: {len(patients)}")
print(f"Total History Records: {len(histories)}")
print(f"Total Visits: {len(visits)}")
print(f"Total Plans: {len(plans)}")
print("=" * 70)

conn.close()
