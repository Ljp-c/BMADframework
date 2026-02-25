# AutoGen Framework - Quick Reference

## Installation

```bash
pip install -r requirements.txt
```

## Environment Setup

Create `.env` file in the project root:

```env
OPENAI_API_KEY=your-api-key
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4-turbo
OTEL_SDK_DISABLED=true
```

For DeepSeek:
```env
OPENAI_API_KEY=your-deepseek-key
OPENAI_API_BASE=https://api.deepseek.com/v1
OPENAI_MODEL_NAME=deepseek-chat
```

## Running the Framework

### 1. Architecture Mode (Validate Structure)
```bash
RUN_MODE=architecture python main.py
```
Output: Validates all persona and task files exist

### 2. Direct Mode (Single Agent)
```bash
RUN_MODE=direct python main.py
```
Output: Direct OpenAI API response without multi-agent coordination

### 3. AutoGen Mode (Multi-Agent)
```bash
RUN_MODE=autogen python main.py
```
Output: Multi-agent group chat coordination

## File Structure

```
agent_framework/
├── main.py                      # Main entry point (now AutoGen-based)
├── loader.py                    # Markdown file parser
├── agent_architecture.json       # Agent & phase definitions
├── autogen_config.json          # AutoGen-specific config
├── requirements.txt             # Dependencies (pyautogen instead of crewai)
├── test_autogen_minimal.py      # AutoGen integration tests
├── test_connection.py           # Connection tests
└── AUTOGEN_MIGRATION_GUIDE.md   # Migration documentation
```

## Key Classes (AutoGen)

### AssistantAgent
```python
from autogen import AssistantAgent

agent = AssistantAgent(
    name="Agent Name",
    system_message="Your role and instructions here..."
)
```

### UserProxyAgent
```python
from autogen import UserProxyAgent

user = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",  # Autonomous mode
    max_consecutive_auto_reply=3
)
```

### GroupChat
```python
from autogen import GroupChat, GroupChatManager

group_chat = GroupChat(
    agents=[user, agent1, agent2],
    messages=[],
    max_round=10
)

manager = GroupChatManager(groupchat=group_chat)
```

## Common Tasks

### Create Custom Agent
```python
def create_custom_agent(name: str, role: str) -> AssistantAgent:
    return AssistantAgent(
        name=name,
        system_message=f"You are a {role}. Provide detailed responses."
    )
```

### Run Group Chat
```python
user.initiate_chat(
    manager,
    message="Your task here..."
)
```

### Access Chat History
```python
messages = group_chat.messages
for msg in messages:
    print(f"{msg['name']}: {msg['content']}")
```

## Debugging

### Enable Verbose Output
```bash
RUN_MODE=autogen python main.py 2>&1 | tee output.log
```

### Check Configuration
```bash
python -c "import json; print(json.dumps(json.load(open('autogen_config.json')), indent=2))"
```

### Test AutoGen Installation
```bash
python test_autogen_minimal.py
```

## Performance Tips

1. **Max Rounds**: Keep `max_round` to 10-15 for reasonable performance
2. **System Messages**: Clear, concise system messages improve accuracy
3. **API Calls**: Reduce verbose output to speed up execution
4. **Batch Operations**: Group multiple tasks in one group chat

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'autogen'` | Run `pip install pyautogen` |
| API authentication fails | Check OPENAI_API_KEY and OPENAI_API_BASE |
| Group chat not progressing | Increase max_round or check agent system messages |
| Slow responses | Check network/API latency, reduce verbose logging |

## API Comparison

| Feature | CrewAI | AutoGen |
|---------|--------|---------|
| Agent Creation | Role/Goal/Backstory | System Message |
| Task Execution | Sequential/Parallel | Group Chat |
| Multi-agent | Built-in Crew | GroupChat + Manager |
| Flexibility | Less | More |
| Learning Curve | Moderate | Steep |

## Next Steps

1. ✅ Installed AutoGen
2. ✅ Configured environment
3. ✅ Test with `test_autogen_minimal.py`
4. ✅ Run in architecture mode: `RUN_MODE=architecture python main.py`
5. ✅ Run in autogen mode: `RUN_MODE=autogen python main.py`
6. 📝 Customize agents in persona files
7. 📝 Define tasks in task files
8. 🚀 Deploy and monitor

## Resources

- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [AutoGen GitHub](https://github.com/microsoft/autogen)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
