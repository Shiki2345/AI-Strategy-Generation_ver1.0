# AI 辅助策略生成模块

---

## 项目简介

本项目为紫鸟浏览器平台构建了一套 **AI 辅助访问策略生成系统**。用户用自然语言描述需求（如"禁止客服访问广告页面"），AI 通过多轮对话收集参数，输出可直接填入平台「新增访问策略」表单的 JSON 配置。

核心思路：将访问策略配置领域的专家经验编码为结构化的 Skill（提示词工程制品），让 LLM 每次面对同类问题时都能按专家水准执行，而不是靠自己即兴发挥。

### 系统工作流程

```
用户自然语言描述
  │
  ▼
Phase 1：意图识别 + 能力边界检查
  │  判断需求是否在平台能力范围内
  │  不支持 → 坦诚告知 + 推荐平台内替代方案
  │  条件支持 → 先问前提条件（如账号结构）
  │  支持 → 继续
  ▼
Phase 2：多轮对话收集参数
  │  RAG 检索 URL（219 条 Amazon 页面知识库）
  │  逐项收集：生效成员、账号、时段、URL 规则、审批限制
  ▼
Phase 3：确认汇总
  │  校验策略名称 ≤24 字符、描述 ≤400 字符、域名精准度
  ▼
Phase 4：生成表单输出
  │  输出 JSON，字段名与平台表单标签一一对应
  ▼
Phase 5：交付
```

### 关键数字

| 指标 | 数值 |
|------|------|
| RAG 知识库条目 | 219 条 Amazon URL（20 个分类，每条平均 8.6 个别名 + 11.9 个关键词） |
| 平台能力地图 | 24 个模块、17 条指路规则 |
| 预制角色策略模板 | 6 种角色（运营总监、产品专员、广告专员、客服、财务、仓储物流） |
| 策略生成样例 | 12 个（覆盖屏蔽、审批、数据隔离、批量角色等场景） |
| 测试案例 | 11 个（覆盖话题边界、正常流程、条件支持、不支持场景） |

---

## 项目结构

