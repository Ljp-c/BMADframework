#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目简报生成器 - 从 JSON 生成 Markdown 文档
严格按照 JSON Schema 结构读取数据
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional


class ProjectBriefGenerator:
    """项目简报生成器类"""
    
    def __init__(self, json_file: str):
        """
        初始化生成器
        
        Args:
            json_file: JSON 文件路径
        """
        self.json_file = json_file
        self.data = self._load_json()
        
    def _load_json(self) -> Dict[str, Any]:
        """加载并验证 JSON 文件"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ 成功加载 JSON 文件: {self.json_file}")
            return data
        except FileNotFoundError:
            print(f"❌ 错误: 文件 '{self.json_file}' 不存在")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ 错误: JSON 格式错误 - {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ 错误: {e}")
            sys.exit(1)
    
    def _safe_get(self, *keys, default="[数据缺失]"):
        """
        安全获取嵌套字典的值
        
        Args:
            *keys: 键的路径
            default: 默认值
        """
        try:
            value = self.data
            for key in keys:
                value = value[key]
            return value if value is not None else default
        except (KeyError, TypeError):
            print(f"⚠️  警告: 无法找到路径 {' -> '.join(str(k) for k in keys)}")
            return default
    
    def generate_markdown(self) -> str:
        """生成完整的 Markdown 文档"""
        sections = []
        
        # 添加文档头部
        sections.append(self._generate_header())
        
        # 1. 项目概述
        sections.append(self._generate_section_1_overview())
        
        # 2. 项目目标
        sections.append(self._generate_section_2_objectives())
        
        # 3. 项目范围
        sections.append(self._generate_section_3_scope())
        
        # 4. 利益相关者
        sections.append(self._generate_section_4_stakeholders())
        
        # 5. 约束条件
        sections.append(self._generate_section_5_constraints())
        
        # 6. 假设条件
        sections.append(self._generate_section_6_assumptions())
        
        # 7. 风险识别
        sections.append(self._generate_section_7_risks())
        
        # 8. 关键里程碑
        sections.append(self._generate_section_8_milestones())
        
        # 9. 审批记录
        sections.append(self._generate_section_9_approvals())
        
        return '\n\n'.join(sections)
    
    def _generate_header(self) -> str:
        """生成文档头部"""
        return "# 项目简报"
    
    def _generate_section_1_overview(self) -> str:
        """生成 1. 项目概述"""
        try:
            # 从 step6 -> 按模板结构编写 -> data -> 项目概述
            overview = self.data['step6_编写项目简报']['按模板结构编写']['data']['项目概述']
            
            project_name = overview.get('项目名称', '[项目名称]')
            background = overview.get('项目背景', '[描述项目产生的背景和原因]')
            problem = overview.get('问题陈述', '[清晰描述要解决的业务问题]')
            
            return f"""## 1. 项目概述

### 项目名称
{project_name}

### 项目背景
{background}

### 问题陈述
{problem}"""
        except KeyError as e:
            print(f"⚠️  警告: 项目概述数据缺失 - {e}")
            return """## 1. 项目概述

### 项目名称
[项目名称]

### 项目背景
[描述项目产生的背景和原因]

### 问题陈述
[清晰描述要解决的业务问题]"""
    
    def _generate_section_2_objectives(self) -> str:
        """生成 2. 项目目标"""
        try:
            objectives = self.data['step6_编写项目简报']['按模板结构编写']['data']['项目目标']
            
            # 主要目标
            main_goals = objectives.get('主要目标', [])
            if main_goals:
                goals_list = '\n'.join([f"- {goal}" for goal in main_goals])
            else:
                goals_list = "- [目标1]\n- [目标2]\n- [目标3]"
            
            # 成功标准
            success_criteria = objectives.get('成功标准', [])
            if success_criteria:
                criteria_rows = []
                for criterion in success_criteria:
                    standard = criterion.get('标准', '[标准]')
                    measure = criterion.get('衡量方式', '[如何衡量]')
                    target = criterion.get('目标值', '[目标值]')
                    criteria_rows.append(f"| {standard} | {measure} | {target} |")
                criteria_table = '\n'.join(criteria_rows)
            else:
                criteria_table = "| [标准1] | [如何衡量] | [目标值] |\n| [标准2] | [如何衡量] | [目标值] |"
            
            return f"""## 2. 项目目标

