#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRD JSON to Markdown Converter
将符合PRD JSON Schema的JSON文件转换为Markdown格式的PRD文档

Author: AI Assistant
Version: 1.0.0
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class PRDMarkdownGenerator:
    """PRD Markdown文档生成器"""

    def __init__(self, json_data: Dict[str, Any]):
        self.data = json_data
        self.lines: List[str] = []

    def generate(self) -> str:
        """生成完整的Markdown文档"""
        self.lines = []

        self._generate_header()
        self._generate_document_info()
        self._generate_step1()
        self._generate_step2()
        self._generate_step3()
        self._generate_step4()
        self._generate_step5()
        self._generate_step6()
        self._generate_appendix()

        return "\n".join(self.lines)

    def _add_line(self, line: str = ""):
        """添加一行"""
        self.lines.append(line)

    def _add_lines(self, lines: List[str]):
        """添加多行"""
        self.lines.extend(lines)

    def _generate_header(self):
        """生成文档头部"""
        self._add_line("# 产品需求文档 (PRD)")
        self._add_line()

    def _generate_document_info(self):
        """生成文档信息表格"""
        info = self.data.get("documentInfo", {})

        self._add_line("## 文档信息")
        self._add_line()
        self._add_line("| 项目 | 内容 |")
        self._add_line("|------|------|")
        self._add_line(f"| 产品名称 | {info.get('productName', '[未填写]')} |")
        self._add_line(f"| 版本 | {info.get('version', '[未填写]')} |")
        self._add_line(f"| 作者 | {info.get('author', '[未填写]')} |")
        self._add_line(f"| 日期 | {info.get('date', '[未填写]')} |")
        self._add_line(f"| 状态 | {info.get('status', '[未填写]')} |")
        self._add_line()

    def _generate_step1(self):
        """生成Step 1: 理解项目背景"""
        step1 = self.data.get("step1", {})

        self._add_line("---")
        self._add_line()
        self._add_line("## 1. 产品概述")
        self._add_line()

        # 1.1 项目简报
        brief = step1.get("readProjectBrief", {})
        self._add_line("### 1.1 项目简报")
        self._add_line()
        self._add_line("**项目摘要**")
        self._add_line()
        self._add_line(brief.get("summary", "[未填写]"))
        self._add_line()
        self._add_line("**项目范围**")
        self._add_line()
        self._add_line(brief.get("scope", "[未填写]"))
        self._add_line()
        self._add_line("**项目背景**")
        self._add_line()
        self._add_line(brief.get("background", "[未填写]"))
        self._add_line()

        # 1.2 需求确认
        requirements = step1.get("confirmRequirementsWithAnalyst", {})
        self._add_line("### 1.2 需求确认")
        self._add_line()
        self._add_line(f"- **需求分析师**: {requirements.get('analystName', '[未填写]')}")
        self._add_line(f"- **确认日期**: {requirements.get('confirmDate', '[未填写]')}")
        self._add_line()

        self._add_line("**关键需求**")
        self._add_line()
        for req in requirements.get("keyRequirements", []):
            self._add_line(f"- {req}")
        self._add_line()

        clarifications = requirements.get("clarifications", [])
        if clarifications:
            self._add_line("**澄清事项**")
            self._add_line()
            self._add_line("| 问题 | 答案 |")
            self._add_line("|------|------|")
            for item in clarifications:
                self._add_line(f"| {item.get('question', '')} | {item.get('answer', '')} |")
            self._add_line()

        # 1.3 业务目标
        objectives = step1.get("understandBusinessObjectives", {})
        self._add_line("### 1.3 业务目标")
        self._add_line()
        self._add_line("**主要业务目标**")
        self._add_line()
        self._add_line(objectives.get("primaryObjective", "[未填写]"))
        self._add_line()

        secondary = objectives.get("secondaryObjectives", [])
        if secondary:
            self._add_line("**次要业务目标**")
            self._add_line()
            for obj in secondary:
                self._add_line(f"- {obj}")
            self._add_line()

        metrics = objectives.get("successMetrics", [])
        if metrics:
            self._add_line("**成功指标**")
            self._add_line()
            self._add_line("| 指标 | 目标值 |")
            self._add_line("|------|--------|")
            for m in metrics:
                self._add_line(f"| {m.get('metric', '')} | {m.get('target', '')} |")
            self._add_line()

        # 1.4 目标用户
        users = step1.get("identifyTargetUsers", {})
        self._add_line("### 1.4 目标用户")
        self._add_line()
        self._add_line("**主要用户群体**")
        self._add_line()
        for user in users.get("primaryUsers", []):
            self._add_line(f"- {user}")
        self._add_line()

        secondary_users = users.get("secondaryUsers", [])
        if secondary_users:
            self._add_line("**次要用户群体**")
            self._add_line()
            for user in secondary_users:
                self._add_line(f"- {user}")
            self._add_line()

    def _generate_step2(self):
        """生成Step 2: 定义产品愿景"""
        step2 = self.data.get("step2", {})

        self._add_line("---")
        self._add_line()
        self._add_line("## 2. 产品愿景")
        self._add_line()

        # 2.1 产品愿景陈述
        vision = step2.get("writeVisionStatement", {})
        self._add_line("### 2.1 产品愿景陈述")
        self._add_line()
        self._add_line(f"> {vision.get('statement', '[未填写]')}")
        self._add_line()
        if vision.get("timeframe"):
            self._add_line(f"**时间框架**: {vision.get('timeframe')}")
            self._add_line()
        if vision.get("impact"):
            self._add_line(f"**预期影响**: {vision.get('impact')}")
            self._add_line()

        # 2.2 产品定位
        positioning = step2.get("defineProductPositioning", {})
        self._add_line("### 2.2 产品定位")
        self._add_line()
        self._add_line(positioning.get("positioning", "[未填写]"))
        self._add_line()

        if positioning.get("category"):
            self._add_line(f"- **产品类别**: {positioning.get('category')}")
        if positioning.get("targetMarket"):
            self._add_line(f"- **目标市场**: {positioning.get('targetMarket')}")
        self._add_line()

        differentiators = positioning.get("differentiators", [])
        if differentiators:
            self._add_line("**差异化因素**")
            self._add_line()
            for diff in differentiators:
                self._add_line(f"- {diff}")
            self._add_line()

        competitors = positioning.get("competitors", [])
        if competitors:
            self._add_line("**竞争对手分析**")
            self._add_line()
            self._add_line("| 竞争对手 | 优势 | 劣势 |")
            self._add_line("|----------|------|------|")
            for comp in competitors:
                self._add_line(
                    f"| {comp.get('name', '')} | {comp.get('strengths', '')} | {comp.get('weaknesses', '')} |"
                )
            self._add_line()

        # 2.3 核心价值主张
        value = step2.get("determineCoreValueProposition", {})
        self._add_line("### 2.3 核心价值主张")
        self._add_line()
        self._add_line(value.get("coreValue", "[未填写]"))
        self._add_line()

        benefits = value.get("benefits", [])
        if benefits:
            self._add_line("**用户收益**")
            self._add_line()
            for benefit in benefits:
                self._add_line(f"- {benefit}")
            self._add_line()

        if value.get("uniqueness"):
            self._add_line(f"**独特性**: {value.get('uniqueness')}")
            self._add_line()

        # 2.4 目标用户画像
        personas = step2.get("describeUserPersonas", [])
        self._add_line("### 2.4 目标用户画像")
        self._add_line()

        for i, persona in enumerate(personas, 1):
            persona_name = persona.get("personaName", f"用户画像 {i}")
            self._add_line(f"#### {persona_name}")
            self._add_line()
            self._add_line("| 属性 | 描述 |")
            self._add_line("|------|------|")
            self._add_line(f"| 用户类型 | {persona.get('userType', '')} |")
            self._add_line(f"| 年龄范围 | {persona.get('ageRange', '')} |")
            self._add_line(f"| 技术水平 | {persona.get('techLevel', '')} |")
            self._add_line(f"| 主要需求 | {', '.join(persona.get('mainNeeds', []))} |")
            self._add_line(f"| 痛点 | {', '.join(persona.get('painPoints', []))} |")

            if persona.get("goals"):
                self._add_line(f"| 目标 | {', '.join(persona.get('goals', []))} |")
            if persona.get("behaviors"):
                self._add_line(f"| 行为特征 | {persona.get('behaviors')} |")

            self._add_line()

    def _generate_step3(self):
        """生成Step 3: 功能规划"""
        step3 = self.data.get("step3", {})

        self._add_line("---")
        self._add_line()
        self._add_line("## 3. 功能需求")
        self._add_line()

        # 3.1 功能列表
        features = step3.get("listAllFeatureRequirements", [])
        self._add_line("### 3.1 功能列表")
        self._add_line()
        self._add_line("| ID | 功能名称 | 描述 | 分类 | 状态 |")
        self._add_line("|----|----------|------|------|------|")
        for feature in features:
            self._add_line(
                f"| {feature.get('id', '')} | {feature.get('name', '')} | "
                f"{feature.get('description', '')} | {feature.get('category', '')} | "
                f"{feature.get('status', '待开发')} |"
            )
        self._add_line()

        # 3.2 优先级排序 (MoSCoW)
        priority = step3.get("prioritizeFeaturesMoSCoW", {})
        self._add_line("### 3.2 功能优先级 (MoSCoW)")
        self._add_line()

        self._add_line("#### Must Have (必须实现)")
        self._add_line()
        must = priority.get("must", [])
        if must:
            self._add_line("| 功能ID | 功能名称 | 理由 |")
            self._add_line("|--------|----------|------|")
            for item in must:
                self._add_line(
                    f"| {item.get('featureId', '')} | {item.get('featureName', '')} | "
                    f"{item.get('reason', '')} |"
                )
        else:
            self._add_line("*无*")
        self._add_line()

        self._add_line("#### Should Have (应该实现)")
        self._add_line()
        should = priority.get("should", [])
        if should:
            self._add_line("| 功能ID | 功能名称 | 理由 |")
            self._add_line("|--------|----------|------|")
            for item in should:
                self._add_line(
                    f"| {item.get('featureId', '')} | {item.get('featureName', '')} | "
                    f"{item.get('reason', '')} |"
                )
        else:
            self._add_line("*无*")
        self._add_line()

        self._add_line("#### Could Have (可以实现)")
        self._add_line()
        could = priority.get("could", [])
        if could:
            self._add_line("| 功能ID | 功能名称 | 理由 |")
            self._add_line("|--------|----------|------|")
            for item in could:
                self._add_line(
                    f"| {item.get('featureId', '')} | {item.get('featureName', '')} | "
                    f"{item.get('reason', '')} |"
                )
        else:
            self._add_line("*无*")
        self._add_line()

        self._add_line("#### Won't Have (本版本不实现)")
        self._add_line()
        wont = priority.get("wont", [])
        if wont:
            self._add_line("| 功能ID | 功能名称 | 理由 |")
            self._add_line("|--------|----------|------|")
            for item in wont:
                self._add_line(
                    f"| {item.get('featureId', '')} | {item.get('featureName', '')} | "
                    f"{item.get('reason', '')} |"
                )
        else:
            self._add_line("*无*")
        self._add_line()

        # 3.3 功能依赖关系
        dependencies = step3.get("defineFeatureDependencies", [])
        self._add_line("### 3.3 功能依赖关系")
        self._add_line()
        if dependencies:
            self._add_line("| 功能ID | 功能名称 | 依赖功能 | 依赖类型 | 说明 |")
            self._add_line("|--------|----------|----------|----------|------|")
            for dep in dependencies:
                depends_on = ", ".join(dep.get("dependsOn", []))
                self._add_line(
                    f"| {dep.get('featureId', '')} | {dep.get('featureName', '')} | "
                    f"{depends_on} | {dep.get('dependencyType', '')} | {dep.get('notes', '')} |"
                )
        else:
            self._add_line("*无功能依赖关系*")
        self._add_line()

        # 3.4 MVP范围
        mvp = step3.get("planMVPScope", {})
        self._add_line("### 3.4 MVP范围")
        self._add_line()
        self._add_line(f"**MVP目标**: {mvp.get('mvpGoal', '[未填写]')}")
        self._add_line()

        included = mvp.get("includedFeatures", [])
        self._add_line(f"**包含功能**: {', '.join(included) if included else '无'}")
        self._add_line()

        excluded = mvp.get("excludedFeatures", [])
        self._add_line(f"**排除功能**: {', '.join(excluded) if excluded else '无'}")
        self._add_line()

        if mvp.get("timeline"):
            self._add_line(f"**预期时间线**: {mvp.get('timeline')}")
            self._add_line()

        if mvp.get("rationale"):
            self._add_line(f"**决策理由**: {mvp.get('rationale')}")
            self._add_line()

    def _generate_step4(self):
        """生成Step 4: 详细功能规格"""
        step4 = self.data.get("step4", [])

        self._add_line("---")
        self._add_line()
        self._add_line("## 4. 功能详细规格")
        self._add_line()

        for feature in step4:
            feature_id = feature.get("featureId", "")
            feature_name = feature.get("featureName", "")

            self._add_line(f"### {feature_id}: {feature_name}")
            self._add_line()

            # 4.x.1 功能描述
            desc = feature.get("detailedDescription", {})
            self._add_line("#### 功能描述")
            self._add_line()
            self._add_line(desc.get("description", "[未填写]"))
            self._add_line()

            # 业务规则
            rules = desc.get("businessRules", [])
            if rules:
                self._add_line("**业务规则**")
                self._add_line()
                for rule in rules:
                    rule_str = f"- **{rule.get('ruleId', '')}**: {rule.get('rule', '')}"
                    if rule.get("condition"):
                        rule_str += f" (条件: {rule.get('condition')})"
                    self._add_line(rule_str)
                self._add_line()

            # 数据需求
            data_req = desc.get("dataRequirements", {})
            if data_req:
                fields = data_req.get("fields", [])
                if fields:
                    self._add_line("**数据字段**")
                    self._add_line()
                    self._add_line("| 字段名 | 类型 | 描述 | 必填 | 验证规则 |")
                    self._add_line("|--------|------|------|------|----------|")
                    for field in fields:
                        required = "是" if field.get("required") else "否"
                        self._add_line(
                            f"| {field.get('fieldName', '')} | {field.get('fieldType', '')} | "
                            f"{field.get('description', '')} | {required} | "
                            f"{field.get('validation', '')} |"
                        )
                    self._add_line()

            # 4.x.2 用户流程
            flow = feature.get("userFlow", {})
            self._add_line("#### 用户流程")
            self._add_line()
            self._add_line(f"**入口**: {flow.get('entryPoint', '[未填写]')}")
            self._add_line()
            self._add_line(f"**出口**: {flow.get('exitPoint', '[未填写]')}")
            self._add_line()

            steps = flow.get("steps", [])
            if steps:
                self._add_line("**流程步骤**")
                self._add_line()
                self._add_line("| 步骤 | 用户操作 | 系统响应 | 备选路径 |")
                self._add_line("|------|----------|----------|----------|")
                for step in steps:
                    self._add_line(
                        f"| {step.get('stepNumber', '')} | {step.get('userAction', '')} | "
                        f"{step.get('systemResponse', '')} | {step.get('alternativePath', '')} |"
                    )
                self._add_line()

            if flow.get("flowDiagram"):
                self._add_line(f"**流程图**: {flow.get('flowDiagram')}")
                self._add_line()

            # 4.x.3 界面原型
            prototype = feature.get("interfacePrototype", {})
            self._add_line("#### 界面原型")
            self._add_line()

            if prototype.get("description"):
                self._add_line(prototype.get("description"))
                self._add_line()

            if prototype.get("prototypeLink"):
                self._add_line(f"**原型链接**: [{prototype.get('prototypeLink')}]({prototype.get('prototypeLink')})")
                self._add_line()

            components = prototype.get("uiComponents", [])
            if components:
                self._add_line("**UI组件**")
                self._add_line()
                self._add_line("| 组件名称 | 组件类型 | 描述 |")
                self._add_line("|----------|----------|------|")
                for comp in components:
                    self._add_line(
                        f"| {comp.get('componentName', '')} | {comp.get('componentType', '')} | "
                        f"{comp.get('description', '')} |"
                    )
                self._add_line()

            interactions = prototype.get("interactions", [])
            if interactions:
                self._add_line("**交互设计**")
                self._add_line()
                self._add_line("| 触发条件 | 交互动作 | 结果 |")
                self._add_line("|----------|----------|------|")
                for inter in interactions:
                    self._add_line(
                        f"| {inter.get('trigger', '')} | {inter.get('action', '')} | "
                        f"{inter.get('result', '')} |"
                    )
                self._add_line()

            collab = prototype.get("designCollaboration", {})
            if collab:
                self._add_line("**设计团队协作**")
                self._add_line()
                if collab.get("designer"):
                    self._add_line(f"- 设计师: {collab.get('designer')}")
                if collab.get("status"):
                    self._add_line(f"- 状态: {collab.get('status')}")
                if collab.get("designLink"):
                    self._add_line(f"- 设计文件: [{collab.get('designLink')}]({collab.get('designLink')})")
                self._add_line()

            # 4.x.4 验收标准
            criteria = feature.get("acceptanceCriteria", [])
            self._add_line("#### 验收标准")
            self._add_line()
            if criteria:
                for ac in criteria:
                    passed = "✅" if ac.get("passed") else "⬜"
                    self._add_line(f"**{ac.get('criteriaId', '')}** {passed}")
                    self._add_line()
                    self._add_line(f"- **Given**: {ac.get('given', '')}")
                    self._add_line(f"- **When**: {ac.get('when', '')}")
                    self._add_line(f"- **Then**: {ac.get('then', '')}")
                    self._add_line()
            else:
                self._add_line("*无验收标准*")
                self._add_line()

    def _generate_step5(self):
        """生成Step 5: 非功能需求"""
        step5 = self.data.get("step5", {})

        self._add_line("---")
        self._add_line()
        self._add_line("## 5. 非功能需求")
        self._add_line()

        # 5.1 性能需求
        perf = step5.get("performanceRequirements", {})
        self._add_line("### 5.1 性能需求")
        self._add_line()

        self._add_line("| 指标 | 要求 | 优先级 |")
        self._add_line("|------|------|--------|")

        if perf.get("pageLoadTime"):
            self._add_line(f"| 页面加载时间 | {perf.get('pageLoadTime')} | 高 |")
        if perf.get("apiResponseTime"):
            self._add_line(f"| API响应时间 | {perf.get('apiResponseTime')} | 高 |")
        if perf.get("concurrentUsers"):
            self._add_line(f"| 并发用户数 | {perf.get('concurrentUsers')} | 中 |")
        if perf.get("throughput"):
            self._add_line(f"| 吞吐量 | {perf.get('throughput')} | 中 |")

        for metric in perf.get("metrics", []):
            self._add_line(
                f"| {metric.get('metric', '')} | {metric.get('requirement', '')} | "
                f"{metric.get('priority', '中')} |"
            )
        self._add_line()

        # 5.2 安全需求
        sec = step5.get("securityRequirements", {})
        self._add_line("### 5.2 安全需求")
        self._add_line()

        requirements = sec.get("requirements", [])
        if requirements:
            self._add_line("| ID | 安全需求 | 描述 | 合规标准 |")
            self._add_line("|----|----------|------|----------|")
            for req in requirements:
                self._add_line(
                    f"| {req.get('id', '')} | {req.get('requirement', '')} | "
                    f"{req.get('description', '')} | {req.get('complianceStandard', '')} |"
                )
            self._add_line()

        if sec.get("authentication"):
            self._add_line(f"- **认证方式**: {sec.get('authentication')}")
        if sec.get("authorization"):
            self._add_line(f"- **授权机制**: {sec.get('authorization')}")
        if sec.get("dataEncryption"):
            self._add_line(f"- **数据加密**: {sec.get('dataEncryption')}")
        if sec.get("auditLogging"):
            self._add_line(f"- **审计日志**: {sec.get('auditLogging')}")
        self._add_line()

        # 5.3 可用性需求
        usability = step5.get("usabilityRequirements", {})
        self._add_line("### 5.3 可用性需求")
        self._add_line()

        self._add_line("| 指标 | 要求 |")
        self._add_line("|------|------|")
        if usability.get("systemAvailability"):
            self._add_line(f"| 系统可用性 | {usability.get('systemAvailability')} |")
        if usability.get("dataBackup"):
            self._add_line(f"| 数据备份 | {usability.get('dataBackup')} |")
        if usability.get("rto"):
            self._add_line(f"| 恢复时间目标(RTO) | {usability.get('rto')} |")
        if usability.get("rpo"):
            self._add_line(f"| 恢复点目标(RPO) | {usability.get('rpo')} |")

        for req in usability.get("otherRequirements", []):
            self._add_line(f"| {req.get('id', '')} | {req.get('requirement', '')} |")
        self._add_line()

        # 5.4 兼容性需求
        compat = step5.get("compatibilityRequirements", {})
        self._add_line("### 5.4 兼容性需求")
        self._add_line()

        browsers = compat.get("browsers", [])
        if browsers:
            self._add_line("**浏览器支持**")
            self._add_line()
            self._add_line("| 浏览器 | 最低版本 |")
            self._add_line("|--------|----------|")
            for browser in browsers:
                self._add_line(f"| {browser.get('browser', '')} | {browser.get('minVersion', '')} |")
            self._add_line()

        devices = compat.get("devices", [])
        if devices:
            self._add_line("**设备支持**")
            self._add_line()
            self._add_line("| 设备类型 | 规格要求 |")
            self._add_line("|----------|----------|")
            for device in devices:
                self._add_line(
                    f"| {device.get('deviceType', '')} | {device.get('specifications', '')} |"
                )
            self._add_line()

        os_list = compat.get("operatingSystems", [])
        if os_list:
            self._add_line("**操作系统支持**")
            self._add_line()
            self._add_line("| 操作系统 | 最低版本 |")
            self._add_line("|----------|----------|")
            for os_item in os_list:
                self._add_line(f"| {os_item.get('os', '')} | {os_item.get('minVersion', '')} |")
            self._add_line()

        resolutions = compat.get("screenResolutions", [])
        if resolutions:
            self._add_line(f"**屏幕分辨率支持**: {', '.join(resolutions)}")
            self._add_line()

    def _generate_step6(self):
        """生成Step 6: 审核与确认"""
        step6 = self.data.get("step6", {})

        self._add_line("---")
        self._add_line()
        self._add_line("## 6. 审核与确认")
        self._add_line()

        # 6.1 技术可行性评审
        tech = step6.get("confirmTechnicalFeasibilityWithArchitect", {})
        self._add_line("### 6.1 技术可行性评审")
        self._add_line()
        self._add_line(f"- **架构师**: {tech.get('architectName', '[未填写]')}")
        self._add_line(f"- **评审日期**: {tech.get('reviewDate', '[未填写]')}")
        self._add_line(f"- **可行性状态**: {tech.get('feasibilityStatus', '[未填写]')}")
        self._add_line()

        constraints = tech.get("technicalConstraints", [])
        if constraints:
            self._add_line("**技术约束**")
            self._add_line()
            for constraint in constraints:
                self._add_line(f"- {constraint}")
            self._add_line()

        recommendations = tech.get("technicalRecommendations", [])
        if recommendations:
            self._add_line("**技术建议**")
            self._add_line()
            for rec in recommendations:
                self._add_line(f"- {rec}")
            self._add_line()

        risks = tech.get("risks", [])
        if risks:
            self._add_line("**技术风险**")
            self._add_line()
            self._add_line("| 风险 | 影响 | 缓解措施 |")
            self._add_line("|------|------|----------|")
            for risk in risks:
                self._add_line(
                    f"| {risk.get('risk', '')} | {risk.get('impact', '')} | "
                    f"{risk.get('mitigation', '')} |"
                )
            self._add_line()

        if tech.get("comments"):
            self._add_line(f"**评审意见**: {tech.get('comments')}")
            self._add_line()

        # 6.2 利益相关者确认
        stakeholder = step6.get("confirmRequirementsWithStakeholders", {})
        self._add_line("### 6.2 利益相关者确认")
        self._add_line()
        self._add_line(f"**确认状态**: {stakeholder.get('confirmationStatus', '[未填写]')}")
        self._add_line()

        stakeholders = stakeholder.get("stakeholders", [])
        if stakeholders:
            self._add_line("**确认清单**")
            self._add_line()
            self._add_line("| 姓名 | 角色 | 已确认 | 确认日期 | 意见 |")
            self._add_line("|------|------|--------|----------|------|")
            for s in stakeholders:
                confirmed = "✅" if s.get("confirmed") else "⬜"
                self._add_line(
                    f"| {s.get('name', '')} | {s.get('role', '')} | {confirmed} | "
                    f"{s.get('confirmDate', '')} | {s.get('comments', '')} |"
                )
            self._add_line()

        pending = stakeholder.get("pendingIssues", [])
        if pending:
            self._add_line("**待解决问题**")
            self._add_line()
            self._add_line("| 问题 | 提出人 | 状态 | 解决方案 |")
            self._add_line("|------|--------|------|----------|")
            for issue in pending:
                self._add_line(
                    f"| {issue.get('issue', '')} | {issue.get('raisedBy', '')} | "
                    f"{issue.get('status', '')} | {issue.get('resolution', '')} |"
                )
            self._add_line()

        # 6.3 最终批准
        approval = step6.get("obtainFinalApproval", {})
        self._add_line("### 6.3 最终批准")
        self._add_line()
        self._add_line(f"- **批准状态**: {approval.get('approvalStatus', '[未填写]')}")

        if approval.get("approver"):
            self._add_line(f"- **批准人**: {approval.get('approver')}")
        if approval.get("approvalDate"):
            self._add_line(f"- **批准日期**: {approval.get('approvalDate')}")
        if approval.get("comments"):
            self._add_line(f"- **批准意见**: {approval.get('comments')}")
        self._add_line()

        conditions = approval.get("conditions", [])
        if conditions:
            self._add_line("**附加条件**")
            self._add_line()
            for cond in conditions:
                self._add_line(f"- {cond}")
            self._add_line()

        signoffs = approval.get("signoffs", [])
        if signoffs:
            self._add_line("**签字确认**")
            self._add_line()
            self._add_line("| 角色 | 姓名 | 已签字 | 签字日期 |")
            self._add_line("|------|------|--------|----------|")
            for sign in signoffs:
                signed = "✅" if sign.get("signed") else "⬜"
                self._add_line(
                    f"| {sign.get('role', '')} | {sign.get('name', '')} | "
                    f"{signed} | {sign.get('signDate', '')} |"
                )
            self._add_line()

    def _generate_appendix(self):
        """生成附录"""
        appendix = self.data.get("appendix", {})

        if not appendix:
            return

        self._add_line("---")
        self._add_line()
        self._add_line("## 附录")
        self._add_line()

        # 术语表
        glossary = appendix.get("glossary", [])
        if glossary:
            self._add_line("### 术语表")
            self._add_line()
            self._add_line("| 术语 | 定义 |")
            self._add_line("|------|------|")
            for term in glossary:
                self._add_line(f"| {term.get('term', '')} | {term.get('definition', '')} |")
            self._add_line()

        # 参考资料
        references = appendix.get("references", [])
        if references:
            self._add_line("### 参考资料")
            self._add_line()
            for i, ref in enumerate(references, 1):
                self._add_line(f"{i}. {ref}")
            self._add_line()

        # 修订历史
        history = appendix.get("revisionHistory", [])
        if history:
            self._add_line("### 修订历史")
            self._add_line()
            self._add_line("| 版本 | 日期 | 作者 | 修改内容 |")
            self._add_line("|------|------|------|----------|")
            for rev in history:
                self._add_line(
                    f"| {rev.get('version', '')} | {rev.get('date', '')} | "
                    f"{rev.get('author', '')} | {rev.get('changes', '')} |"
                )
            self._add_line()


