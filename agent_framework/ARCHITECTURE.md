# 📐 AutoGen Framework 项目架构详解

## 🎯 项目目标

AutoGen Framework 是一个智能体对话框架，支持用户与多个 AI 智能体进行交互式对话。框架基于 AutoGen-agentchat 库，支持多种 LLM 提供商（OpenAI、DeepSeek 等）。

---

## 📦 项目结构

```
agent_framework/                    ← 你在这个目录
├── 📄 main.py                      (核心入口程序)
├── 📄 loader.py                    (Markdown 加载器)
├── ⚙️  autogen_config.json         (配置文件)
├── 🏗️  agent_architecture.json     (架构定义)
├── 📝 .env                         (环境变量 - 需要配置)
├── 📋 requirements.txt             (Python 依赖)
├── 🚀 run.bat                      (Windows 启动脚本)
├── 🚀 run.sh                       (Linux/Mac 启动脚本)
├── 📖 README.md                    (使用文档)
├── 📖 QUICKSTART.md                (快速开始)
└── 📖 RECONSTRUCTION_REPORT.md     (重构报告)

project/                            ← 项目根目录
├── docs/                           (文档文件)
│   ├── prd.md                      (产品需求文档)
│   ├── architecture.md             (架构文档)
│   └── ...
└── src/                            (源代码)
```

---

## 🔄 执行流程

```
用户运行程序
    ↓
    python main.py
    ↓
┌─────────────────────────────────────────┐
│ main() 函数                             │
│ - 读取 RUN_MODE 环境变量                │
│ - 初始化配置                             │
└─────────────────────────────────────────┘
    ↓
    根据 RUN_MODE 分支：
    ├─→ "interactive" (默认)  ──→ run_interactive_mode_simple()
    ├─→ "test"              ──→ run_test_mode()
    └─→ "architecture"      ──→ architecture_validation()
```

### 交互模式详细流程

```
开始 (RUN_MODE=interactive)
    ↓
加载配置文件
    ├─ autogen_config.json
    └─ .env 环境变量
    ↓
初始化 OpenAI 客户端
    ├─ API_KEY
    ├─ API_BASE
    └─ 模型名称
    ↓
┌─────────────────────────────────────┐
│ 交互循环 (while True)               │
│                                     │
│ 1. 读取用户输入                    │
│ 2. 检查退出条件                    │
│ 3. 调用 OpenAI API                │
│ 4. 显示回复                        │
│                                     │
└─────────────────────────────────────┘
    ↓
用户输入 "exit" 或按 Ctrl+C
    ↓
结束程序
```

---

## 🔑 核心模块说明

### 1️⃣ main.py (主程序)

**职责：**
- 程序入口和控制流
- 配置加载和验证
- 运行模式分发
- 错误处理

**关键函数：**

```python
# 配置相关
load_autogen_config()        # 加载 autogen_config.json
get_llm_config()             # 获取 LLM 配置（支持三级优先级）

# 运行模式
run_interactive_mode_simple()  # 交互对话模式
run_test_mode()                # 测试验证模式
load_architecture_config()     # 加载架构配置

# 主函数
main()                       # 程序入口，分发到不同模式
```

**优先级逻辑（get_llm_config）：**

```
最高优先级：.env 环境变量
    ↓ (如果不存在)
中等优先级：autogen_config.json
    ↓ (如果不存在)
最低优先级：内置默认值
    ↓ (如果仍不存在)
抛出 ValueError 异常
```

### 2️⃣ loader.py (Markdown 加载器)

**职责：**
- 读取 Markdown 文件
- 解析人物设定
- 解析任务描述
- 章节提取

**关键类和方法：**

```python
class MarkdownLoader:
    @staticmethod
    def load_file(path)          # 读取文件内容
    @staticmethod
    def parse_persona(path)      # 解析人物设定
    @staticmethod
    def parse_task(path)         # 解析任务描述
    @staticmethod
    def _extract_section(...)    # 提取 Markdown 章节
```

**人物设定文件格式：**

```markdown
# 角色名称

## Goal
目标描述

## Backstory
背景故事
```

