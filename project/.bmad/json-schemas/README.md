# JSON Schema 和转换系统

##  系统概述

这是 AUTOGNEN 项目的完整 JSON Schema 定义和文档转换系统。

##  快速开始

### 转换单个文件

```bash
python converters/json_to_markdown.py input.json output.md
```

##  文件结构

```
json-schemas/
 schemas/              # JSON Schema 定义（9 个）
    project-brief-schema.json
    prd-schema.json
    architecture-schema.json
    front-end-architecture-schema.json
    component-specs-schema.json
    data-models-schema.json
    api-reference-schema.json
    tech-stack-schema.json
    environment-schema.json
 converters/          # Python 脚本（3 个）
    json_to_markdown.py
    converter_config.py
    schema_definitions.py
 README.md
```

##  支持的文档类型

1. **Project Brief** - 项目简报
2. **PRD** - 产品需求文档
3. **Architecture** - 系统架构
4. **Front-end Architecture** - 前端架构
5. **Component Specs** - 组件规范
6. **Data Models** - 数据模型
7. **API Reference** - API 参考
8. **Tech Stack** - 技术栈
9. **Environment** - 环境配置

##  工作流

1. 将文档编写为 JSON 格式（遵循相应的 Schema）
2. 使用转换器将 JSON 转换为 Markdown
3. Markdown 文档可用于版本控制和展示

---

**版本:** 1.0  
**最后更新:** 2026-03-30
