#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test AutoGen framework integration
"""

import os
import json
from autogen import AssistantAgent, UserProxyAgent, GroupChat, GroupChatManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_autogen_basic():
    """Test basic AutoGen functionality"""
    print("Testing AutoGen basic functionality...")
    
    # Create a simple assistant agent
    assistant = AssistantAgent(
        name="Assistant",
        system_message="You are a helpful AI assistant.",
        llm_config={
            "model": os.getenv("OPENAI_MODEL_NAME", "gpt-4-turbo"),
            "api_key": os.getenv("OPENAI_API_KEY"),
            "base_url": os.getenv("OPENAI_API_BASE"),
        }
    )
    
    # Create a user proxy agent
    user_proxy = UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1,
        llm_config={
            "model": os.getenv("OPENAI_MODEL_NAME", "gpt-4-turbo"),
            "api_key": os.getenv("OPENAI_API_KEY"),
            "base_url": os.getenv("OPENAI_API_BASE"),
        }
    )
    
    print("Agents created successfully!")
    print(f"Assistant name: {assistant.name}")
    print(f"User proxy name: {user_proxy.name}")
    
    return assistant, user_proxy

def test_group_chat():
    """Test AutoGen group chat functionality"""
    print("\nTesting AutoGen group chat...")
    
    # Create multiple agents
    agent1 = AssistantAgent(
        name="Analyst",
        system_message="You are a Business Analyst.",
        llm_config={
            "model": os.getenv("OPENAI_MODEL_NAME", "gpt-4-turbo"),
            "api_key": os.getenv("OPENAI_API_KEY"),
            "base_url": os.getenv("OPENAI_API_BASE"),
        }
    )
    
    agent2 = AssistantAgent(
        name="Developer",
        system_message="You are a Developer.",
        llm_config={
            "model": os.getenv("OPENAI_MODEL_NAME", "gpt-4-turbo"),
            "api_key": os.getenv("OPENAI_API_KEY"),
            "base_url": os.getenv("OPENAI_API_BASE"),
        }
    )
    
    user_proxy = UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=2,
        llm_config={
            "model": os.getenv("OPENAI_MODEL_NAME", "gpt-4-turbo"),
            "api_key": os.getenv("OPENAI_API_KEY"),
            "base_url": os.getenv("OPENAI_API_BASE"),
        }
    )
    
    # Create group chat
    group_chat = GroupChat(
        agents=[user_proxy, agent1, agent2],
        messages=[],
        max_round=3
    )
    
    manager = GroupChatManager(groupchat=group_chat)
    
    print("Group chat created successfully!")
    print(f"Agents in group: {len(group_chat.agents)}")
    
    return group_chat, manager

def test_autogen_config():
    """Test AutoGen configuration"""
    print("\nTesting AutoGen configuration...")
    
    config_path = os.path.join(os.path.dirname(__file__), "autogen_config.json")
    
    if not os.path.exists(config_path):
        print(f"AutoGen config file not found at {config_path}")
        return False
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    print(f"Config loaded successfully!")
    print(f"Framework: {config.get('framework')}")
    print(f"Version: {config.get('version')}")
    print(f"Agents: {len(config.get('agents', []))}")
    
    return True

def main():
    print("=" * 50)
    print("AutoGen Integration Tests")
    print("=" * 50)
    
    # Test 1: Basic functionality
    try:
        test_autogen_basic()
        print("✓ Basic AutoGen test passed")
    except Exception as e:
        print(f"✗ Basic AutoGen test failed: {e}")
    
    # Test 2: Group chat
    try:
        test_group_chat()
        print("✓ Group chat test passed")
    except Exception as e:
        print(f"✗ Group chat test failed: {e}")
    
    # Test 3: Configuration
    try:
        test_autogen_config()
        print("✓ Configuration test passed")
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
    
    print("\n" + "=" * 50)
    print("All tests completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()
