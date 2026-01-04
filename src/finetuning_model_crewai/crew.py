from pathlib import Path
import yaml
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class FinetuningModelCrewai:
    def __init__(self):
        # Load agents configuration from YAML
        config_path = Path(__file__).parent / 'config' / 'agents.yaml'
        with open(config_path, 'r') as f:
            self.agents_config = yaml.safe_load(f)
        
        # Load tasks configuration from YAML
        tasks_path = Path(__file__).parent / 'config' / 'tasks.yaml'
        with open(tasks_path, 'r') as f:
            self.tasks_config = yaml.safe_load(f)

    agents: List[BaseAgent]
    tasks: List[Task]

    # ============================================================================
    # 3-AGENT WORKFLOW
    # ============================================================================
    # Agent 1: Acute Symptoms (Chief Complaint + HPI + ROS)
    # Agent 2: Medical History (PMH + Medications + Allergies)
    # Agent 3: Clinical Summary (Synthesizes agent 1 + 2)
    # ============================================================================

    # ========== AGENT 1: Acute Symptoms Interview ==========
    @agent
    def subjective_agent_Acute_Symptoms(self) -> Agent:
        """Gathers Chief Complaint, HPI, and Review of Systems"""
        return Agent(
            config=self.agents_config["subjective_agent_Acute_Symptoms"],
            verbose=True, # Prints detailed execution logs
            max_iter=5, # Maximum 5 iterations if agent needs to refine answers
            allow_delegation=False # No delegation to other agents
        )

    @task
    def acute_symptoms_interview_task(self) -> Task:
        """Task for symptom interview"""
        task_config = self.tasks_config["acute_symptoms_interview_task"]
        return Task(
            description=task_config.get("description", ""),
            expected_output=task_config.get("expected_output", ""),
            config=self.tasks_config["acute_symptoms_interview_task"]
        )

    # ========== AGENT 2: Medical History Interview ==========
    @agent
    def subjective_agent_history(self) -> Agent:
        """Gathers Past Medical History, Medications, and Allergies"""
        return Agent(
            config=self.agents_config["subjective_agent_history"],
            verbose=True,
            max_iter=5,
            allow_delegation=False
        )
    
    @task
    def medical_history_interview_task(self) -> Task:
        """Task for medical history collection"""
        task_config = self.tasks_config["medical_history_interview_task"]
        return Task(
            description=task_config.get("description", ""),
            expected_output=task_config.get("expected_output", ""),
            config=self.tasks_config["medical_history_interview_task"]
        )

    # ========== AGENT 3: Clinical Summary ==========
    @agent
    def clinical_summary_agent(self) -> Agent:
        """Synthesizes all collected information into clinical summary"""
        return Agent(
            config=self.agents_config["clinical_summary_agent"],
            verbose=True,
            max_iter=2,
            allow_delegation=False
        )
    
    @task
    def clinical_summary_task(self) -> Task:
        """Task for creating comprehensive clinical summary"""
        task_config = self.tasks_config["clinical_summary_task"]
        return Task(
            description=task_config.get("description", ""),
            expected_output=task_config.get("expected_output", ""),
            config=self.tasks_config["clinical_summary_task"]
        )

    # ========== Crew Definition ==========
    @crew
    def crew(self) -> Crew:
       
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