```
AI辅助策略生成模块/
│
├── 体验内容/access_policy_skill_package/   ← 核心 Skill 文件（提示词工程制品）
│   ├── skill_definition.json               ← 主 Skill 定义：平台能力边界 + 5 阶段对话流程 + 表单字段映射
│   ├── presets.json                         ← 预设值库：URL/时段/成员/浏览器控制/审批 5 类预设
│   ├── config_template.json                 ← 表单字段模板：字段类型、选项、约束
│   ├── example_output.json                  ← 输出示例：工作时间视频网站限制
│   ├── platform_module_map.json             ← 紫鸟平台能力地图：24 个模块 + 17 条指路规则
│   ├── README_ver2.0.md                     ← v2.0 改动说明
│   ├── README_platform_module_map.md        ← 能力地图产出过程文档
│   └── readme.md                            ← skill package 说明
│
├── amazon-rag-skill/                        ← RAG 数据 + 场景 Skill + 策略样例
│   ├── rag_simple_db.json                   ← RAG 知识库（219 条 URL，全量语义补全）
│   ├── data/amazon_urls.json                ← 种子数据（20 条手工整理的高质量 URL）
│   ├── rag_backup.json                      ← RAG 数据备份
│   │
│   ├── skills/
│   │   └── approval_based_access_control_skill.json  ← Amazon 场景 Skill：决策树 + 6 种角色策略模板
│   │
│   ├── generated_policies/                  ← 已生成的策略样例（12 个）
│   │   ├── 运营专员账户详情页审批策略.json
│   │   ├── 实习生定价管理审批策略.json
│   │   ├── 客服专员账户详情页完全禁止策略.json
│   │   ├── 买家号Checkout结账页屏蔽策略.json
│   │   ├── 6组Case数据隔离策略.json
│   │   ├── 财务专员多页面访问限制策略.json
│   │   ├── 财务专员多页面访问审批策略_v2.json
│   │   ├── 非财务人员VAT税务文件禁止访问策略.json
│   │   ├── 客服专员访问限制技术实现方案.md
│   │   ├── 三组访问策略结构化输出.md
│   │   └── 三组策略_表单填写版.md
│   │
│   ├── scripts/                             ← 工具脚本
│   │   ├── rag_system.py                    ← RAG 完整版（ChromaDB + OpenAI Embedding）
│   │   ├── rag_system_simple.py             ← RAG 简化版（JSON + 文本相似度）
│   │   ├── import_real_urls.py              ← 从平台 API 导入真实 URL 的脚本
│   │   ├── init_rag.py                      ← 完整版 RAG 初始化
│   │   ├── init_rag_simple.py               ← 简化版 RAG 初始化
│   │   ├── test_rag.py                      ← 完整版 RAG 测试
│   │   ├── test_rag_simple.py               ← 简化版 RAG 测试
│   │   ├── export_skill.py                  ← Skill 导出工具
│   │   ├── finalize_skill.py                ← Skill 炼制脚本
│   │   ├── validate_skill_reuse.py          ← Skill 复用验证
│   │   ├── generate_customer_service_policy.py  ← 客服策略生成脚本
│   │   └── search_pricing.py                ← 定价页面搜索脚本
│   │
│   ├── requirements.txt                     ← Python 依赖（chromadb、openai、python-dotenv）
│   ├── skill_finalization_report.json        ← Skill 炼制报告（JSON）
│   ├── skill_reuse_comparison_report.json    ← Skill 复用对比报告
│   ├── skill_reuse_deployment.json           ← Skill 复用部署信息
│   ├── SKILL_FINALIZATION_REPORT.md          ← Skill 炼制报告（可读版）
│   ├── FINANCE_MULTI_PAGE_SKILL_REPORT.md    ← 财务多页面策略报告
│   ├── QUICK_DEPLOYMENT_GUIDE.md             ← 快速部署指南
│   ├── 客服专员访问限制实施总结.md
│   ├── 财务专员多页面访问限制_skill_report.json
│   ├── README.md
│   ├── quick_rag_search.py
│   ├── update_rag_for_customer_service.py
│   └── finalize_finance_skill.py
│
├── 体验内容/                                ← 设计文档 + 过程记录
│   ├── 提示词.md                            ← 系统提示词 v2.1（可直接部署到 Aily）
│   ├── skill.md                             ← Skill 概念说明
│   ├── Skill 炼制操作指南.md                 ← Skill 炼制教程
│   ├── 整体流程梳理.md                       ← 业务流程全景
│   ├── 业务流程图-简化版.md                   ← 简化版流程图
│   ├── 完善工作流方案.md                      ← 工作流优化方案
│   ├── 输出数据总结.md                        ← 输出数据结构总结
│   ├── 平台URL知识库方案.md                   ← URL 知识库设计方案
│   ├── URL知识库对话演示.md                   ← RAG 对话效果演示
│   ├── 飞书Aily实战脚本.md                    ← 飞书 Aily 部署脚本
│   ├── 飞书Aily_Skill模板评估报告.md          ← Aily Skill 模板评估
│   ├── 文件关系说明.md                        ← 文件间依赖关系说明
│   ├── skill_system_implementation.py        ← Skill 系统实现参考
│   ├── knowledge_base_amazon_example.json    ← 知识库示例数据
│   ├── 工作时间视频网站限制.json              ← 场景示例：视频网站限制
│   └── access_policy_skill_package.zip       ← Skill 包打包文件
│
├── 根目录文件
│   ├── README.md                            ← 项目说明 + 改动日志 + 可行性评估
│   ├── 业务逻辑.md                          ← Agent 调用 Skill 的业务逻辑说明
│   ├── 用乐高积木与说明书讲解 Skill.md       ← Skill 概念类比解释
│   ├── 测试案例.md                           ← 11 个测试案例（话题边界 + 正常流程 + 能力边界）
│   ├── 黑话总结.md                           ← 跨境电商行业术语表
│   ├── Amazon_real_URL.txt                   ← 从紫鸟平台 API 获取的原始 URL 数据
│   ├── rag_simple_db.json                    ← RAG 数据库副本（根目录同步）
│   ├── rag_backup.json                       ← RAG 数据备份副本
│   ├── Skill 沉淀对话流程（Amazon 网站访问限制版）.md  ← 3 场景对话流程演示
│   └── Amazon 页面访问限制 RAG 实现方案.md    ← RAG 技术方案设计文档
```

---

## 核心文件说明

### 第一层：Skill 定义（喂给 LLM 的结构化提示词）

| 文件 | 作用 | 关键内容 |
|------|------|----------|
| skill_definition.json | 通用 Skill 基座 | 平台能力边界（supported / conditionally_supported / not_supported）、5 阶段对话流程、表单字段映射、输出规则 |
| approval_based_access_control_skill.json | Amazon 场景专精 Skill | 决策树（完全禁止 vs 需要审批）、RAG 集成点、6 种角色完整策略模板、URL 模块映射表 |
| presets.json | 预设值库 | 10 组 URL 预设、5 个时段预设、6 个成员预设、4 个浏览器控制预设、3 个审批预设 |
| platform_module_map.json | 紫鸟平台能力地图 | 24 个模块的导航路径和触发用语，当需求超出访问策略能力时指路到正确模块 |
| 提示词.md | 可直接部署的系统提示词 | 整合了上述所有 Skill 的精华，包含话题边界、能力检查、对话流程、表单规范、URL 语法规则 |

