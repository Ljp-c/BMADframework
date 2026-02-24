# -*- coding: utf-8 -*-
import json
import os
from crewai import Agent, Task, Crew, Process, LLM
from openai import OpenAI
from dotenv import load_dotenv

# Import loader
from loader import MarkdownLoader

# Load environment variables
load_dotenv()

# Disable Telemetry explicitly
os.environ["OTEL_SDK_DISABLED"] = "true"

def create_agent_from_markdown(file_path: str, llm=None) -> Agent:
    """Create CrewAI Agent from Markdown file"""
    data = MarkdownLoader.parse_persona(file_path)
    
    return Agent(
        role=data['role'],
        goal=data['goal'],
        backstory=data['backstory'],
        verbose=True,
        allow_delegation=False,
        llm=llm
    )

def create_task_from_markdown(file_path: str, agent: Agent) -> Task:
    """Create CrewAI Task from Markdown file"""
    data = MarkdownLoader.parse_task(file_path)
    
    return Task(
        description=data['description'],
        expected_output=data['expected_output'],
        agent=agent
    )

def run_direct(personas_dir: str, tasks_dir: str, project_context: str):
    model = os.getenv("OPENAI_MODEL_NAME", "gpt-4-turbo")
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE"),
        timeout=120.0
    )

    pm_file = os.path.join(personas_dir, 'pm.md')
    if not os.path.exists(pm_file):
        print(f"Error: Persona file not found at {pm_file}")
        return

    prd_task_file = os.path.join(tasks_dir, 'create-prd.md')
    if not os.path.exists(prd_task_file):
        print(f"Error: Task file not found at {prd_task_file}")
        return

    persona_text = MarkdownLoader.load_file(pm_file)
    task_text = MarkdownLoader.load_file(prd_task_file)
    user_content = f"{task_text}\n\nProject context:\n{project_context}"

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": persona_text},
            {"role": "user", "content": user_content}
        ],
        max_tokens=800
    )

    output = response.choices[0].message.content
    print("\nResult:")
    print(output)

def load_architecture_config(project_root: str):
    config_path = os.path.join(project_root, "agent_framework", "agent_architecture.json")
    if not os.path.exists(config_path):
        print(f"Error: Architecture config not found at {config_path}")
        return None
    with open(config_path, "r", encoding="utf-8") as file_handle:
        return json.load(file_handle)

def validate_architecture_files(config: dict, project_root: str):
    paths = set()
    for agent in config.get("agents", []):
        if agent.get("persona_file"):
            paths.add(agent["persona_file"])
    for phase in config.get("phases", []):
        for item in phase.get("inputs", []):
            if isinstance(item, str):
                paths.add(item)
        for item in phase.get("outputs", []):
            if isinstance(item, str):
                paths.add(item)
        if phase.get("task_file"):
            paths.add(phase["task_file"])
        for item in phase.get("gates", []):
            paths.add(item)
    missing = []
    for relative_path in sorted(paths):
        full_path = os.path.join(project_root, relative_path)
        if not os.path.exists(full_path):
            missing.append(relative_path)
    return missing

def print_architecture_summary(config: dict):
    agents = config.get("agents", [])
    phases = config.get("phases", [])
    print("\nArchitecture Summary")
    print(f"Agents: {len(agents)}")
    print(f"Phases: {len(phases)}")
    for phase in phases:
        print(f"- {phase.get('id')}: {phase.get('name')} -> {phase.get('owner')}")

def create_agents_from_config(config: dict, project_root: str, llm: LLM):
    agents_map = {}
    for agent_cfg in config.get("agents", []):
        agent_id = agent_cfg.get("id")
        persona_file = agent_cfg.get("persona_file")
        if not agent_id or not persona_file:
            continue
        persona_path = os.path.join(project_root, persona_file)
        if not os.path.exists(persona_path):
            print(f"Error: Persona file not found at {persona_path}")
            continue
        agents_map[agent_id] = create_agent_from_markdown(persona_path, llm)
    return agents_map

def filter_phases(phases: list[dict]):
    start_phase = os.getenv("START_PHASE")
    end_phase = os.getenv("END_PHASE")
    if not start_phase and not end_phase:
        return phases
    ids = [phase.get("id") for phase in phases]
    if start_phase and start_phase not in ids:
        return []
    if end_phase and end_phase not in ids:
        return []
    start_index = ids.index(start_phase) if start_phase else 0
    end_index = ids.index(end_phase) if end_phase else len(phases) - 1
    if start_index > end_index:
        return []
    return phases[start_index : end_index + 1]

def create_tasks_from_config(config: dict, project_root: str, agents_map: dict):
    tasks = []
    phases = filter_phases(config.get("phases", []))
    for phase in phases:
        task_file = phase.get("task_file")
        owner_id = phase.get("owner")
        if not task_file or not owner_id:
            continue
        agent = agents_map.get(owner_id)
        if not agent:
            print(f"Error: Agent not found for phase {phase.get('id')}")
            continue
        task_path = os.path.join(project_root, task_file)
        if not os.path.exists(task_path):
            print(f"Error: Task file not found at {task_path}")
            continue
        tasks.append(create_task_from_markdown(task_path, agent))
    return tasks

def main():
    # Configure LLM (needs OPENAI_API_KEY env var)
    # Support for other OpenAI-compatible APIs (DeepSeek, Moonshot, etc.)
    # Also support Proxy settings via OPENAI_PROXY env var
    
    # Force set environment variables for CrewAI internal usage
    if os.getenv("OPENAI_API_BASE"):
        os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE")
    if os.getenv("OPENAI_MODEL_NAME"):
        os.environ["OPENAI_MODEL_NAME"] = os.getenv("OPENAI_MODEL_NAME")
    
    llm = LLM(
        model=os.getenv("OPENAI_MODEL_NAME", "gpt-4-turbo"),
        base_url=os.getenv("OPENAI_API_BASE"),
        api_key=os.getenv("OPENAI_API_KEY"),
        timeout=120.0
    )
    
    # Path configuration
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    personas_dir = os.path.join(project_root, 'project', '.bmad', 'personas')
    tasks_dir = os.path.join(project_root, 'project', '.bmad', 'tasks')
    
    print(f"Loading personas from: {personas_dir}")
    print(f"Loading tasks from: {tasks_dir}")

    inputs = {
        "project_context": "A code assistant tool based on AI, designed to help developers write code more efficiently."
    }

    run_mode = os.getenv("RUN_MODE", "direct").lower()
    if run_mode == "architecture":
        config = load_architecture_config(project_root)
        if not config:
            return
        print_architecture_summary(config)
        missing = validate_architecture_files(config, project_root)
        if missing:
            print("\nMissing files:")
            for item in missing:
                print(f"- {item}")
        else:
            print("\nAll referenced files exist.")
    elif run_mode == "crewai":
        config = load_architecture_config(project_root)
        if not config:
            return
        agents_map = create_agents_from_config(config, project_root, llm)
        tasks = create_tasks_from_config(config, project_root, agents_map)
        if not tasks:
            print("Error: No tasks were created for CrewAI execution.")
            return
        crew_agents = list({task.agent for task in tasks})
        crew = Crew(
            agents=crew_agents,
            tasks=tasks,
            verbose=True,
            process=Process.sequential
        )
        print("\nStarting the Crew...")
        print("----------------------------------------")
        result = crew.kickoff(inputs=inputs)
        print("\n----------------------------------------")
        print("Crew execution finished.")
        print("Result:")
        print(result)
    else:
        run_direct(personas_dir, tasks_dir, inputs["project_context"])

if __name__ == "__main__":
    main()
