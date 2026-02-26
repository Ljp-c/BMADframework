# 🚀 快速开始指南

## 重构完成！框架现在可以正常运行

### ⚡ 3 步快速开始

#### 1️⃣ 配置 API 密钥

编辑 `.env` 文件：

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4-turbo
RUN_MODE=interactive
```

**示例配置（其他 API 提供商）：**

**DeepSeek:**
```env
OPENAI_API_KEY=sk-xxx
OPENAI_API_BASE=https://api.deepseek.com/v1
OPENAI_MODEL_NAME=deepseek-chat
```

**Qwen (阿里云):**
```env
OPENAI_API_KEY=sk-xxx
OPENAI_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL_NAME=qwen-plus
```

#### 2️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

或双击 `run.bat` (Windows) 会自动安装。

#### 3️⃣ 运行框架

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

### 🧪 验证框架

```bash
# 测试模式 - 检查所有配置
python main.py
# 直接测试，或在 .env 中设置：
# RUN_MODE=test
# python main.py
```

### 📋 运行模式

**交互模式**（默认）- 与 AI 对话：
```env
RUN_MODE=interactive
```
然后运行 `python main.py`，输入问题进行对话。输入 `exit` 或 `quit` 退出。

**测试模式** - 验证配置：
```env
RUN_MODE=test
```
运行 `python main.py` 会自动测试所有组件。

**架构模式** - 检查文件完整性：
```env
RUN_MODE=architecture
```

### 🔧 文件说明

| 文件 | 说明 | 状态 |
|------|------|------|
| `main.py` | 主程序 | ✅ 已重写 |
| `loader.py` | Markdown 加载器 | ✅ 已改进 |
| `autogen_config.json` | 配置文件 | ✅ 已修复 |
| `.env` | 环境变量 | ✅ 已更新 |
| `requirements.txt` | 依赖列表 | ✅ 已创建 |
| `run.bat/sh` | 启动脚本 | ✅ 已创建 |
| `README.md` | 完整文档 | ✅ 已创建 |

### ✨ 新功能

- ✅ 支持新版 AutoGen (v0.7.5+) API
- ✅ 多个 LLM 提供商支持
- ✅ 完善的错误处理
- ✅ 自动依赖检查安装
- ✅ 详细的日志输出
- ✅ 简单的交互界面

### ⚠️ 常见问题

**Q: 框架无法导入 autogen？**
A: 运行 `pip install pyautogen`

**Q: API 连接失败？**
A: 
1. 检查 `.env` 中 OPENAI_API_KEY 是否正确
2. 验证 OPENAI_API_BASE URL 是否正确
3. 确保网络连接正常

**Q: 模型不存在？**
A: 检查 OPENAI_MODEL_NAME 在你的 API 提供商上是否可用

**Q: 想要详细文档？**
A: 查看 `README.md` 和 `RECONSTRUCTION_REPORT.md`

### 📚 下一步

1. 编辑 `.env` 配置你的 API
2. 运行框架进行交互
3. 查看 README.md 了解更多高级功能
4. 根据需要定制对话流程

---

**现在就开始吧！** 🎉

```bash
python main.py
```

输入任何问题或请求，享受与 AI 的交互吧！

需要帮助？查看：
- `README.md` - 完整使用指南
- `RECONSTRUCTION_REPORT.md` - 重构详情
- 相关文件中的注释
