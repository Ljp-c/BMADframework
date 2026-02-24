import os
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Force set environment variables
if os.getenv("OPENAI_API_BASE"):
    os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE")
if os.getenv("OPENAI_MODEL_NAME"):
    os.environ["OPENAI_MODEL_NAME"] = os.getenv("OPENAI_MODEL_NAME")
os.environ["OTEL_SDK_DISABLED"] = "true"

def main():
    print("Initializing LLM...")
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL_NAME"),
        base_url=os.getenv("OPENAI_API_BASE"),
        api_key=os.getenv("OPENAI_API_KEY"),
        timeout=120.0,
        streaming=False # Disable streaming
    )

    print("Creating Agent...")
    agent = Agent(
        role='Tester',
        goal='Say hello',
        backstory='A simple tester',
        llm=llm,
        verbose=True
    )

    print("Creating Task...")
    task = Task(
        description='Say hello to the world',
        expected_output='A greeting',
        agent=agent
    )

    print("Creating Crew...")
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )

    print("Kickoff...")
    result = crew.kickoff()
    print("Result:", result)

if __name__ == "__main__":
    main()
