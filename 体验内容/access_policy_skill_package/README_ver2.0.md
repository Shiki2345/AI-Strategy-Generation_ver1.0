# Skill 文件 v2.0 改动说明

> 改动日期：2026-04-13
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
