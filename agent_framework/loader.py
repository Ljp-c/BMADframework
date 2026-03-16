# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    Markdown 文件加载器 (MarkdownLoader)                      ║
║                                                                              ║
║  功能：解析和加载 Markdown 格式的人物设定和任务文件                          ║
║  用途：为 AutoGen 智能体提供人物背景、目标、任务描述等信息                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────────────┐
│ 主要功能                                                                      │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. load_file() ................ 读取 Markdown 文件内容                    │
│  2. parse_persona() ............ 解析智能体人物设定文件                    │
│  3. parse_task() ............... 解析任务描述文件                           │
│  4. _extract_section() ......... 提取 Markdown 中的特定章节                │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────┐
│ 文件格式规范                                                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│ 🎭 人物设定文件 (persona.md) 预期格式：                                      │
│                                                                              │
│    # Product Manager                                                        │
│    这是第一行标题，作为角色名称                                            │
│                                                                              │
│    ## Goal                                                                  │
│    编写完整的产品需求文档，确保所有功能需求都被详细记录。                  │
│                                                                              │
│    ## Backstory                                                             │
│    你是一位经验丰富的产品经理，有 10 年的产品开发经验...                   │
│                                                                              │
│ ────────────────────────────────────────────────────────────────────────────│
│                                                                              │
│ 📋 任务文件 (task.md) 预期格式：                                             │
│                                                                              │
│    # Create PRD (产品需求文档)                                              │
│    根据项目简述和用户反馈，创建完整的产品需求文档。                        │
│                                                                              │
│    ## Output                                                                │
│    一份包含功能列表、用户故事和技术要求的 Markdown 文档。                   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
"""
import os
import re
from typing import Dict, Any, Optional


class MarkdownLoader:
    """
    Markdown 文件加载器类
    
    用途：
      - 从 Markdown 文件中提取结构化信息
      - 支持智能体人物设定和任务定义的解析
      - 提供灵活的章节提取功能
    
    使用示例：
      # 加载人物设定
      persona = MarkdownLoader.parse_persona('project/.bmad/personas/pm.md')
      print(persona['role'])      # 'Product Manager'
      print(persona['goal'])      # 目标描述
      print(persona['backstory']) # 背景故事
      
      # 加载任务
      task = MarkdownLoader.parse_task('project/.bmad/tasks/prd-task.md')
      print(task['description'])   # 任务描述
      print(task['expected_output']) # 期望输出
    """
    
    @staticmethod
    def load_file(file_path: str) -> str:
        """
        📖 读取 Markdown 文件内容
        
        功能：
          - 安全地打开和读取 Markdown 文件
          - 处理文件不存在的情况
          - 使用 UTF-8 编码确保中文支持
        
        参数：
          file_path (str): 要读取的文件路径（绝对或相对路径）
        
        返回值：
          str: 文件的完整内容
        
        异常：
          FileNotFoundError: 当文件不存在时
          IOError: 当文件读取失败时
        
        示例：
          content = MarkdownLoader.load_file('personas/pm.md')
          print(len(content))  # 文件字符数
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error loading file {file_path}: {str(e)}")
            raise

    @staticmethod
    def parse_persona(file_path: str) -> Dict[str, str]:
        """
        🎭 解析人物设定 Markdown 文件
        
        从人物设定文件中提取以下信息：
          - role: 角色名称（来自第一个 # 标题）
          - goal: 角色的目标（## Goal 章节）
          - backstory: 角色的背景故事（## Backstory 章节）
        
        参数：
          file_path (str): 人物设定 Markdown 文件的路径
        
        返回值：
          dict: 包含 'role'、'goal'、'backstory' 的字典
        
        错误处理：
          - 如果文件不存在，返回默认值而不是抛出异常
          - 如果缺少某些章节，使用合理的默认值
        
        示例：
          persona = MarkdownLoader.parse_persona('pm.md')
          # 返回：{
          #   'role': 'Product Manager',
          #   'goal': '编写完整的产品需求文档...',
          #   'backstory': '你是一位经验丰富的产品经理...'
          # }
        """
        try:
            content = MarkdownLoader.load_file(file_path)
            lines = content.split('\n')
            
            # 提取角色名称：从第一个 # 标题中获取
            role_name = "Unknown Role"
            for line in lines:
                if line.startswith('#') and not line.startswith('##'):
                    role_name = line.replace('#', '').strip()
                    break
            #提取目标的角色定义
            role_define = MarkdownLoader._extract_section(content, "角色定义", 
                                                    "按照角色名字定义完成任务.")
            # 输出目标和背景故事
            Core_responsibilities = MarkdownLoader._extract_section(content, "核心职责", 
                                                    "完成指派任务，确保成果高质量交付.")
            
            Output = MarkdownLoader._extract_section(content, "输出物",
                                                     "根据任务要求输出结果，确保满足预期目标.")
            #技能要求以及协作关系
            tech_requirements = MarkdownLoader._extract_section(content, "技能要求",
                                                     "具备相关领域的专业知识和技能，能够高效完成任务.")
            
            collaboration = MarkdownLoader._extract_section(content, "协作关系",
                                                     "与其他智能体或人类协作，确保任务顺利完成.")
            #工作原则以及决策权限
            work_principles = MarkdownLoader._extract_section(content, "工作原则",
                                                     "遵循高效、协作和创新的工作原则，确保任务高质量完成.") 
            decision_authority = MarkdownLoader._extract_section(content, "决策权限",
                                                     "在完成任务过程中拥有一定的决策权限，能够自主解决问题.")


            return {
                "role": role_name,
                "role_define": role_define,
                "Core_responsibilities": Core_responsibilities,
                "Output": Output,
                "tech_requirements": tech_requirements,
                "collaboration": collaboration,
                "work_principles": work_principles,
                "decision_authority": decision_authority
            }
        except Exception as e:
            print(f"Error parsing persona file {file_path}: {str(e)}")
            # 返回默认值而不是抛出异常，确保程序继续运行
            return {
                "role": "Unknown Agent",
                "role_define": "Unknown role definition",
                "Core_responsibilities": "Unknown core responsibilities",
                "Output": "Unknown output specification",
                "tech_requirements": "Unknown technical requirements",
                "collaboration": "Unknown collaboration details",
                "work_principles": "Unknown work principles",
                "decision_authority": "Unknown decision authority"
            }

    @staticmethod
    def parse_task(file_path: str) -> Dict[str, str]:
        """
        📋 解析任务描述 Markdown 文件
        
        从任务文件中提取以下信息：
          - description: 任务描述（主体内容）
          - expected_output: 期望的输出格式（## Output 章节）
        
        参数：
          file_path (str): 任务描述 Markdown 文件的路径
        
        返回值：
          dict: 包含 'description'、'expected_output' 的字典
        
        错误处理：
          - 如果文件不存在，返回默认值
          - 如果缺少 Output 章节，使用默认值
        
        示例：
          task = MarkdownLoader.parse_task('prd-task.md')
          # 返回：{
          #   'description': '根据项目简述创建...',
          #   'expected_output': '一份包含功能列表的文档...'
          # }
        """
        try:
            content = MarkdownLoader.load_file(file_path)
            
            # 提取描述：## 之前的所有内容
            description = content
            sections = content.split('##')
            if len(sections) > 1:
                description = sections[0].strip()
            #任务描述以及角色执行者
            role_executed_by = MarkdownLoader._extract_section(content, "角色执行者",
                                                     "The role that executes this task.")
            task_description = MarkdownLoader._extract_section(content, "任务描述",
                                                     "Detailed description of the task to be completed.")
            #输入以及输出
            iNput = MarkdownLoader._extract_section(content, "输入",
                                                     "Specific input requirements for the task, if any.")

            oUtput = MarkdownLoader._extract_section(content, "输出",
                                                     "Specific output requirements for the task, if any.")
            #执行步骤
            execution_steps = MarkdownLoader._extract_section(content, "执行步骤",
                                                     "Step-by-step instructions for completing the task.")

            # 质量检查清单以及交付验收标准
            quality_checklist = MarkdownLoader._extract_section(content, "质量检查清单",
                                                     "A checklist to ensure the quality of the output.")
            acceptance_criteria = MarkdownLoader._extract_section(content, "交付验收标准",
                                                     "Criteria that the output must meet for acceptance.")

            return {
                "description": description,
                "role_executed_by": role_executed_by,
                "task_description": task_description,
                "input": iNput,
                "output": oUtput,
                "execution_steps": execution_steps,
                "quality_checklist": quality_checklist,
                "acceptance_criteria": acceptance_criteria
            }
        except Exception as e:
            print(f"Error parsing task file {file_path}: {str(e)}")
            return {
                "description": "Unable to load task description",
                "expected_output": "Expected output not specified"
            }
    @staticmethod
    def parse_checklist(file_path: str) -> Dict[str, str]:
        """
        ✅ 解析检查清单 Markdown 文件
        
        从检查清单文件中提取以下信息：
          - checklist: 检查清单内容（主体内容）
        参数：
          file_path (str): 检查清单 Markdown 文件的路径
        返回值：
          dict: 包含 'checklist' 的字典
        错误处理：
          - 如果文件不存在，返回默认值
        示例：
          checklist = MarkdownLoader.parse_checklist('checklist.md')
          # 返回：{
          #   'checklist': '1. 确认需求完整...\n2. 确保输出格式正确...'
          # }
        """
        try:
            content = MarkdownLoader.load_file(file_path)
            sections = content.split('##')
            if len(sections) > 1:
                return {
                    "checklist": sections
                }
        except Exception as e:
            print(f"Error parsing checklist file {file_path}: {str(e)}")
            return {
                "checklist": "Unable to load checklist"
            }






    @staticmethod
    def _extract_section(content: str, section_name: str, default: str = "") -> str:
        """
        🔍 从 Markdown 内容中提取特定章节
        
        使用正则表达式查找以 ## 开头的章节。
        
        工作原理：
          1. 查找以 ## 开头，后跟章节名称的行（不区分大小写）
          2. 提取该章节下的所有内容
          3. 直到遇到下一个 ## 章节或文件末尾
        
        参数：
          content (str): Markdown 文件的完整内容
          section_name (str): 要查找的章节名称（如 'goal'、'output'）
          default (str): 如果找不到该章节，返回的默认值
        
        返回值：
          str: 提取的章节内容或默认值
        
        示例：
          content = '''# Agent
          
          ## Goal
          This is the goal section.
          
          ## Backstory
          This is backstory.
          '''
          
          goal = MarkdownLoader._extract_section(content, "goal")
          # 返回：'This is the goal section.'
        
        技术说明：
          - 使用正则表达式 r"##\\s*{section_name}\\s*\\n(.*?)(?=##|$)"
          - re.IGNORECASE：不区分大小写（Goal、goal、GOAL 都能匹配）
          - re.DOTALL：. 也匹配换行符，允许多行提取
        """
        try:
            # 创建正则表达式模式
            # ## 后面跟空格、章节名、换行符、然后捕获内容直到下一个 ##
            pattern = rf"##\s*{section_name}\s*\n(.*?)(?=##|$)"
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            
            if match:
                return match.group(1).strip()
            return default
        except Exception:
            # 正则表达式错误时返回默认值
            return default


