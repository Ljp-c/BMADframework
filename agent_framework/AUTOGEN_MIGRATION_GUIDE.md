# AutoGen Migration Guide

## Overview
This project has been migrated from **CrewAI** to **AutoGen** framework for AI agent orchestration.

## Key Changes

### 1. Framework Dependencies
**Before (CrewAI):**
```
crewai
python-dotenv
langchain_openai
```

**After (AutoGen):**
```
pyautogen>=0.2.0
python-dotenv
langchain_openai
openai
```

### 2. Agent Creation
**CrewAI:**
```python
from crewai import Agent, Task, Crew, Process, LLM

agent = Agent(
    role="role",
    goal="goal",
    backstory="backstory",
    llm=llm
)
```

**AutoGen:**
```python
from autogen import AssistantAgent, UserProxyAgent

agent = AssistantAgent(
    name="agent_name",
    system_message="system message with role, goal, backstory"
)
```

### 3. Execution Modes
The system now supports multiple execution modes:

- **direct**: Direct OpenAI API calls (no multi-agent coordination)
- **autogen**: AutoGen group chat orchestration
- **architecture**: Configuration validation only

Set via environment variable:
```bash
export RUN_MODE=autogen
```

### 4. Running AutoGen
```bash
# Install dependencies
pip install -r requirements.txt

# Run AutoGen mode
RUN_MODE=autogen python main.py

# Run tests
python test_autogen_minimal.py
```

### 5. Configuration Files
- **autogen_config.json**: AutoGen-specific configuration
- **agent_architecture.json**: Shared configuration (still compatible)

### 6. Key Components

#### AssistantAgent
- Responds to messages and performs tasks
- Can call functions and use tools
- Primary agent type for task execution

#### UserProxyAgent
- Initiates conversations
- Can approve/reject actions
- Set to `human_input_mode="NEVER"` for autonomous operation

#### GroupChat
- Multi-agent conversation management
- Manages message history
- Configurable max rounds

#### GroupChatManager
- Orchestrates conversations
- Determines which agent speaks next
- Handles message routing

### 7. Migration Checklist

- [x] Update requirements.txt with pyautogen
- [x] Replace CrewAI imports with AutoGen
- [x] Convert Agent creation (Role/Goal/Backstory → system_message)
- [x] Replace Task execution with group chat
- [x] Remove Crew/Process orchestration
- [x] Add UserProxyAgent for conversation initiation
- [x] Create AutoGen configuration file
- [x] Add AutoGen execution mode to main.py
- [x] Create AutoGen test file
- [x] Update documentation

### 8. API Compatibility
AutoGen works with OpenAI-compatible APIs:
- OpenAI (gpt-4-turbo, gpt-3.5-turbo, etc.)
- DeepSeek
- Moonshot/Kimi
- Other OpenAI-compatible endpoints

Configure via environment variables:
```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_API_BASE="https://api.openai.com/v1"
export OPENAI_MODEL_NAME="gpt-4-turbo"
```

### 9. Performance Considerations

#### AutoGen Advantages
- Better multi-agent conversation flow
- More flexible agent interaction patterns
- Better error handling and recovery
- Rich conversation history tracking

#### Differences from CrewAI
- No automatic task sequencing (manual orchestration)
- More control over agent interactions
- Better for complex multi-agent workflows
- Requires explicit message crafting

### 10. Future Enhancements

- [ ] Add tool/function calling capabilities
- [ ] Implement custom agent selectors
- [ ] Add conversation history persistence
- [ ] Implement RAG (Retrieval Augmented Generation)
- [ ] Add streaming response support
- [ ] Create custom termination conditions

## Troubleshooting

### Issue: "No module named 'autogen'"
**Solution:** 
```bash
pip install pyautogen>=0.2.0
```

### Issue: API authentication errors
**Solution:** 
Verify environment variables:
```bash
echo $OPENAI_API_KEY
echo $OPENAI_API_BASE
echo $OPENAI_MODEL_NAME
```

### Issue: Group chat stuck or not progressing
**Solution:** 
- Check max_round configuration
- Verify agent system messages are clear
- Check for termination conditions

## Resources

- AutoGen Documentation: https://microsoft.github.io/autogen/
- AutoGen GitHub: https://github.com/microsoft/autogen
- OpenAI API: https://platform.openai.com/docs/api-reference
- DeepSeek API: https://platform.deepseek.com/

## Support

For issues or questions about the AutoGen migration, please refer to:
1. AutoGen official documentation
2. Project architecture documentation
3. Environment configuration guide