**任务文件格式：**

```markdown
# 任务名称

任务描述内容

## Output
期望输出
```

### 3️⃣ 配置文件

#### autogen_config.json

```json
{
  "llm_config": {
    "model": "LongCat-Flash-Thinking",
    "api_key": null,              // 从 .env 读取
    "base_url": "https://...",    // 从 .env 读取
    "timeout": 120,
    "temperature": 0.7,
    "max_tokens": 2048
  },
  
  "user_interaction": {
    "enabled": true,
    "human_input_mode": "ALWAYS",
    "max_consecutive_auto_reply": 10
  },
  
  "agents": [...],                // 智能体定义
  
  "group_chat_config": {          // 群聊配置
    "max_round": 20
  },
  
  "conversation_settings": {      // 对话设置
    "welcome_message": "...",
    "termination_keywords": [...]
  }
}
```

#### .env 文件

```env
# 必填项
OPENAI_API_KEY=sk-...              # API 密钥
OPENAI_API_BASE=https://api...     # API 端点

# 可选项
OPENAI_MODEL_NAME=model-name       # 模型名称
RUN_MODE=interactive               # 运行模式
OTEL_SDK_DISABLED=true             # 禁用遥测
```

---

## 🔌 API 通信流程

```
┌──────────────┐
│   用户输入   │  "你好"
└──────┬───────┘
       ↓
┌──────────────────────────────────────┐
│  OpenAI 客户端                       │
│  (来自 openai 库)                    │
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│  HTTP 请求 (使用 httpx)              │
│  POST https://api.*.com/v1/chat      │
│  Headers: Authorization: Bearer ...  │
│  Body: {                             │
│    "model": "...",                   │
│    "messages": [...],                │
│    "temperature": 0.7,               │
│    "max_tokens": 500                 │
│  }                                   │
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│  LLM 处理                            │
│  (GPT-4, DeepSeek, Qwen 等)         │
└──────┬───────────────────────────────┘
       ↓
┌──────────────────────────────────────┐
│  API 响应                            │
│  {                                   │
│    "choices": [{                     │
│      "message": {                    │
│        "content": "回复内容..."      │
│      }                               │
│    }]                                │
│  }                                   │
└──────┬───────────────────────────────┘
       ↓
┌──────────────────┐
│  显示给用户      │
│  "🤖 Assistant: ..."
└──────────────────┘
```

---

## 🌳 类和函数树

```
📁 main.py
├── load_autogen_config(dir)
│   └─ 加载 JSON 配置文件
├── get_llm_config(config)
│   ├─ 环境变量优先
│   ├─ 配置文件次之
│   └─ 内置默认值最后
├── run_test_mode()
│   ├─ 检查导入
│   ├─ 加载配置
│   ├─ 初始化 API 客户端
│   └─ 验证 Agent API
├── run_interactive_mode_simple()
│   ├─ 加载配置
│   ├─ 初始化客户端
│   └─ 交互循环
│       ├─ 读取输入
│       ├─ 检查退出
│       └─ 调用 API
├── load_architecture_config(root)
├── validate_architecture_files()
├── print_architecture_summary()
└── main()
    ├─ 读取 RUN_MODE
    └─ 分支处理

📁 loader.py
└── class MarkdownLoader
    ├── load_file(path)
    ├── parse_persona(path)
    ├── parse_task(path)
    └── _extract_section(content, name, default)
```

---

## 🔐 错误处理层级

```
第 1 层：导入错误
├─ ImportError: autogen 未安装
├─ ImportError: openai 未安装
└─ ImportError: python-dotenv 未安装
   ↓
   提示用户安装，程序退出

第 2 层：配置错误
├─ FileNotFoundError: 配置文件不存在
├─ JSONDecodeError: JSON 格式错误
├─ ValueError: OPENAI_API_KEY 未配置
└─ ValueError: OPENAI_API_BASE 未配置
   ↓
   显示错误信息，建议用户修复

第 3 层：运行时错误
├─ KeyboardInterrupt: 用户按 Ctrl+C
├─ ConnectionError: API 连接失败
├─ TimeoutError: 请求超时
└─ Exception: 其他异常
   ↓
   捕获并显示友好的错误信息
```

