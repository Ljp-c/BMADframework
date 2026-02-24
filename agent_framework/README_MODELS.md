# 多模型配置指南

如果您的模型不是 OpenAI 官方的，而是其他兼容 OpenAI 接口的模型（如 DeepSeek、Kimi/Moonshot、阿里通义千问等），请按以下方式配置 `.env` 文件。

## 常见问题：连接超时 (Connection Timeout)

如果您遇到 `ConnectionError` 或 `Timeout`，通常是因为网络问题。

1.  **国内模型**：检查 `OPENAI_API_BASE` 是否正确。有些模型不需要 `/v1` 后缀，有些需要。请参考下方各厂商的文档。
2.  **OpenAI**：如果您在中国大陆访问 OpenAI，**必须**配置代理。

### 配置代理

在 `.env` 文件中添加：

```ini
OPENAI_PROXY=http://127.0.0.1:7890  # 请替换为您本地代理的端口
```

---

## 1. DeepSeek (深度求索)

```ini
OPENAI_API_KEY=sk-xxxxxx
OPENAI_API_BASE=https://api.deepseek.com
OPENAI_MODEL_NAME=deepseek-chat
```

## 2. Moonshot (Kimi)

```ini
OPENAI_API_KEY=sk-xxxxxx
OPENAI_API_BASE=https://api.moonshot.cn/v1
OPENAI_MODEL_NAME=moonshot-v1-8k
```

## 3. DashScope (阿里通义千问)

```ini
OPENAI_API_KEY=sk-xxxxxx
OPENAI_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL_NAME=qwen-plus
```

## 4. SiliconFlow (硅基流动)

```ini
OPENAI_API_KEY=sk-xxxxxx
OPENAI_API_BASE=https://api.siliconflow.cn/v1
OPENAI_MODEL_NAME=deepseek-ai/DeepSeek-V3
```

## 5. Local LLM (本地模型 - Ollama)

```ini
OPENAI_API_KEY=NA
OPENAI_API_BASE=http://localhost:11434/v1
OPENAI_MODEL_NAME=llama3
```

---

**配置完成后，直接运行 `uv run main.py` 即可。**
