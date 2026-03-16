#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户故事 JSON 转 Markdown 工具
"""

import json
from pathlib import Path

# ============================================
# 🔧 配置区域 - 只需修改这里
# ============================================

# JSON 文件路径
JSON_FILE = "user_stories.json"

# 输出目录
OUTPUT_DIR = "output"

# 拆分模式选择（修改数字即可切换模式）
# 1 = 按工作流程拆分
# 2 = 按用户类型拆分
# 3 = 按界面元素拆分
# 4 = 按复杂度拆分
# 5 = 全部故事（不分类）
SPLIT_MODE = 5

# ============================================
# 以下代码无需修改
# ============================================

# 模式配置
MODE_CONFIG = {
    1: {
        "name": "按工作流程拆分",
        "key": "by_workflow",
        "category_key": "workflow_name",
        "filename": "user_stories_by_workflow.md"
    },
    2: {
        "name": "按用户类型拆分",
        "key": "by_user_type",
        "category_key": "user_type",
        "filename": "user_stories_by_user_type.md"
    },
    3: {
        "name": "按界面元素拆分",
        "key": "by_ui_element",
        "category_key": "ui_element",
        "filename": "user_stories_by_ui_element.md"
    },
    4: {
        "name": "按复杂度拆分",
        "key": "by_complexity",
        "category_key": "complexity_level",
        "filename": "user_stories_by_complexity.md"
    },
    5: {
        "name": "全部故事",
        "key": "all",
        "category_key": None,
        "filename": "user_stories_all.md"
    }
}


class UserStoryGenerator:
    """用户故事文档生成器"""
    
    def __init__(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    
    def generate_story(self, story_data, story_number):
        """生成单个用户故事"""
        info = story_data.get('story_info', {})
        user_story = story_data.get('user_story', {})
        ac = story_data.get('acceptance_criteria', {})
        tech = story_data.get('technical_notes', {})
        deps = story_data.get('dependencies', {})
        test = story_data.get('test_scenarios', {})
        ui_ux = story_data.get('ui_ux_reference', {})
        tasks = story_data.get('task_breakdown', [])
        
        title = info.get('title', '[故事标题]')
        
        md = f"""# 用户故事: 故事{story_number}: {title}

## 故事信息

| 项目 | 内容 |
|------|------|
| 故事ID | {info.get('story_id', '[Epic号].[故事号]')} |
| Epic | {info.get('epic_name', '[所属Epic名称]')} |
| 优先级 | {info.get('priority', '[高/中/低]')} |
| 故事点 | {info.get('story_points', '[估算点数]')} |
| 状态 | {info.get('status', '[新建/细化/就绪/进行中/完成]')} |

## 用户故事

**作为** {user_story.get('as_a', '[角色]')}

**我想要** {user_story.get('i_want', '[功能/行为]')}

**以便于** {user_story.get('so_that', '[价值/目的]')}

## 业务背景

{story_data.get('business_context', '[描述这个功能的业务背景和价值]')}

## 验收标准

### 功能验收
"""
        
        # 功能验收
        functional = ac.get('functional', [])
        if functional:
            for item in functional:
                checked = "x" if item.get('verified', False) else " "
                md += f"- [{checked}] {item.get('ac_id', 'AC')}: {item.get('description', '[验收标准描述]')}\n"
        else:
            md += "- [ ] AC1: [验收标准描述]\n- [ ] AC2: [验收标准描述]\n- [ ] AC3: [验收标准描述]\n"
        
        # 非功能验收
        nf = ac.get('non_functional', {})
        md += f"""
### 非功能验收
- [ ] 性能: {nf.get('performance', '[性能要求]')}
- [ ] 安全: {nf.get('security', '[安全要求]')}
- [ ] 可访问性: {nf.get('accessibility', '[可访问性要求]')}

## 技术说明

