# 技能模板生成

## 1. 基础技能模板

### 模板结构
```markdown
---
name: [skill-name]
label: [human-readable-label]
description: "[完整的功能描述，包括使用场景和触发条件]"
---

# [技能标题]

## 概述

[1-2句话说明技能功能]

## 工作流程决策树

### 第1步：意图理解
- **触发词**：[用户可能使用的关键词]
- **识别逻辑**：[如何识别用户意图]
- **输出**：[确定的策略类型]

### 第2步：多轮确认
1. **问题1**：[第一个问题的具体内容]
   - [可能的用户回答模式]
   - [需要澄清的细节]

2. **问题2**：[第二个问题的具体内容]
   - [可能的用户回答模式]
   - [需要澄清的细节]

3. **问题3**：[第三个问题的具体内容]
   - [可能的用户回答模式]
   - [需要澄清的细节]

4. **问题4**：[第四个问题的具体内容]
   - [可能的用户回答模式]
   - [需要澄清的细节]

### 第3步：配置生成
- **JSON schema**：[引用的schema文件]
- **自动填充**：[哪些字段自动生成]
- **验证规则**：[配置验证标准]

### 第4步：Skill沉淀
- **模式记录**：[如何记录对话模式]
- **规则提取**：[如何提取可复用规则]
- **模板更新**：[如何更新技能模板]

## 核心功能

### 1. [功能1名称]
- [功能描述]
- [使用示例]
- [相关资源]

### 2. [功能2名称]
- [功能描述]
- [使用示例]
- [相关资源]

## 使用示例

### 示例1：[示例名称]
**用户查询**："[用户原始查询]"

**技能响应流程**：
1. [第一步响应]
2. [第二步响应]
3. [第三步响应]

**生成配置**：[配置说明]

## 资源引用

### 关键配置文件
- **schema文件**：[schema.md](references/schema.md) - [文件说明]
- **模式文件**：[patterns.md](references/patterns.md) - [文件说明]
- **规则文件**：[rules.md](references/rules.md) - [文件说明]
- **模板文件**：[template.md](references/template.md) - [文件说明]

### 执行脚本
- **[脚本名称]**：[script.py](scripts/script.py) - [脚本功能说明]

### 示例资源
- **[资源名称]**：[example.json](assets/example.json) - [资源说明]

## 最佳实践

### 对话引导
- [对话引导建议1]
- [对话引导建议2]
- [对话引导建议3]

### 配置生成
- [配置生成建议1]
- [配置生成建议2]
- [配置生成建议3]

### Skill沉淀
- [Skill沉淀建议1]
- [Skill沉淀建议2]
- [Skill沉淀建议3]
```

## 2. 访问策略配置助手模板

### 完整模板（基于当前对话）
```markdown
---
name: web-access-policy-builder
label: 访问策略配置助手
description: "通过结构化对话生成网页访问策略配置，支持限制特定网站访问和控制网站操作权限。当用户需要配置网页访问策略时使用此技能，特别是：1) 在工作时间限制社交媒体网站访问 2) 控制特定网站功能权限 3) 配置员工网络访问策略 4) 生成标准化的JSON策略配置。关键词：禁止访问、限制网站、访问策略、工作时间、社交媒体、审批流程。"
---

# 访问策略配置助手

## 概述

本技能帮助用户通过结构化对话生成网页访问策略配置。遵循4步工作流程：1) 理解意图 2) 多轮确认 3) 生成配置 4) 沉淀Skill。支持两种策略类型：specific_website（限制特定网站访问）和global_website（控制所有网站操作权限）。

## 工作流程决策树

### 第1步：策略类型识别
- **触发词**：用户提到"禁止访问" + 网站类型 → `specific_website`
  - 示例："上班时间禁止员工访问社交媒体网站"
- **触发词**：用户提到"所有网站" + "操作权限" → `global_website`
  - 示例："控制员工对所有网站的下载权限"

### 第2步：多轮确认流程（必须按顺序询问）
1. **生效对象是谁？**
   - 需要澄清：排除人群定义、员工类型包含性（实习生/外包/远程员工）
   - 模式："除XX外的所有员工" → 需要询问XX的具体定义

2. **什么时间生效？**
   - 标准工作时间：周一到周五 9:00-18:00，上海时区，排除午休
   - 需要确认：具体时间段、工作日/周末、是否包括午休

3. **具体限制内容是什么？**
   - `specific_website`：列出具体域名（如：weibo.com, douyin.com）
   - `global_website`：定义操作权限（如：禁止下载、打印、上传）
   - 需要确认：完全禁止还是功能限制、工作用途例外

4. **是否需要审批流程？**
   - 默认配置：需要审批时，CEO线上审批，最长4小时有效期，自动撤销
   - 需要确认：审批人、审批方式（线上/线下）、最长有效期

### 第3步：配置生成
- 使用预定义的JSON schema（见`references/schema.md`）
- 自动填充：策略ID、名称、状态、创建信息
- 包含完整模块：target_users, schedule, restrictions, approval_process, enforcement, monitoring

### 第4步：Skill沉淀
- 记录对话模式到`references/patterns.md`
- 提取可复用规则到`references/rules.md`
- 生成Skill模板到`references/template.md`

## 核心功能

### 1. 意图理解
- **自然语言处理**：识别"禁止"、"限制"、"允许"等关键动词
- **网站分类识别**：理解"社交媒体"、"视频网站"、"游戏网站"等类别概念
- **时间表达式解析**：解析"上班时间"、"下班后"、"周末"等时间表达

### 2. 结构化信息收集
采用4问题标准化流程，每个问题有针对性follow-up：
```markdown
**1. 生效对象是谁？**
- [Follow-up] 是否排除特定人群？
- [Follow-up] 是否包括实习生/外包/远程员工？

