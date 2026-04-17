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