### 第二层：RAG 数据（URL 知识库）

| 文件 | 条目数 | 作用 |
|------|--------|------|
| rag_simple_db.json | 219 条 | 主数据库，每条包含 user_description、exact_url、page_description、aliases（平均 8.6 个）、keywords（平均 11.9 个），覆盖 20 个分类 |
| amazon_urls.json | 20 条 | 种子数据，手工整理的高质量条目（含 url_pattern 字段），用于早期测试 |

### 第三层：策略样例（验证 Skill 输出质量的产物）

12 个已生成的策略覆盖以下场景：

| 场景类型 | 样例文件 |
|----------|----------|
| 单页面审批制 | 运营专员账户详情页审批策略、实习生定价管理审批策略 |
| 单页面完全屏蔽 | 客服专员账户详情页完全禁止策略 |
| 多页面角色限制 | 财务专员多页面访问限制策略、财务专员多页面访问审批策略_v2 |
| 买家号屏蔽 | 买家号Checkout结账页屏蔽策略 |
| 数据隔离（反选模式） | 6组Case数据隔离策略 |
| 敏感数据保护 | 非财务人员VAT税务文件禁止访问策略 |
| 批量角色策略 | 三组策略_表单填写版、三组访问策略结构化输出 |

### 第四层：工具脚本

| 脚本 | 作用 |
|------|------|
| rag_system.py | 完整版 RAG（ChromaDB + OpenAI Embedding），支持语义检索 |
| rag_system_simple.py | 简化版 RAG（JSON + difflib 文本相似度），无外部依赖 |
| import_real_urls.py | 从紫鸟平台 API 数据导入 URL，自动分类 + 编码修复 |
| validate_skill_reuse.py | 对比首次配置与 Skill 复用的效率差异 |

### 第五层：文档

| 文档 | 受众 | 作用 |
|------|------|------|
| 业务逻辑.md | 开发者/产品经理 | 解释 Agent 如何调用 Skill 的完整链路 |
| 测试案例.md | 测试/部署人员 | 11 个测试案例，验证部署后模型行为是否符合预期 |
| 黑话总结.md | Skill 维护者 | 跨境电商行业术语，用于补充 RAG 别名和关键词 |
| 用乐高积木与说明书讲解 Skill.md | 非技术人员 | 用类比解释 Skill 概念 |

---

## 改动日志

### 版本演进路线总结

| 版本 | 核心主题 | 关键数字 |
|------|---------|---------|
| v1.0 | 基础 Skill 框架 + 自定义 JSON 输出 | 6 phase、自定义字段 |
| v2.0 | 输出 1:1 对齐平台表单 | 5 phase、5 类预设、2 个审批选项 |
| v2.1 | 系统提示词细化 | 部署指南 |
| v2.2 | 能力边界 + 平台地图 + RAG 扩容 | 24 模块、17 条指路规则、11 条指引原则、219 条 URL |
| v2.3 | RAG 数据质量从"有 URL"到"可检索" | 219 条全量语义补全、平均 8.6 别名 + 11.9 关键词、12 个策略样例 |

---

## v2.3 改动说明（2026-04-16）

> 改动范围：RAG 数据库全量补全 + 新增策略样例 + 项目清理
> 核心主题：RAG 数据质量从"有 URL"升级到"可检索"

### 改动背景

v2.2 将 RAG 数据库从 20 条扩容到 219 条，但这 219 条记录只有 `user_description` 和 `exact_url` 两个字段有值，`page_description`、`aliases`、`keywords` 均为空。这意味着用户用口语化表达（如"上架""铺货""广告报表"）搜索时，RAG 无法匹配到对应 URL，扩容的数据实际上处于不可检索状态。

v2.3 的核心改动：对 219 条记录逐条补全语义字段，让 RAG 从"有数据"变为"能用起来"。

### 一、RAG 数据库全量语义补全（rag_simple_db.json）

对全部 219 条记录补全 3 个关键字段：

| 字段 | 补全前 | 补全后 |
|------|--------|--------|
| `page_description` | 空（0/219 条有值） | 全部填写（219/219），每条用一句话描述页面功能 |
| `aliases` | 空（0/219 条有值） | 全部填写（219/219），平均每条 8.6 个别名 |
| `keywords` | 仅 1 个（=user_description） | 全部扩展（219/219），平均每条 11.9 个关键词 |

