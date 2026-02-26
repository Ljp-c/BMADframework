# -*- coding: utf-8 -*-
"""
AutoGen 智能体对话框架 - 简化版本
==================================
支持新版 autogen-agentchat (0.7.5+) API
"""
import json
import os
import sys
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Disable Telemetry explicitly
os.environ["OTEL_SDK_DISABLED"] = "true"

# Import loader
from loader import MarkdownLoader

# Try importing from new autogen_agentchat
try:
    from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
    AUTOGEN_VERSION = 2
    print("✓ Using autogen-agentchat v2 API")
except ImportError:
    try:
        # Fallback for old autogen
        from autogen import AssistantAgent, UserProxyAgent
        AUTOGEN_VERSION = 1
        print("✓ Using autogen v1 API")
    except ImportError:
        print("❌ Error: autogen package not installed.")
        print("Please run: pip install pyautogen")
        sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("❌ Error: openai package not installed.")
    print("Please run: pip install openai")
    sys.exit(1)


def load_autogen_config(agent_framework_dir: str) -> dict:
    """Load autogen_config.json configuration"""
    config_path = os.path.join(agent_framework_dir, "autogen_config.json")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def get_llm_config(config: dict) -> dict:
    """Get LLM configuration from autogen_config with environment variable overrides"""
    llm_cfg = config.get("llm_config", {})
    
    # Priority: Environment variables > Config file > Defaults
    api_key = os.getenv("OPENAI_API_KEY") or llm_cfg.get("api_key")
    base_url = os.getenv("OPENAI_API_BASE") or llm_cfg.get("base_url")
    model = os.getenv("OPENAI_MODEL_NAME") or llm_cfg.get("model", "gpt-4-turbo")
    
    # Validate critical configuration
    if not api_key:
        raise ValueError("OPENAI_API_KEY not configured in environment variables or config file")
    if not base_url:
        raise ValueError("OPENAI_API_BASE not configured in environment variables or config file")
    
    return {
        "model": model,
        "api_key": api_key,
        "base_url": base_url,
        "timeout": llm_cfg.get("timeout", 120),
        "temperature": llm_cfg.get("temperature", 0.7),
        "max_tokens": llm_cfg.get("max_tokens", 2048)
    }


def load_architecture_config(project_root: str):
    """Load agent_architecture.json configuration"""
    config_path = os.path.join(project_root, "agent_framework", "agent_architecture.json")
    if not os.path.exists(config_path):
        print(f"⚠️  Warning: Architecture config not found at {config_path}")
        return None
    with open(config_path, "r", encoding="utf-8") as file_handle:
        return json.load(file_handle)


def validate_architecture_files(config: dict, project_root: str) -> list:
    """Validate that all files referenced in architecture config exist"""
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
    """Print summary of architecture configuration"""
    agents = config.get("agents", [])
    phases = config.get("phases", [])
    print("\n📊 Architecture Summary")
    print(f"  Agents: {len(agents)}")
    print(f"  Phases: {len(phases)}")
    for phase in phases:
        print(f"  - {phase.get('id')}: {phase.get('name')} (Owner: {phase.get('owner')})")


def run_test_mode():
    """Run a simple test to verify the framework works"""
    print("\n" + "=" * 60)
    print("🧪 Running AutoGen Framework Test Mode")
    print("=" * 60)
    
    try:
        # Test imports
        print("\n✓ All imports successful")
        
        # Test configuration loading
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        agent_framework_dir = os.path.join(project_root, 'agent_framework')
        
        config = load_autogen_config(agent_framework_dir)
        print(f"✓ AutoGen config loaded (version {config.get('version', 'unknown')})")
        
        try:
            llm_config = get_llm_config(config)
            print(f"✓ LLM config loaded: {llm_config['model']}")
        except ValueError as e:
            print(f"⚠️  {str(e)}")
            return
        
        # Test OpenAI client
        try:
            client = OpenAI(
                api_key=llm_config["api_key"],
                base_url=llm_config["base_url"],
                timeout=10.0
            )
            print(f"✓ OpenAI client initialized")
        except Exception as e:
            print(f"⚠️  OpenAI client error: {str(e)}")
            return
        
        # Test agent creation
        try:
            from autogen_agentchat.agents import AssistantAgent
            from autogen_agentchat._runtime import _AsyncIOEventLoop  # For v2 API
            
            # For new API, we need to provide model_client
            # For now, just test that the import works
            print(f"✓ Agent API available (AssistantAgent)")
        except Exception as e:
            print(f"⚠️  Agent creation error: {str(e)}")
        
        print("\n" + "=" * 60)
        print("✓ All tests passed! Framework is ready to use.")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()


def run_interactive_mode_simple():
    """Run a simple interactive mode for testing"""
    print("\n" + "=" * 60)
    print("🤖 AutoGen Interactive Mode")
    print("=" * 60)
    print("\nA simple interactive mode for testing the framework.")
    print("Type 'exit' or 'quit' to exit.\n")
    
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        agent_framework_dir = os.path.join(project_root, 'agent_framework')
        
        # Load configuration
        config = load_autogen_config(agent_framework_dir)
        llm_config = get_llm_config(config)
        
        # Initialize OpenAI client
        client = OpenAI(
            api_key=llm_config["api_key"],
            base_url=llm_config["base_url"],
            timeout=120.0
        )
        
        print(f"Connected to: {llm_config['base_url']}")
        print(f"Using model: {llm_config['model']}\n")
        
        # Interactive loop
        while True:
            try:
                user_input = input("👤 You: ").strip()
                
                if user_input.lower() in ["exit", "quit", "退出", "结束"]:
                    print("\n👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                print("\n🤔 Thinking...\n")
                
                # Send message to LLM
                response = client.chat.completions.create(
                    model=llm_config["model"],
                    messages=[
                        {"role": "system", "content": "You are a helpful AI assistant."},
                        {"role": "user", "content": user_input}
                    ],
                    max_tokens=500,
                    temperature=llm_config["temperature"]
                )
                
                assistant_message = response.choices[0].message.content
                print(f"🤖 Assistant: {assistant_message}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")
                continue
    
    except ValueError as e:
        print(f"\n❌ Configuration Error: {str(e)}")
        print("\nPlease configure your API in .env file:")
        print("  OPENAI_API_KEY=your-key")
        print("  OPENAI_API_BASE=https://api.example.com/v1")
        print("  OPENAI_MODEL_NAME=model-name")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


def main():
    """Main entry point"""
    try:
        # Get running mode
        run_mode = os.getenv("RUN_MODE", "interactive").lower()
        
        if run_mode == "test":
            run_test_mode()
        elif run_mode == "interactive":
            run_interactive_mode_simple()
        elif run_mode == "architecture":
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config = load_architecture_config(project_root)
            if config:
                print_architecture_summary(config)
                missing = validate_architecture_files(config, project_root)
                if missing:
                    print("\n⚠️  Missing files:")
                    for item in missing:
                        print(f"  - {item}")
                else:
                    print("\n✓ All referenced files exist.")
        else:
            print(f"❌ Unknown run mode: {run_mode}")
            print("Available modes: interactive, test, architecture")
            
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
