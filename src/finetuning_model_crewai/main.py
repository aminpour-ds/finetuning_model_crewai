
import sys
import warnings
from typing import Any
from datetime import datetime

from finetuning_model_crewai.crew import FinetuningModelCrewai
from finetuning_model_crewai.database_layer import search_patient_direct, save_visit_direct

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# ---------------------------------- running Functions ------------------------------

def run():
    """
    Run the simplified 3-agent clinical consultation system.
    """
    
    print("=" * 70)
    print("🏥 CLINICAL AI SYSTEM - 3 Agent Workflow")
    print("=" * 70)
    print("\nWelcome! This system uses 3 specialized agents:")
    print("1️⃣  Symptom Interview (Chief Complaint + HPI + ROS)")
    print("2️⃣  Medical History (PMH + Medications + Allergies)")
    print("3️⃣  Clinical Summary (Synthesizes all information)\n")
    
    # Interactive patient input
    print("📋 PATIENT REGISTRATION")
    print("-" * 70)
    patient_name = input("Enter your full name: ").strip()
    patient_birth_date = input("Enter your date of birth (YYYY-MM-DD): ").strip()
    
    print("\n💬 CHIEF COMPLAINT")
    print("-" * 70)
    print("Please describe what brings you in today:")
    patient_complaint = input("> ").strip()

    try:
        # SEARCH for patient in DATABASE 
        print("\n🔍 Searching patient database...")
        patient_id, patient_status, existing_record = search_patient_direct(patient_name, patient_birth_date)
        
        if patient_status == 'returning':
            print(f"✅ Welcome back! Found existing record (Patient ID: {patient_id})")
            if existing_record:
                last_visit = existing_record.get('last_visit_date', 'N/A')
                print(f"📅 Last visit: {last_visit}")
        else:
            print(f"✅ New patient registered (Patient ID: {patient_id})")
        
        
        # Format patient history for agents
        patient_history_context = ""
        if patient_status == 'returning' and existing_record:
            patient_history_context = f"""
PATIENT MEDICAL HISTORY (from previous visits):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Last Visit Date: {existing_record.get('last_visit_date', 'N/A')}
Previous Chief Complaints: {existing_record.get('previous_complaints', 'None recorded')}
Past Medical History: {existing_record.get('pmh', 'None recorded')}
Current Medications: {existing_record.get('medications', 'None recorded')}
Known Allergies: {existing_record.get('allergies', 'None recorded')}
Surgical History: {existing_record.get('surgical_history', 'None recorded')}
Social History: {existing_record.get('social_history', 'None recorded')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  Please review this information and ask about any CHANGES or UPDATES.
"""
        else:
            patient_history_context = "NEW PATIENT - No previous medical history on file. Conduct full medical history interview."
        

        # Prepare inputs for AI agents
        inputs: dict[str, Any] = {
            'patient_id': str(patient_id) if patient_id is not None else '',
            'patient_name': patient_name,
            'patient_birth_date': patient_birth_date,
            'patient_complaint': patient_complaint,
            'patient_status': patient_status,
            'patient_history_context': patient_history_context
        }
        
        print("\n" + "=" * 70)
        print("🚀 Starting Clinical AI Consultation Workflow...")
        print("=" * 70)
        print(f"\n👤 Patient: {patient_name}")
        print(f"📅 DOB: {patient_birth_date}")
        print(f"🆔 Patient ID: {patient_id}")
        print(f"📊 Status: {patient_status.upper()}")
        print(f"💬 Chief Complaint: {patient_complaint}\n")
        
        
        # Run the 3-agent crew
        result = FinetuningModelCrewai().crew().kickoff(inputs=inputs)
        
        print("\n" + "=" * 70)
        print("💾 Saving consultation data to database...")
        print("=" * 70)
        
        # Save visit data to database (objective_findings is empty for simplified version)
        save_success, conversation_id = save_visit_direct(
            patient_id=patient_id,
            chief_complaint=patient_complaint,
            Subjective_assessment_result=result,
            objective_findings="",  # Empty for simplified 3-agent system
            patient_status=patient_status
        )
        
        if save_success:
            print(f"✅ Visit data saved! (Conversation ID: {conversation_id})")
        
        print("\n" + "=" * 70)
        print("✅ CONSULTATION COMPLETED - 3 Agents Successfully Executed")
        print("=" * 70)
        print("\n📊 Subjective Assessment Summary:")
        print(result)
        
        print("\n📊 View saved data with: python view_database.py")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        import traceback
        traceback.print_exc()
        raise


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        FinetuningModelCrewai().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        FinetuningModelCrewai().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }

    try:
        FinetuningModelCrewai().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": ""
    }

    try:
        result = FinetuningModelCrewai().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")

if __name__ == "__main__":
    run()