**补全内容覆盖：**
- **中文口语别名**：如"上架""铺货""刷评""跟卖""退款"等跨境电商黑话
- **英文原词**：如 Add Product、Listing Upload、FBA Shipment、PPC Campaign
- **缩写/行话**：如 FBA、PPC、ASIN、SKU、A+、VINE
- **操作动词**：如"查看""修改""下载""导出""申诉"
- **场景化表达**：如"为什么被封号""怎么发 FBA""广告跑了多少钱"

**数据分布（20 个类别）：**

| 类别 | 条目数 | 类别 | 条目数 |
|------|--------|------|--------|
| account_settings | 42 | pricing | 6 |
| advertising | 25 | help_support | 6 |
| inventory_fba | 24 | reports | 5 |
| marketplace_homepage | 20 | account_health | 5 |
| finance | 18 | apps_services | 5 |
| other | 17 | growth_tools | 4 |
| product_management | 15 | returns | 2 |
| promotions | 10 | b2b | 2 |
| order_management | 9 | brand | 2 |
| — | — | tax / authentication | 各 1 |

### 二、新增策略生成样例

新增 `非财务人员VAT税务文件禁止访问策略.json`，覆盖以下场景：
- **需求**：禁止运营人员查看和下载 VAT 税务文件，仅财务可访问
- **策略要点**：反选模式（选中除财务部门外所有部门）、完全禁止申请访问、仅 boss 可审批
- **RAG 匹配**：命中 rag_070（Tax Library 页面）
- 累计策略样例：11 → 12 个

### 三、项目清理

删除与本项目无关的文件：
- `体验内容/red_black_tree.cpp`（红黑树 C++ 代码，398 行）
- `体验内容/未命名.md`（空文件）

### 改动文件清单

| 文件 | 操作 | 变更量 |
|------|------|--------|
| amazon-rag-skill/rag_simple_db.json | 更新（全量语义补全） | +5,261 / -1,221 行 |
| amazon-rag-skill/generated_policies/非财务人员VAT税务文件禁止访问策略.json | 新建 | +55 行 |
| 体验内容/red_black_tree.cpp | 删除 | -398 行 |
| 体验内容/未命名.md | 删除 | -0 行 |

---

## v2.2 改动说明（2026-04-14）

> 改动范围：access_policy_skill_package 3 个文件更新 + 2 个新文件 + RAG 数据库扩容
> 详细文档：体验内容/access_policy_skill_package/README_platform_module_map.md

### 改动背景

v2.0 解决了"输出对齐表单"的问题，但当用户需求超出访问策略能力时，Agent 的响应存在两个问题：
1. 展示技术方案（Row-Level Security、API 网关等），小白用户看不懂
2. Agent 只了解"访问策略"这一个模块，无法指路到平台其他功能

v2.2 的核心改动：让 Agent 拥有紫鸟平台的完整能力地图，能精确指路；建议边界收敛到平台内，不推荐外部系统。

### 一、能力边界指引优化（skill_definition.json + 提示词.md）

**not_supported 数据结构重构**

改动前：
```json
{
  "capability": "业务系统字段级权限",
  "alternative": "在业务系统的角色权限模块中配置"
}
```

改动后：
```json
{
  "capability": "业务系统字段级权限",
  "user_explanation": "访问策略可以控制整个页面的访问权限，但没办法只隐藏页面里的某几个字段。",
  "platform_suggestion": "如果您想隐藏的是页面上的某个按钮或特定区域，可以试试「网页元素采集」功能...",
  "if_cannot_solve": "如果需要隐藏的是表格里的某一列数据，这个目前做不到。"
}
```

**on_not_supported 响应模板重写**，新增 response_tone 约束和 routing_fallback 规则。

**conditionally_supported（共用账号场景）** 去掉技术术语，改为平台内替代建议（拆分独立账号）。

**提示词.md 指引原则确立**，从 4 条扩展到 11 条平台内指路场景。

### 二、平台能力地图（新建 platform_module_map.json）

通过 9 次截图收集紫鸟浏览器实际界面，建立完整的平台模块地图：
- 24 个模块（安全监管 9 个、企业管理 7 个、账号/设备 2 个、云号 1 个、更多菜单 4 个、费用管理 1 个）
- 17 条指路规则（routing_rules）
- 每个模块标注置信度（verified/inferred）、导航路径、触发用语

### 三、指引原则收敛

确立核心原则：**Agent 的建议边界 = 紫鸟平台的能力边界**
- 不推荐外部系统（ERP、OA 等）
- 不出现「找技术团队」「找服务商」等指向外部角色的引导
- 平台内有替代方案就推荐，有现成模板就推荐模板
- 确实做不到的需求，坦诚告知「目前做不到」

### 四、RAG 数据库扩容（20 → 219 条）