### 前端实现
"""
        
        # 前端
        frontend = tech.get('frontend_implementation', [])
        if frontend:
            for item in frontend:
                md += f"- {item}\n"
        else:
            md += "- [技术要点1]\n- [技术要点2]\n"
        
        md += "\n### 后端实现\n"
        backend = tech.get('backend_implementation', [])
        if backend:
            for item in backend:
                md += f"- {item}\n"
        else:
            md += "- [技术要点1]\n- [技术要点2]\n"
        
        md += "\n### 数据库变更\n"
        db = tech.get('database_changes', [])
        if db:
            for item in db:
                md += f"- {item}\n"
        else:
            md += "- [变更描述]\n"
        
        # API
        md += "\n### API接口\n| 接口 | 方法 | 描述 |\n|------|------|------|\n"
        apis = tech.get('api_interfaces', [])
        if apis:
            for api in apis:
                md += f"| {api.get('endpoint', '[路径]')} | {api.get('method', '[方法]')} | {api.get('description', '[描述]')} |\n"
        else:
            md += "| [路径] | [方法] | [描述] |\n"
        
        # 依赖
        md += "\n## 依赖关系\n\n### 前置依赖\n"
        preds = deps.get('predecessors', [])
        if preds:
            for dep in preds:
                md += f"- [ ] Story-{dep.get('story_id', '[ID]')}: {dep.get('description', '[依赖描述]')}\n"
        else:
            md += "- [ ] Story-[ID]: [依赖描述]\n"
        
        md += "\n### 后置依赖\n"
        succs = deps.get('successors', [])
        if succs:
            for dep in succs:
                md += f"- [ ] Story-{dep.get('story_id', '[ID]')}: {dep.get('description', '[依赖描述]')}\n"
        else:
            md += "- [ ] Story-[ID]: [依赖描述]\n"
        
        # 测试场景
        md += "\n## 测试场景\n\n### 正向场景\n"
        positive = test.get('positive_scenarios', [])
        if positive:
            for idx, s in enumerate(positive, 1):
                md += f"{idx}. {s}\n"
        else:
            md += "1. [场景描述]\n2. [场景描述]\n"
        
        md += "\n### 异常场景\n"
        negative = test.get('negative_scenarios', [])
        if negative:
            for idx, s in enumerate(negative, 1):
                md += f"{idx}. {s}\n"
        else:
            md += "1. [场景描述]\n2. [场景描述]\n"
        
        md += "\n### 边界场景\n"
        edge = test.get('edge_cases', [])
        if edge:
            for idx, s in enumerate(edge, 1):
                md += f"{idx}. {s}\n"
        else:
            md += "1. [场景描述]\n2. [场景描述]\n"
        
        # UI/UX
        md += "\n## UI/UX参考\n\n"
        if ui_ux.get('prototype_url') or ui_ux.get('design_url'):
            if ui_ux.get('prototype_url'):
                md += f"[原型图链接]({ui_ux['prototype_url']})\n\n"
            if ui_ux.get('design_url'):
                md += f"[设计稿链接]({ui_ux['design_url']})\n\n"
        else:
            md += "[原型图或设计稿链接]\n"
        
        # 任务分解
        md += "\n## 任务分解\n\n| 任务 | 负责人 | 估算 | 状态 |\n|------|--------|------|------|\n"
        if tasks:
            for task in tasks:
                md += f"| {task.get('task_description', '[任务描述]')} | {task.get('assignee', '[负责人]')} | {task.get('estimation', '[估算]')} | {task.get('status', '[状态]')} |\n"
        else:
            md += "| [任务描述] | [负责人] | [估算] | [状态] |\n"
        
        # 备注
        md += f"\n## 备注\n\n{story_data.get('notes', '[其他需要说明的内容]')}\n"
        
        # 变更历史
        md += "\n## 变更历史\n\n| 日期 | 作者 | 变更内容 |\n|------|------|----------|\n"
        revisions = self.data.get('document_info', {}).get('revision_history', [])
        if revisions:
            for rev in revisions:
                md += f"| {rev.get('date', '[日期]')} | {rev.get('author', '[作者]')} | {rev.get('changes', '[变更内容]')} |\n"
        else:
            md += "| [日期] | [作者] | [变更内容] |\n"
        
        return md
    
    def generate_document(self, split_mode):
        """根据拆分模式生成文档"""
        config = MODE_CONFIG.get(split_mode, MODE_CONFIG[5])
        doc_info = self.data.get('document_info', {})
        stories = self.data.get('step3_write_story_details', {}).get('stories', [])
        techniques = self.data.get('step2_story_splitting', {}).get('splitting_techniques', {})
        
        # 文档头
        md = f"""# 用户故事文档