**2. 什么时间生效？**  
- [Follow-up] 具体时间段？
- [Follow-up] 工作日/周末？
- [Follow-up] 是否包括午休？

**3. 具体限制内容是什么？**
- [Follow-up] 具体网站列表？
- [Follow-up] 完全禁止还是功能限制？

**4. 是否需要审批流程？**
- [Follow-up] 谁审批？
- [Follow-up] 线上还是线下？
- [Follow-up] 最长有效期？
```

### 3. 配置生成标准化
- **JSON schema模板**：标准化的字段结构和默认值
- **自动填充**：创建时间、创建人、状态等系统字段
- **模块化设计**：target_users, schedule, restrictions, approval_process, enforcement, monitoring
- **可扩展性**：支持自定义字段和规则

### 4. 知识沉淀机制
- **实时模式识别**：记录成功对话模式
- **规则提取**：从对话中提取可复用规则
- **Skill模板生成**：创建标准化的Skill模板

## 使用示例

### 示例1：工作时间社交媒体限制
**用户查询**："我想在上班时间禁止员工访问社交媒体网站"

**技能响应流程**：
1. 识别策略类型：`specific_website`
2. 询问生效对象："除了老板外的所有员工"
3. 询问生效时间："周一到周五，早上9点到下午6点（标准工作时间）"  
4. 询问具体内容："微博、抖音网页版、小红书、Facebook、Twitter/X、Instagram"
5. 询问审批流程："需要申请特殊权限，由BOSS线上审批"

**生成配置**：完整的JSON策略配置（示例见`assets/example_config.json`）

## 资源引用

### 关键配置文件
- **策略schema**：[schema.md](references/schema.md) - 完整的JSON schema定义和字段说明
- **对话模式**：[patterns.md](references/patterns.md) - 已识别的对话模式和触发条件
- **提取规则**：[rules.md](references/rules.md) - 从对话中提取的可复用规则
- **技能模板**：[template.md](references/template.md) - 标准化的Skill模板

### 执行脚本
- **配置验证**：[validate_policy.py](scripts/validate_policy.py) - 验证生成的策略配置
- **JSON生成**：[generate_config.py](scripts/generate_config.py) - 根据对话生成JSON配置

### 示例资源
- **完整配置示例**：[example_config.json](assets/example_config.json) - 工作时间社交媒体限制的完整配置
- **标准时间设置**：[time_standards.json](assets/time_standards.json) - 常见工作时间标准定义

## 最佳实践

### 对话引导
- **逐步细化**：从宽泛问题开始，逐步细化到具体细节
- **明确澄清**：当用户回答模糊时，必须澄清具体定义
- **记录模式**：每次成功对话后记录模式到`references/patterns.md`

### 配置生成
- **验证完整性**：使用`scripts/validate_policy.py`验证配置
- **标准化命名**：遵循`policy_{type}_{purpose}_{number}`命名规范
- **自动填充**：系统字段（created_at, created_by, status）必须自动填充

### Skill沉淀
- **及时记录**：对话结束后立即沉淀模式
- **版本控制**：Skill模板保持向后兼容
- **示例完整**：提供完整的示例配置供参考
```