从紫鸟平台网页资源管理 API 获取真实亚马逊 URL 数据，编写导入脚本自动修复编码 + 自动分类（20 个类别），写入 rag_simple_db.json。

### 五、产出文档

新建 README_platform_module_map.md，记录能力地图的完整产出过程。

### 改动文件清单

| 文件 | 操作 |
|------|------|
| access_policy_skill_package/platform_module_map.json | 新建 |
| access_policy_skill_package/README_platform_module_map.md | 新建 |
| access_policy_skill_package/skill_definition.json | 更新 |
| 体验内容/提示词.md | 更新 |
| amazon-rag-skill/rag_simple_db.json | 覆盖（20→219 条） |
| amazon-rag-skill/rag_backup.json | 备份旧数据 |
| amazon-rag-skill/scripts/import_real_urls.py | 新建 |

---

## v2.0 改动说明（2026-04-13）

> 改动范围：access_policy_skill_package 全部 4 个文件 + approval_based_access_control_skill 1 个文件

---

## 改动背景

v1.0 的 skill 输出是一份自定义结构的 JSON 策略文档，包含审计日志、合规声明、部署建议等字段。这些字段在实际使用的零信任平台「新增访问策略」表单中没有对应的输入位置，导致生成的结果无法直接使用，需要人工翻译才能填入表单。

v2.0 的核心改动：让输出结构 1:1 对齐平台表单字段，生成的结果可以直接照着填表。

---

## 一、config_template.json

### 改了什么

整个模板从自定义抽象字段重构为平台表单字段的精确映射。

### v1.0 的结构

```json
{
  "policy_name": "{{POLICY_NAME}}",
  "policy_type": "time_based_blacklist",
  "time_restrictions": {
    "schedule": {
      "days_of_week": "{{DAYS_OF_WEEK}}",
      "time_range": { "start": "{{START_TIME}}", "end": "{{END_TIME}}" },
      "timezone": "{{TIMEZONE}}"
    }
  },
  "blacklist": {
    "domains": "{{BLOCKED_DOMAINS}}",
    "match_type": "{{MATCH_TYPE}}",
    "block_message": "{{BLOCK_MESSAGE}}"
  },
  "user_scope": {
    "apply_to": "{{APPLY_TO}}",
    "exceptions": { "roles": "{{EXCEPTION_ROLES}}" }
  },
  "enforcement": {
    "strict_mode": true,
    "log_violations": true
  }
}
```

问题：`policy_type`、`blacklist.block_message`、`enforcement`、`timezone` 等字段在平台表单中没有对应输入框。

### v2.0 的结构

```json
{
  "form_fields": {
    "策略名称":      { "type": "text",      "max_length": 24 },
    "生效成员":      { "type": "selector",   "options": ["所有成员","除BOSS外所有成员","指定成员"] },
    "生效平台账号":   { "type": "selector",   "options": ["所有账号","指定账号"] },
    "生效时段": {
      "生效日期":    { "type": "date_range"  },
      "生效周期":    { "type": "weekday_selector", "options": ["一","二","三","四","五","六","七"] },
      "生效时间":    { "type": "time_range"  }
    },
    "访问策略描述":   { "type": "textarea",   "max_length": 400 },
    "访问审批限制": {
      "仅boss账号可审批": { "type": "checkbox" },
      "不允许申请访问":   { "type": "checkbox" }
    }
  },
  "tab_指定网页生效策略": { "type": "url_rule_list" },
  "tab_所有网页通用策略": {
    "复制":        { "options": ["允许且记录","限制"] },
    "文件上传":     { "options": ["允许且记录","限制"] },
    "文件下载":     { "options": ["允许且记录","限制"] },
    "打印":        { "options": ["允许且记录","限制"] },
    "开发者模式":   { "options": ["允许且记录","限制"] },
    "查看密码框":   { "options": ["允许且记录","限制"] }
  }
}
```

每个字段名就是表单上的标签名，每个值就是要填入的内容。

---

## 二、example_output.json

### 改了什么

示例输出从自定义文档格式换成表单填写版，展示"工作时间视频网站限制"场景生成的结果长什么样。

### v1.0 的示例输出

```json
{
  "policy_name": "工作时间视频网站限制",
  "policy_type": "time_based_blacklist",
  "time_restrictions": { "schedule": { "days_of_week": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "time_range": {"start":"09:00","end":"18:00"}, "timezone": "Asia/Shanghai" } },
  "blacklist": { "domains": ["*.bilibili.com","*.iqiyi.com","*.youku.com","*.v.qq.com","*.mgtv.com"], "match_type": "wildcard", "block_message": "工作时间禁止访问视频网站" },
  "user_scope": { "apply_to": "all_users", "exceptions": { "roles": ["BOSS"] } },
  "enforcement": { "strict_mode": true, "log_violations": true }
}
```