## 文档信息

| 项目 | 内容 |
|------|------|
| 项目名称 | {doc_info.get('project_name', '[项目名称]')} |
| 版本 | {doc_info.get('version', '[版本]')} |
| 作者 | {doc_info.get('author', '[作者]')} |
| 创建日期 | {doc_info.get('created_date', '[日期]')} |
| 最后更新 | {doc_info.get('last_updated', '[日期]')} |
| 拆分模式 | {config['name']} |

---

"""
        
        story_number = 1
        
        if split_mode == 5:
            # 全部故事模式
            md += "## 故事列表\n\n| 序号 | 故事ID | 标题 | 优先级 | 故事点 | 状态 |\n|------|--------|------|--------|--------|------|\n"
            for idx, story in enumerate(stories, 1):
                info = story.get('story_info', {})
                md += f"| {idx} | {info.get('story_id', '')} | {info.get('title', '')} | {info.get('priority', '')} | {info.get('story_points', '')} | {info.get('status', '')} |\n"
            
            md += "\n---\n\n"
            
            for story in stories:
                md += self.generate_story(story, story_number)
                md += "\n---\n\n"
                story_number += 1
        
        else:
            # 分类模式
            split_data = techniques.get(config['key'], [])
            category_key = config['category_key']
            
            for category in split_data:
                category_name = category.get(category_key, '')
                if not category_name:
                    continue
                
                md += f"## {category_name}\n\n"
                
                category_stories = category.get('stories', [])
                for story_ref in category_stories:
                    story_id = story_ref if isinstance(story_ref, str) else story_ref.get('story_id', '')
                    
                    # 查找故事详情
                    story_data = None
                    for s in stories:
                        if s.get('story_info', {}).get('story_id') == story_id:
                            story_data = s
                            break
                    
                    if story_data:
                        md += self.generate_story(story_data, story_number)
                    else:
                        md += f"### 故事{story_number}: {story_ref}\n\n[待补充详细信息]\n"
                    
                    md += "\n---\n\n"
                    story_number += 1
        
        return md, config['filename']
    
    def save(self, split_mode, output_dir):
        """保存文档"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        content, filename = self.generate_document(split_mode)
        
        output_file = output_path / filename
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return output_file


def main():
    """主函数"""
    print("\n" + "=" * 50)
    print("  用户故事文档生成工具")
    print("=" * 50)
    
    # 显示当前配置
    config = MODE_CONFIG.get(SPLIT_MODE, MODE_CONFIG[5])
    print(f"\n📋 JSON文件: {JSON_FILE}")
    print(f"📁 输出目录: {OUTPUT_DIR}")
    print(f"🔧 拆分模式: [{SPLIT_MODE}] {config['name']}")
    print()
    
    try:
        generator = UserStoryGenerator(JSON_FILE)
        output_file = generator.save(SPLIT_MODE, OUTPUT_DIR)
        print(f"✅ 文档已生成: {output_file}")
        print("\n🎉 完成!")
    except FileNotFoundError:
        print(f"❌ 错误: 文件 {JSON_FILE} 不存在")
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析错误: {e}")
    except Exception as e:
        print(f"❌ 错误: {e}")


if __name__ == '__main__':
    main()