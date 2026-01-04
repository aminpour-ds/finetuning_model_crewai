# Clinical AI Consultation System

An intelligent medical consultation system powered by [crewAI](https://crewai.com) and fine-tuned phi-3 models running locally via Ollama. This system simulates a complete clinical workflow with 6 specialized AI agents that conduct patient interviews, process clinical data, generate assessments, and maintain persistent medical records.

############################################################################################
Adding a finetune model to ollamd:

1. In the cmd Go to the directory that “Modelfile” and “phi-3-mini-4k-instruct.Q4_K_M.gguf” are there.

2. run this command in that directory:
ollama create subjective_agent -f Modelfile

3. run “ollama list” to see the model
############################################################################################

## Features

- **Patient Identification**: Automatically searches database for returning patients or creates new records
- **Interactive Symptom Interview**: Context-aware OPQRST-based questioning for acute symptoms
- **Medical History Gathering**: Comprehensive or focused history-taking based on patient status
- **Objective Data Processing**: Structures examination findings and lab results
- **Clinical Assessment & Planning**: Synthesizes all data into evidence-based recommendations
- **Database Persistence**: SQLite database with patient records and visit transcripts

## Prerequisites

### Required Software
- **Python**: >=3.10 <3.14
- **Ollama**: Install from [ollama.ai](https://ollama.ai)
- **UV Package Manager**: For dependency management

### Required Models
This project uses fine-tuned phi-3 models running locally via Ollama:
- `llama3.1` (4.9 GB) - For patient identification and data persistence
- `subjective_agent` (2.3 GB) - Fine-tuned for symptom/history interviews
- `objective_exam_agent` (2.3 GB) - Fine-tuned for objective data processing
- `assessment_plan_agent` (2.3 GB) - Fine-tuned for clinical assessments

## Installation

### 1. Install Ollama
Download and install from [ollama.ai](https://ollama.ai)

### 2. Pull Required Models
```bash
ollama pull llama3.1
```

### 3. Install Fine-tuned Models (Optional)
If you have the fine-tuned `.gguf` model files:
```bash
ollama create subjective_agent -f Modelfile_subjective
ollama create objective_exam_agent -f Modelfile_objective
ollama create assessment_plan_agent -f Modelfile_assessment
```

### 4. Install Python Dependencies
```bash
pip install uv
crewai install
```

### 5. Configure Environment
Create a `.env` file in the project root:
```bash
MODEL=ollama/llama3.1
API_BASE=http://localhost:11434
```

**Note**: No API keys required - this project runs 100% locally!

## Running the Application

### Method 1: Interactive Mode (Recommended)
Start Ollama server (if not already running):
```bash
ollama serve
```

Run the interactive consultation system:
```bash
.venv\Scripts\python.exe src\finetuning_model_crewai\main.py
```

You will be prompted to enter:
- Your full name
- Date of birth (YYYY-MM-DD format)
- Chief complaint (what brings you in today)
- Vital signs (optional - press Enter for defaults)
- Physical examination findings (optional)

The system will then:
1. Search database for your existing records
2. Conduct interactive symptom interview
3. Gather relevant medical history
4. Process objective clinical findings
5. Generate assessment and treatment plan
6. Save complete consultation to database

### Method 2: Using CrewAI Command
```bash
crewai run
```
*Note: This uses example patient data*

## Project Structure

```
finetuning_model_crewai/
├── database/
│   └── clinical_system.db          # SQLite patient database
├── src/finetuning_model_crewai/
│   ├── config/
│   │   ├── agents.yaml             # 6 agent configurations
│   │   └── tasks.yaml              # Sequential task workflow
│   ├── tools/
│   │   └── custom_tool.py          # 5 database CRUD tools
│   ├── crew.py                     # CrewAI agent definitions
│   └── main.py                     # Entry point
├── Modelfile_*                     # Fine-tuned model configurations
└── pyproject.toml                  # Python dependencies
```

## Understanding the System

### 6 AI Agents
1. **Patient Identification Agent**: Database search and record management
2. **Subjective Agent (Acute Symptoms)**: Interactive symptom interview using OPQRST method
3. **Subjective Agent (History)**: Medical/family/social history gathering
4. **Objective Agent**: Structures exam findings and lab results
5. **Assessment/Plan Agent**: Clinical decision support and treatment planning
6. **Data Persistence Agent**: Saves consultation records to database

### Sequential Workflow
Each task builds on previous context:
- Patient Identification → Symptom Interview → History → Objective Data → Assessment → Database Save

### Database Schema
- **patients** table: Demographics, medical history, medications, allergies
- **conversations** table: Visit transcripts, chief complaints, assessments

## Support

For support, questions, or feedback regarding the FinetuningModelCrewai Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