问题：`policy_type`、`timezone`、`match_type`、`block_message`、`enforcement` 在表单里填不进去。

### v2.0 的示例输出

```json
{
  "form_output": {
    "策略名称": "工作时间视频网站限制",
    "生效成员": "除BOSS外所有成员",
    "生效平台账号": "所有账号",
    "生效时段": {
      "模式": "指定时段生效",
      "生效日期": { "启用": false },
      "生效周期": { "启用": true, "选中": ["一","二","三","四","五"] },
      "生效时间": { "启用": true, "开始时间": "09:00", "结束时间": "18:00" }
    },
    "访问策略描述": "工作日9:00-18:00禁止访问视频网站（B站、爱奇艺、优酷、腾讯视频、芒果TV），BOSS不受限。防止工作时间浏览娱乐内容影响效率。",
    "访问审批限制": { "仅boss账号可审批": false, "不允许申请访问": false }
  },
  "tab_指定网页生效策略": [
    { "url_rule": "*.bilibili.com", "说明": "B站" },
    { "url_rule": "*.iqiyi.com",    "说明": "爱奇艺" },
    { "url_rule": "*.youku.com",    "说明": "优酷" },
    { "url_rule": "*.v.qq.com",     "说明": "腾讯视频" },
    { "url_rule": "*.mgtv.com",     "说明": "芒果TV" }
  ],
  "tab_所有网页通用策略": {
    "复制": "允许且记录",
    "文件上传": "允许且记录",
    "文件下载": "允许且记录",
    "打印": "允许且记录",
    "开发者模式": "允许且记录",
    "查看密码框": "允许且记录"
  }
}
```

拿到这个 JSON，每一行就是表单上一个框要填的值。

---

## 三、skill_definition.json

### 改了什么

三处关键变更，对话收集流程本身保留不变。

### 变更 1：新增平台能力边界定义

v1.0 没有这个概念，任何用户需求都会走完全流程并生成输出。

v2.0 新增 `platform_capability` 节点，明确列出平台能做和不能做的事：

**能做的（生成表单输出）：**
- URL 级页面屏蔽/放行 → 对应「指定网页生效策略」
- 浏览器行为控制（复制/下载/打印/F12/密码框）→ 对应「所有网页通用策略」
- 按成员/账号/时段生效 → 对应「生效成员」「生效平台账号」「生效时段」
- 审批控制 → 对应「访问审批限制」的两个勾选项

**做不了的（终止流程，给替代方案）：**
- 数据库行级记录过滤（如"6组只能看自己的Case"）→ 建议在业务系统后端实现
- 业务系统字段级权限（如"隐藏价格列"）→ 建议在业务系统角色模块配置
- 多级审批链 / 自定义审批表单 → 平台仅支持两个勾选项，复杂审批需在OA实现
- API / 接口级访问控制 → 建议在API网关实现

### 变更 2：phase_1 从"识别意图"升级为"检查+识别"

v1.0 的 phase_1 只做意图分类（时间黑名单/审批制/只读等）。

v2.0 的 phase_1 先检查平台能力边界：
- 匹配到 `supported` → 继续后续流程
- 匹配到 `not_supported` → 立即告知用户不可实现，给出替代方案，不再生成输出

### 变更 3：phase_4 输出规则对齐表单

v1.0 的 `parameter_mapping` 映射到自定义字段：

```
time_range    → time_restrictions.schedule
blocked_sites → blacklist.domains
user_scope    → user_scope
```

v2.0 映射到表单字段：

```
policy_name          → form_fields.策略名称
effective_members    → form_fields.生效成员
effective_period     → form_fields.生效时段
url_rules            → tab_指定网页生效策略
browser_controls     → tab_所有网页通用策略
approval             → form_fields.访问审批限制
```

新增 `output_rules`：
- 每个字段的值必须直接可填入表单，不需要二次加工
- 策略名称不超过 24 字符
- 策略描述不超过 400 字符
- 表单中没有的字段一律不输出

---

## 四、presets.json

### 改了什么

所有预设值从通用格式改为平台表单的实际选项格式，新增多个预设类别。

### URL 预设格式变更

v1.0：
```json
{ "domains": ["*.bilibili.com", "*.iqiyi.com"] }
```

v2.0：
```json
{ "rules": [
    { "url_rule": "*.bilibili.com", "说明": "B站" },
    { "url_rule": "*.iqiyi.com",    "说明": "爱奇艺" }
]}
```

每条带说明，且新增 `amazon_buyer_checkout` 类别（含已验证的 checkout URL）。

### 时段预设格式变更