def load_json_file(file_path: str) -> Dict[str, Any]:
    """加载JSON文件"""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_markdown_file(content: str, file_path: str):
    """保存Markdown文件"""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="将PRD JSON文件转换为Markdown格式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python prd_json_to_markdown.py input.json
  python prd_json_to_markdown.py input.json -o output.md
  python prd_json_to_markdown.py input.json --output custom_prd.md
        """
    )

    parser.add_argument(
        "input",
        type=str,
        help="输入的JSON文件路径"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="输出的Markdown文件路径（默认为输入文件名.md）"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="显示详细输出"
    )

    args = parser.parse_args()

    # 确定输出文件路径
    input_path = Path(args.input)
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_suffix(".md")

    try:
        # 加载JSON数据
        if args.verbose:
            print(f"正在读取JSON文件: {input_path}")

        json_data = load_json_file(str(input_path))

        # 生成Markdown
        if args.verbose:
            print("正在生成Markdown文档...")

        generator = PRDMarkdownGenerator(json_data)
        markdown_content = generator.generate()

        # 保存Markdown文件
        save_markdown_file(markdown_content, str(output_path))

        print(f"✅ 成功生成PRD文档: {output_path}")

    except FileNotFoundError:
        print(f"❌ 错误: 找不到文件 '{input_path}'")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ 错误: JSON解析失败 - {e}")
        exit(1)
    except Exception as e:
        print(f"❌ 错误: {e}")
        exit(1)


if __name__ == "__main__":
    main()