### 主要目标
{goals_list}

### 成功标准
| 标准 | 衡量方式 | 目标值 |
|------|----------|--------|
{criteria_table}"""
        except KeyError as e:
            print(f"⚠️  警告: 项目目标数据缺失 - {e}")
            return """## 2. 项目目标

### 主要目标
- [目标1]
- [目标2]
- [目标3]

### 成功标准
| 标准 | 衡量方式 | 目标值 |
|------|----------|--------|
| [标准1] | [如何衡量] | [目标值] |
| [标准2] | [如何衡量] | [目标值] |"""
    
    def _generate_section_3_scope(self) -> str:
        """生成 3. 项目范围"""
        try:
            scope = self.data['step6_编写项目简报']['按模板结构编写']['data']['项目范围']
            
            # 范围内
            in_scope = scope.get('范围内', [])
            if in_scope:
                in_scope_list = '\n'.join([f"- {item}" for item in in_scope])
            else:
                in_scope_list = "- [功能/模块1]\n- [功能/模块2]"
            
            # 范围外
            out_scope = scope.get('范围外', [])
            if out_scope:
                out_scope_list = '\n'.join([f"- {item}" for item in out_scope])
            else:
                out_scope_list = "- [排除项1]\n- [排除项2]"
            
            return f"""## 3. 项目范围

### 范围内
{in_scope_list}

### 范围外
{out_scope_list}"""
        except KeyError as e:
            print(f"⚠️  警告: 项目范围数据缺失 - {e}")
            return """## 3. 项目范围

### 范围内
- [功能/模块1]
- [功能/模块2]

### 范围外
- [排除项1]
- [排除项2]"""
    
    def _generate_section_4_stakeholders(self) -> str:
        """生成 4. 利益相关者"""
        try:
            stakeholders = self.data['step6_编写项目简报']['按模板结构编写']['data']['利益相关者']
            
            if stakeholders:
                rows = []
                for sh in stakeholders:
                    role = sh.get('角色', '[角色]')
                    name = sh.get('姓名', '[姓名]')
                    duty = sh.get('职责', '[职责]')
                    contact = sh.get('联系方式', '[联系方式]')
                    rows.append(f"| {role} | {name} | {duty} | {contact} |")
                table = '\n'.join(rows)
            else:
                table = "| [角色] | [姓名] | [职责] | [联系方式] |"
            
            return f"""## 4. 利益相关者

| 角色 | 姓名 | 职责 | 联系方式 |
|------|------|------|----------|
{table}"""
        except KeyError as e:
            print(f"⚠️  警告: 利益相关者数据缺失 - {e}")
            return """## 4. 利益相关者

| 角色 | 姓名 | 职责 | 联系方式 |
|------|------|------|----------|
| [角色] | [姓名] | [职责] | [联系方式] |"""
    
    def _generate_section_5_constraints(self) -> str:
        """生成 5. 约束条件"""
        try:
            constraints = self.data['step6_编写项目简报']['按模板结构编写']['data']['约束条件']
            
            time_constraint = constraints.get('时间约束', '[描述时间限制]')
            budget_constraint = constraints.get('预算约束', '[描述预算限制]')
            tech_constraint = constraints.get('技术约束', '[描述技术限制]')
            resource_constraint = constraints.get('资源约束', '[描述资源限制]')
            
            return f"""## 5. 约束条件

### 时间约束
{time_constraint}

### 预算约束
{budget_constraint}

### 技术约束
{tech_constraint}

### 资源约束
{resource_constraint}"""
        except KeyError as e:
            print(f"⚠️  警告: 约束条件数据缺失 - {e}")
            return """## 5. 约束条件

### 时间约束
[描述时间限制]

### 预算约束
[描述预算限制]