v1.0：
```json
{ "days": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "hours": "09:00-18:00" }
```

v2.0：
```json
{ "生效周期": { "启用": true, "选中": ["一","二","三","四","五"] },
  "生效时间": { "启用": true, "开始时间": "09:00", "结束时间": "18:00" } }
```

新增 `after_work`（下班后 17:30-23:59）和 `weekend_only`（仅周末）预设。

### 新增预设类别

v1.0 只有 URL 预设和时间预设。v2.0 新增：
- `member_presets` — 所有成员 / 除BOSS外所有成员 / 指定成员
- `browser_control_presets` — 默认全允许 / 账号安全(限密码框) / 严格锁定(全限制)
- `approval_presets` — 不限制 / 仅boss审批 / 完全禁止

---

## 五、approval_based_access_control_skill.json

### 改了什么

将审批制访问控制的输出从自定义审批流文档收敛为平台表单能支持的范围。

### 审批能力收敛

v1.0 输出包含：
- `approval_chain`：多级审批链（主管 → 经理 → BOSS）
- `temporary_access`：临时权限有效期（15分钟/1小时/自定义）
- `application_form`：自定义申请表单（理由/紧急程度/预计时长）
- `approval_notification`：多渠道通知模板（邮件/短信/APP推送）
- `access_granted_reminder`：访问期间倒计时横幅

v2.0 收敛为平台支持的两个勾选项：
- `仅boss账号可审批`：true / false
- `不允许申请访问`：true / false

超出平台能力的审批功能不再输出。

### 对话流程精简

v1.0 有 6 个 phase，其中 phase_3（收集审批参数）和 phase_4（配置通知）包含大量平台不支持的选项。

v2.0 精简为 5 个 phase：
1. 检查平台能力 + RAG检索URL
2. 收集表单参数
3. 确认配置
4. 生成表单输出
5. 交付 + 同步RAG

### 新增表单填写版示例

提供两个完整的 `example_form_outputs`：
- 示例 1：运营专员访问账户详情页需BOSS审批（审批制）
- 示例 2：买家号Checkout结账页完全屏蔽 17:30起（黑名单）

每个示例都是可以直接照着填表单的 JSON。

---

## v2.3 可行性评估（2026-04-16）

> 评估范围：Skill 提示词体系 + RAG 数据库 + 策略样例
> 评估视角：系统上线后能否满足用户定制访问策略的需求

### 一、v2.3 解决了什么

v2.2 将 RAG 数据库从 20 条扩容到 219 条，但这些数据的 `page_description`、`aliases`、`keywords` 全部为空，处于"有数据但不可检索"的状态。v2.3 对全部 219 条记录完成了语义补全：

| 指标 | v2.2 | v2.3 |
|------|------|------|
| `page_description` 有值 | 0/219 | 219/219 |
| `aliases` 有值 | 0/219 | 219/219（平均 8.6 个） |
| `keywords` 有实际意义 | 0/219 | 219/219（平均 11.9 个） |

抽查数据质量：
- **rag_001 "添加商品"**：别名覆盖"上架""上新""铺货""创建Listing""Add Product"——跨境电商运营的高频口语表达
- **rag_030 "管理亚马逊物流库存"**：标注了"与 rag_018 功能一致"——补全时做了去重/关联标注
- **rag_058 "选品指南针"**：别名包含"蓝海选品""新品机会"，关键词包含"红海产品""品类分析"——场景化表达
- **rag_071 广告**：别名包含"SP广告""PPC广告""CPC广告""投手工具"——正式名称、缩写、行话三类覆盖

补全质量高，中文口语、英文原词、缩写行话三类表达均有覆盖。

### 二、版本迭代脉络

```
v1.0  输出自定义 JSON → 发现平台表单填不进去
  ↓
v2.0  输出对齐平台表单 → 发现超出能力的需求无法处理
  ↓
v2.1  细化系统提示词 → 发现Agent只知道访问策略模块，不知道平台全貌
  ↓
v2.2  加入平台能力地图 + RAG扩容到219条 → 发现219条数据不可检索
  ↓
v2.3  全量语义补全
```

每个版本都是针对上一版实际使用中暴露的问题做修正。这个迭代方式本身就是 Skill 沉淀的活证据——每次发现问题，提取规则，写入结构化提示词，下个版本不再犯同样的错。

### 三、当前系统各组件状态

#### 3.1 Skill 提示词体系 — 可用于生产

三层结构（通用定义 → 场景 Skill → 预设库）经过 4 次迭代，核心机制稳定：