## 3. 模板定制指南

### 3.1 根据对话内容定制
**需要替换的占位符**：
- `[skill-name]`：技能名称，使用小写字母和连字符
- `[human-readable-label]`：用户可见的标签，使用用户语言
- `[完整的功能描述]`：必须包含触发条件和关键词
- `[技能标题]`：与label保持一致
- `[用户可能使用的关键词]`：从对话中提取的实际关键词
- `[使用示例]`：使用实际对话作为示例

### 3.2 基于新对话扩展模板
**扩展步骤**：
1. **识别新模式**：分析新对话与现有模式的区别
2. **更新patterns.md**：添加新模式到对话模式文件
3. **更新rules.md**：提取新规则到规则文件
4. **更新template.md**：将新模式整合到模板中
5. **更新SKILL.md**：同步更新技能主体内容

### 3.3 模板验证
**验证项目**：
1. **完整性检查**：所有占位符是否已替换
2. **一致性检查**：各文件间引用是否正确
3. **可执行性检查**：示例是否可实际运行
4. **可读性检查**：文档是否清晰易懂

## 4. 模板生成脚本

### 自动生成脚本示例
```python
# template_generator.py
def generate_skill_template(conversation_data):
    """根据对话数据生成技能模板"""
    
    # 提取对话信息
    user_query = conversation_data.get('user_query', '')
    responses = conversation_data.get('responses', [])
    policy_config = conversation_data.get('policy_config', {})
    
    # 生成技能名称
    skill_name = generate_skill_name(user_query)
    
    # 生成标签
    label = generate_label(user_query)
    
    # 生成描述
    description = generate_description(user_query, responses)
    
    # 生成工作流程
    workflow = generate_workflow(responses)
    
    # 生成示例
    examples = generate_examples(conversation_data)
    
    # 生成完整模板
    template = {
        'name': skill_name,
        'label': label,
        'description': description,
        'workflow': workflow,
        'examples': examples,
        'resources': ['schema.md', 'patterns.md', 'rules.md']
    }
    
    return template
```

### 模板生成规则
1. **名称生成规则**：使用小写字母、连字符，反映核心功能
2. **标签生成规则**：使用用户语言，简洁明了
3. **描述生成规则**：包含功能、触发条件、关键词
4. **工作流程规则**：基于实际对话流程
5. **示例生成规则**：使用真实对话作为示例

## 5. 模板维护

### 版本管理
```
templates/
├── v1.0/              # 初始版本
│   ├── base.md       # 基础模板
│   └── examples/     # 示例文件
├── v1.1/              # 增加新功能
│   ├── base.md       # 更新模板
│   └── changelog.md  # 变更记录
└── current/          # 当前版本（符号链接）
```

### 变更记录格式
```markdown
# 模板变更记录

## v1.1 (2026-04-10)
### 新增
- 支持global_website策略类型
- 添加审批流程默认配置
- 增加时间表达式解析规则

### 修改
- 优化工作流程决策树结构
- 完善示例对话格式
- 更新资源引用说明

### 修复
- 修正策略ID生成规则
- 修复时间范围验证逻辑
- 完善Follow-up问题模板
```

## 6. 模板应用建议

### 新技能创建流程
1. **收集对话数据**：至少3个成功对话示例
2. **分析模式**：识别共同模式和差异
3. **生成模板**：使用模板生成器创建基础模板
4. **定制化**：根据具体需求调整模板
5. **验证测试**：使用新对话验证模板有效性
6. **迭代优化**：根据测试结果优化模板

### 模板质量评估
**优秀模板特征**：
1. **完整性**：覆盖所有必要组件
2. **清晰性**：结构清晰，易于理解
3. **可扩展性**：支持新功能扩展
4. **实用性**：提供实际可用的示例
5. **一致性**：各组件间逻辑一致

**需要改进的信号**：
1. 用户频繁询问相同问题
2. 配置生成失败率高
3. 对话模式识别不准确
4. 资源引用错误
5. 示例不可用或过时