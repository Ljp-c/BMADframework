# AutoGen Framework - 智能体对话系统

重构后的 AutoGen 框架，提供了完整的多智能体协作对话系统。

## 功能特性

- ✅ **交互模式** (Interactive) - 与用户实时对话的多智能体系统
- ✅ **协作模式** (AutoGen) - 多智能体自动协作完成任务
- ✅ **直接模式** (Direct) - 单智能体直接调用
- ✅ **架构验证** (Architecture) - 验证配置文件完整性
- ✅ **OpenAI 兼容 API** - 支持任何 OpenAI 兼容的 API 端点
- ✅ **错误恢复** - 完善的错误处理和恢复机制

## 快速开始

### 1. 安装依赖

```bash
# 使用 pip
pip install -r requirements.txt

# 或者单独安装
pip install pyautogen openai python-dotenv
```

### 2. 配置 API 凭证

编辑 `.env` 文件，配置你的 API 凭证：

```env
# OpenAI 或兼容的 API
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4-turbo

# 或使用其他模型提供商
# OPENAI_API_KEY=your-key-here
# OPENAI_API_BASE=https://api.deepseek.com/v1
# OPENAI_MODEL_NAME=deepseek-chat
```

### 3. 运行框架

**Windows:**
```cmd
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

**直接运行 Python:**
```bash
python main.py
```

## 运行模式

通过设置 `.env` 中的 `RUN_MODE` 环境变量来选择运行模式：

```env
# 交互模式（默认推荐）- 与用户进行实时对话
RUN_MODE=interactive

# 协作模式 - 多智能体自动执行任务
RUN_MODE=autogen

# 直接模式 - 单智能体直接调用
RUN_MODE=direct

# 架构验证 - 检查配置文件完整性
RUN_MODE=architecture
```

## 文件结构

```
agent_framework/
├── main.py                  # 主程序入口
├── loader.py               # Markdown 加载器
├── autogen_config.json     # AutoGen 配置文件
├── agent_architecture.json # 智能体架构配置
├── .env                    # 环境变量配置（需要手动配置）
├── .env.example            # 环境变量示例
├── requirements.txt        # Python 依赖列表
├── run.bat                 # Windows 启动脚本
├── run.sh                  # Linux/Mac 启动脚本
├── test_connection.py      # API 连接测试
└── test_autogen_minimal.py # AutoGen 最小化测试
```

## 配置说明

### autogen_config.json

核心配置文件，包含：
- **llm_config**: LLM 模型配置（从环境变量读取）
- **user_interaction**: 用户交互设置
- **agents**: 智能体列表
- **group_chat_config**: 群聊配置
- **conversation_settings**: 对话设置（欢迎语、退出关键词等）

### agent_architecture.json

智能体架构定义，包含：
- **agents**: 所有智能体的定义
- **phases**: 任务执行阶段
- **interaction_mode**: 交互模式设置

## 故障排查

### 错误：`ModuleNotFoundError: No module named 'autogen'`

解决：安装依赖
```bash
pip install pyautogen
```

### 错误：`Configuration Error: OPENAI_API_KEY not configured`

解决：编辑 `.env` 文件，添加有效的 API 凭证

### 错误：`Connection Failed`

解决：
1. 检查网络连接
2. 验证 `OPENAI_API_BASE` URL 是否正确
3. 确保 API 密钥有效
4. 运行 `python test_connection.py` 测试连接

### 智能体无法创建

解决：
1. 确保相关的 Markdown 人物设定文件存在
2. 检查文件路径是否正确
3. 验证 Markdown 文件格式是否正确

## 扩展指南

### 添加新智能体

1. 在 `autogen_config.json` 中添加新智能体定义
2. 创建对应的 Markdown 人物设定文件
3. 在代码中引用新智能体

### 自定义对话流程

编辑 `main.py` 中的相关函数：
- `run_interactive_mode()` - 自定义交互模式
- `run_autogen_mode()` - 自定义协作模式
- `run_direct()` - 自定义直接模式

### 使用不同的 LLM 提供商

编辑 `.env` 文件中的 API 配置：

```env
# DeepSeek
OPENAI_API_KEY=sk-...
OPENAI_API_BASE=https://api.deepseek.com/v1
OPENAI_MODEL_NAME=deepseek-chat

# Claude (需要 Anthropic SDK)
# OPENAI_API_KEY=sk-ant-...
# OPENAI_API_BASE=https://api.anthropic.com
# OPENAI_MODEL_NAME=claude-3-opus

# Qwen
OPENAI_API_KEY=sk-...
OPENAI_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL_NAME=qwen-plus
```

## 测试

运行提供的测试脚本：

```bash
# 测试 API 连接
python test_connection.py

# 运行最小化 AutoGen 测试
python test_autogen_minimal.py
```

## 环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `OPENAI_API_KEY` | API 密钥 | `sk-...` |
| `OPENAI_API_BASE` | API 端点 URL | `https://api.openai.com/v1` |
| `OPENAI_MODEL_NAME` | 模型名称 | `gpt-4-turbo` |
| `RUN_MODE` | 运行模式 | `interactive` |
| `OTEL_SDK_DISABLED` | 禁用遥测 | `true` |
| `START_PHASE` | 开始阶段 (可选) | `phase-1` |
| `END_PHASE` | 结束阶段 (可选) | `phase-3` |

## 支持的 LLM 模型

框架支持任何 OpenAI 兼容的 API，包括：
- OpenAI (GPT-4, GPT-3.5 等)
- DeepSeek
- Qwen (通义千问)
- Moonshot (月之暗面)
- LongCat
- 自建 vLLM / Ollama 服务
- 等等...

## 许可证

MIT

## 贡献

欢迎提交 Issue 和 Pull Request！

## 注意事项

1. **API 密钥安全**: 不要将实际的 API 密钥提交到版本控制系统
2. **模型选择**: 不同模型有不同的成本和性能，请根据实际需要选择
3. **超时设置**: 对于慢速网络，可能需要增加超时时间
4. **错误处理**: 框架包含完善的错误处理，遇到问题时查看错误信息

## 更新日志

### v1.1 (最新)
- ✅ 完整重构，修复所有导入和 API 兼容性问题
- ✅ 改进错误处理和验证
- ✅ 添加详细的日志输出
- ✅ 创建启动脚本简化使用
- ✅ 增强 Markdown 加载器功能