- **能力边界判断**：v2.0 引入，v2.2 加入平台地图（24 个模块 + 17 条指路规则），能拦截不可实现的需求
- **表单对齐输出**：v2.0 起输出格式 1:1 对应表单字段，12 个策略样例验证了输出格式的一致性
- **角色策略模板**：6 种常见角色有完整预制策略
- **平台内指路**：超出访问策略能力时能导航到正确模块

#### 3.2 RAG 数据 — 从"不可用"升级到"基本可用"

219 条数据现在每条都有一句话页面功能描述、8-9 个别名、12 个关键词。

仍然存在的问题：
1. **上下文容量**：219 条 x 约 150 tokens/条 ≈ 33K tokens，加上 Skill 定义（约 15K tokens）+ presets（约 8K tokens），总计约 56K tokens。需要确认飞书 Aily 的系统提示词长度限制是否容纳得下
2. **重复条目**：部分记录指向功能相同的页面（如 rag_018 与 rag_030），可能导致检索结果冗余
3. **时效性**：无 URL 校验机制，Amazon 改了页面路径后系统无感知

#### 3.3 策略样例 — 覆盖面广

12 个样例覆盖的场景类型：

| 场景类型 | 样例 |
|----------|------|
| 单页面审批制 | 运营专员账户详情页审批、实习生定价管理审批 |
| 单页面完全屏蔽 | 客服专员账户详情页禁止 |
| 多页面角色限制 | 财务专员多页面限制、客服访问限制 |
| 买家号屏蔽 | 买家号Checkout结账页屏蔽 |
| 数据隔离（反选模式） | 6组Case数据隔离 |
| 敏感数据保护 | 非财务人员VAT税务文件禁止 |
| 批量角色策略 | 三组策略（表单填写版） |

### 四、上线后能否满足用户需求

#### 能做好的场景

| 场景 | 覆盖率 | 说明 |
|------|--------|------|
| 角色权限批量配置 | ~85% | 6 种角色模板直接输出；自定义角色需用户描述职责后由 LLM 从模块映射表组合 |
| 单页面屏蔽/审批 | ~70% | 目标页面在 219 条已知 URL 中时表现良好；RAG 未命中时需用户补充 |
| 时间条件策略 | ~90% | 预设完善，常见时段直接套用 |
| 不可实现需求的拦截 | ~80% | 能力边界定义 + 平台地图能识别并坦诚告知，不会生成无法执行的配置 |

#### 有风险的场景

| 场景 | 覆盖率 | 风险点 |
|------|--------|--------|
| 数据隔离 | ~50% | 需先确认用户的账号结构（独立/共用），用户自己不清楚时对话会卡住 |
| 复合需求 | ~40% | "工作时间可看不可导出，下班后完全禁止"需拆成多条策略，对话流程面向单条策略设计 |
| 非标页面 | ~30% | 用户描述的页面不在 219 条中，且用户无法提供 URL 时，系统无法生成准确的 URL 规则 |

#### 系统层面的限制（Skill 提示词无法解决）

1. **系统不知道用户的实际环境**：不知道用户公司有哪些部门、角色、账号，"生效成员"和"生效平台账号"字段需用户自行确认
2. **从 JSON 到填表仍是手动的**：输出 JSON 后用户需对照逐项填写，未实现自动化
3. **没有部署后反馈**：策略生效后如果屏蔽了不该屏蔽的页面，系统无法感知和帮助排查

#### 总体判断

v2.3 把系统从"框架完善但数据缺失"推进到了"框架和数据都就绪"的状态。对于常见的单条策略配置需求（占实际需求的大部分），系统已经具备输出正确、可直接填表的 JSON 的能力。它是一个有效的**配置辅助工具**——把"配置访问策略"的门槛从"需要理解平台表单的每个字段和选项"降低到"用自然语言说清楚你想限制谁访问什么"。

剩下的限制主要在系统与平台之间的集成层面（不知道用户环境、不能自动填表），这些不是 Skill 提示词层面能解决的问题。

### 五、后续优先级建议

| 优先级 | 行动 | 预期收益 |
|--------|------|----------|
| P0 | 确认飞书 Aily 的系统提示词长度限制，决定 RAG 数据是嵌入提示词还是走独立检索 | 决定技术路线 |
| P1 | 加入"自定义角色"引导——用户角色不在 6 种模板中时，引导描述职责范围后从模块映射表组合 | 提升角色覆盖率 |
| P2 | 支持复合需求拆分——对话流程中判断是否需拆为多条策略，明确告知用户并逐条生成 | 覆盖复合场景 |
| P3 | URL 输出标注可信度——区分"已验证"和"系统推断，建议确认" | 降低 URL 错误风险 |
| P4 | 清理重复/关联条目——合并指向同一功能的 URL，或在检索结果中去重 | 减少用户困惑 |