---

## 📊 数据流

```
输入数据流：
  .env 环境变量
    ↓
  autogen_config.json
    ↓
  Markdown 文件 (personas, tasks)
    ↓
  用户输入
    ↓
  OpenAI API

输出数据流：
  OpenAI API 响应
    ↓
  处理和提取
    ↓
  显示给用户
    ↓
  保存到对话历史（可选）
```

---

## 🎛️ 运行模式详解

### interactive (交互模式) - 默认

```
特点：
  ✅ 支持多轮对话
  ✅ 实时与 AI 交互
  ✅ 简单易用
  
启动：
  python main.py
  或 RUN_MODE=interactive python main.py
  
交互示例：
  👤 You: 你好
  🤔 Thinking...
  🤖 Assistant: 你好！我是一个 AI 助手...
  👤 You: exit
  👋 Goodbye!
```

### test (测试模式)

```
特点：
  ✅ 验证所有依赖
  ✅ 测试 API 连接
  ✅ 检查配置有效性
  
启动：
  RUN_MODE=test python main.py
  
输出：
  ✓ All imports successful
  ✓ AutoGen config loaded
  ✓ LLM config loaded
  ✓ OpenAI client initialized
  ✓ All tests passed!
```

### architecture (架构模式)

```
特点：
  ✅ 检查文件完整性
  ✅ 验证配置引用
  ✅ 显示架构摘要
  
启动：
  RUN_MODE=architecture python main.py
  
输出：
  📊 Architecture Summary
    Agents: 6
    Phases: 5
    - phase-1: ...
    - phase-2: ...
```

---

## 🔧 配置优先级示例

**场景：** 需要切换到 DeepSeek API

```
1. 编辑 .env 文件：
   OPENAI_API_KEY=sk-deepseek-key
   OPENAI_API_BASE=https://api.deepseek.com/v1
   OPENAI_MODEL_NAME=deepseek-chat

2. 程序加载配置时：
   ✓ 优先读取环境变量（.env）
   ✓ 如果 .env 中有值，就不读 config.json
   ✓ 如果都没有，使用内置默认值

3. 启动程序：
   python main.py
   ✓ 使用 DeepSeek API
```

---

## 📈 扩展点

### 1. 添加新的运行模式

```python
# 在 main() 中添加新的 elif 分支：
elif run_mode == "my_mode":
    run_my_custom_mode()

# 实现新的模式函数：
def run_my_custom_mode():
    # 你的逻辑
    pass
```

### 2. 添加新的 LLM 提供商

```env
# 只需修改 .env：
OPENAI_API_KEY=your-api-key
OPENAI_API_BASE=https://your-api.com/v1
OPENAI_MODEL_NAME=your-model
```

### 3. 自定义 Markdown 解析

```python
# 在 loader.py 中添加新的解析方法：
@staticmethod
def parse_custom_format(file_path):
    content = MarkdownLoader.load_file(file_path)
    # 自定义解析逻辑
    return {...}
```

---

## 🎓 学习路径

1. **理解项目结构**
   - 查看本文件和 `README.md`

2. **学习配置**
   - 查看 `autogen_config.json` 和 `.env.example`

3. **理解代码**
   - `main.py` - 从 `main()` 函数开始
   - `loader.py` - 学习 Markdown 解析

4. **尝试运行**
   - `python main.py` - 交互模式
   - `RUN_MODE=test python main.py` - 测试模式

5. **扩展功能**
   - 自定义运行模式
   - 添加新的 Markdown 解析器
   - 集成新的 LLM 提供商

---

**创建时间：** 2026年2月26日  
**框架版本：** 1.1  
**最后更新：** 2026年2月26日

2026.3.6 完成vibe coding 智能体架构的创建
下一步 检查main.py 观看这个架构是否正确
2026.3.16 main.py 基本检查完成 到step7
下一步 继续完成main.py 