### 技术约束
[描述技术限制]

### 资源约束
[描述资源限制]"""
    
    def _generate_section_6_assumptions(self) -> str:
        """生成 6. 假设条件"""
        try:
            assumptions = self.data['step6_编写项目简报']['按模板结构编写']['data']['假设条件']
            
            if assumptions:
                assumptions_list = '\n'.join([f"- {assumption}" for assumption in assumptions])
            else:
                assumptions_list = "- [假设1]\n- [假设2]\n- [假设3]"
            
            return f"""## 6. 假设条件

{assumptions_list}"""
        except KeyError as e:
            print(f"⚠️  警告: 假设条件数据缺失 - {e}")
            return """## 6. 假设条件

- [假设1]
- [假设2]
- [假设3]"""
    
    def _generate_section_7_risks(self) -> str:
        """生成 7. 风险识别"""
        try:
            risks = self.data['step6_编写项目简报']['按模板结构编写']['data']['风险识别']
            
            if risks:
                rows = []
                for risk in risks:
                    risk_desc = risk.get('风险', '[风险描述]')
                    probability = risk.get('可能性', '高/中/低')
                    impact = risk.get('影响', '高/中/低')
                    mitigation = risk.get('缓解措施', '[缓解措施]')
                    rows.append(f"| {risk_desc} | {probability} | {impact} | {mitigation} |")
                table = '\n'.join(rows)
            else:
                table = "| [风险描述] | 高/中/低 | 高/中/低 | [缓解措施] |"
            
            return f"""## 7. 风险识别

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
{table}"""
        except KeyError as e:
            print(f"⚠️  警告: 风险识别数据缺失 - {e}")
            return """## 7. 风险识别

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|----------|
| [风险描述] | 高/中/低 | 高/中/低 | [缓解措施] |"""
    
    def _generate_section_8_milestones(self) -> str:
        """生成 8. 关键里程碑"""
        try:
            milestones = self.data['step6_编写项目简报']['按模板结构编写']['data']['关键里程碑']
            
            if milestones:
                rows = []
                for milestone in milestones:
                    name = milestone.get('里程碑', '[里程碑名称]')
                    date = milestone.get('日期', '[日期]')
                    deliverable = milestone.get('交付物', '[交付物]')
                    rows.append(f"| {name} | {date} | {deliverable} |")
                table = '\n'.join(rows)
            else:
                table = "| [里程碑名称] | [日期] | [交付物] |"
            
            return f"""## 8. 关键里程碑

| 里程碑 | 日期 | 交付物 |
|--------|------|--------|
{table}"""
        except KeyError as e:
            print(f"⚠️  警告: 关键里程碑数据缺失 - {e}")
            return """## 8. 关键里程碑

| 里程碑 | 日期 | 交付物 |
|--------|------|--------|
| [里程碑名称] | [日期] | [交付物] |"""
    
    def _generate_section_9_approvals(self) -> str:
        """生成 9. 审批记录"""
        try:
            approvals = self.data['step6_编写项目简报']['按模板结构编写']['data']['审批记录']
            
            if approvals:
                rows = []
                for approval in approvals:
                    role = approval.get('角色', '[角色]')
                    name = approval.get('姓名', '[姓名]')
                    date = approval.get('日期', '[日期]')
                    signature = approval.get('签名', '[签名]')
                    rows.append(f"| {role} | {name} | {date} | {signature} |")
                table = '\n'.join(rows)
            else:
                table = "| [角色] | [姓名] | [日期] | [签名] |"
            
            return f"""## 9. 审批记录

| 角色 | 姓名 | 日期 | 签名 |
|------|------|------|------|
{table}"""
        except KeyError as e:
            print(f"⚠️  警告: 审批记录数据缺失 - {e}")
            return """## 9. 审批记录

| 角色 | 姓名 | 日期 | 签名 |
|------|------|------|------|
| [角色] | [姓名] | [日期] | [签名] |"""
    
    def save_to_file(self, output_file: str) -> None:
        """
        保存 Markdown 文档到文件
        
        Args:
            output_file: 输出文件路径
        """
        print("\n" + "="*60)
        print("开始生成项目简报...")
        print("="*60 + "\n")
        
        markdown_content = self.generate_markdown()
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            file_size = Path(output_file).stat().st_size
            print("\n" + "="*60)
            print(f"✅ 项目简报生成成功！")
            print(f"📄 文件路径: {output_file}")
            print(f"📊 文件大小: {file_size} bytes")
            print("="*60 + "\n")
        except Exception as e:
            print(f"\n❌ 保存文件时出错: {e}\n")
            sys.exit(1)
    
    def print_data_structure(self) -> None:
        """打印 JSON 数据结构（调试用）"""
        print("\n" + "="*60)
        print("JSON 数据结构:")
        print("="*60)
        
        def print_keys(d, indent=0):
            if isinstance(d, dict):
                for key, value in d.items():
                    print("  " * indent + f"- {key}")
                    if isinstance(value, (dict, list)) and value:
                        print_keys(value, indent + 1)
            elif isinstance(d, list) and d:
                print("  " * indent + f"[列表，{len(d)} 项]")
                if isinstance(d[0], dict):
                    print_keys(d[0], indent + 1)
        
        print_keys(self.data)
        print("="*60 + "\n")
    
    def validate_structure(self) -> bool:
        """验证 JSON 结构完整性"""
        print("\n" + "="*60)
        print("验证 JSON 结构...")
        print("="*60 + "\n")
        
        required_paths = [
            ['step6_编写项目简报', '按模板结构编写', 'data', '项目概述'],
            ['step6_编写项目简报', '按模板结构编写', 'data', '项目目标'],
            ['step6_编写项目简报', '按模板结构编写', 'data', '项目范围'],
            ['step6_编写项目简报', '按模板结构编写', 'data', '利益相关者'],
            ['step6_编写项目简报', '按模板结构编写', 'data', '约束条件'],
            ['step6_编写项目简报', '按模板结构编写', 'data', '假设条件'],
            ['step6_编写项目简报', '按模板结构编写', 'data', '风险识别'],
            ['step6_编写项目简报', '按模板结构编写', 'data', '关键里程碑'],
            ['step6_编写项目简报', '按模板结构编写', 'data', '审批记录'],
        ]
        
        all_valid = True
        for path in required_paths:
            try:
                value = self.data
                for key in path:
                    value = value[key]
                print(f"✅ {' -> '.join(path)}")
            except KeyError:
                print(f"❌ {' -> '.join(path)} [缺失]")
                all_valid = False
        
        print("\n" + "="*60)
        if all_valid:
            print("✅ 所有必需字段都存在")
        else:
            print("⚠️  部分字段缺失，将使用默认值")
        print("="*60 + "\n")
        
        return all_valid


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='从 JSON 数据生成项目简报 Markdown 文档',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python generate_brief.py input.json
  python generate_brief.py input.json -o output.md
  python generate_brief.py input.json --validate
  python generate_brief.py input.json --debug
        """
    )
    
    parser.add_argument(
        'input_file',
        help='输入的 JSON 文件路径'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='项目简报.md',
        help='输出的 Markdown 文件路径 (默认: 项目简报.md)'
    )
    
    parser.add_argument(
        '--validate',
        action='store_true',
        help='验证 JSON 结构完整性'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='显示 JSON 数据结构（调试模式）'
    )
    
    args = parser.parse_args()
    
    # 检查输入文件是否存在
    if not Path(args.input_file).exists():
        print(f"\n❌ 错误: 输入文件 '{args.input_file}' 不存在\n")
        sys.exit(1)
    
    # 生成项目简报
    try:
        generator = ProjectBriefGenerator(args.input_file)
        
        # 调试模式
        if args.debug:
            generator.print_data_structure()
        
        # 验证模式
        if args.validate:
            generator.validate_structure()
        
        # 生成文档
        generator.save_to_file(args.output)
        
    except Exception as e:
        print(f"\n❌ 生成失败: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()