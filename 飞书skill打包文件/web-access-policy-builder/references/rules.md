# 可复用规则提取

## 1. 策略类型识别规则

### Rule-001：specific_website识别
**触发条件**：用户查询包含以下任一模式：
- "禁止访问" + [网站类型/域名]
- "限制" + [网站类型/域名]
- "不允许" + "访问" + [网站类型/域名]
- "上班时间" + "禁止" + [网站类型/域名]

**逻辑处理**：
```python
if contains_any(query, ["禁止访问", "限制", "不允许访问"]):
    if contains_all(query, ["所有网站"]):
        return "global_website"  # 优先检查全局模式
    else:
        return "specific_website"
```

**默认配置**：
```json
{
  "policy_type": "specific_website",
  "default_name": "工作时间{网站类型}访问限制策略"
}
```

### Rule-002：global_website识别
**触发条件**：用户查询包含以下任一模式：
- "所有网站" + [操作权限关键词]
- "全局" + [网站] + [权限]
- "控制" + [下载/打印/上传] + "权限"

**操作权限关键词**：["下载", "打印", "上传", "复制", "分享", "保存"]

**逻辑处理**：
```python
if contains_all(query, ["所有网站"]) and contains_any(query, operations_keywords):
    return "global_website"
```

**默认配置**：
```json
{
  "policy_type": "global_website",
  "default_name": "全局网站{操作类型}限制策略"
}
```

## 2. 生效对象解析规则

### Rule-101：排除人群解析
**触发模式**：
- "除了[人群]外的所有员工"
- "除了[职位]外，其他员工"

**人群定义映射表**：
| 用户说法 | 系统映射 | 需要澄清的问题 |
|---------|---------|---------------|
| 老板 | ceo | 具体指CEO还是管理层？ |
| 管理层 | management | 包括哪些级别？ |
| 高管 | executives | VP及以上？ |
| 特定部门 | department:[name] | 具体部门列表？ |

**逻辑处理**：
```python
def parse_target_users(user_response):
    if "除了" in user_response:
        exclusion = extract_between(user_response, "除了", "外的")
        mapping = {
            "老板": ["ceo"],
            "管理层": ["management"],
            "高管": ["executives"]
        }
        exclusions = mapping.get(exclusion, [exclusion])
        return {
            "scope": "all_employees",
            "exclusions": exclusions,
            "needs_clarification": ["人群具体定义", "员工类型包含性"]
        }
```

### Rule-102：员工类型包含性规则
**默认设置**：
```json
{
  "includes_contractors": false,
  "includes_interns": true,
  "includes_remote_employees": true,
  "includes_temporary": false
}
```

**询问模板**：
```
1. 是否包括实习生？
2. 是否包括外包人员？
3. 是否包括远程办公员工？
```

## 3. 时间解析规则

### Rule-201：标准工作时间解析
**触发关键词**：["上班时间", "工作时间", "标准工作时间"]

**默认值**：
```json
{
  "weekdays": ["monday", "tuesday", "wednesday", "thursday", "friday"],
  "time_ranges": [
    {
      "start": "09:00",
      "end": "18:00"
    }
  ],
  "timezone": "Asia/Shanghai",
  "exclude_holidays": true
}
```

### Rule-202：时间段格式验证
**有效格式**：
1. "周一到周五，早上9点到下午6点"
2. "周一至周五 9:00-18:00"
3. "工作日 9:00-12:00, 13:00-18:00"

**解析逻辑**：
```python
def parse_time_range(text):
    patterns = [
        r"(周[一-五]至周[一-五])，?早上?(\d{1,2})点到下午?(\d{1,2})点",
        r"(周[一-五]至周[一-五])\s*(\d{1,2}:\d{2})-(\d{1,2}:\d{2})"
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            weekdays = parse_weekdays(match.group(1))
            start = normalize_time(match.group(2))
            end = normalize_time(match.group(3))
            return {"weekdays": weekdays, "start": start, "end": end}
```

## 4. 限制内容处理规则

### Rule-301：网站域名标准化
**输入处理**：
- "微博" → "weibo.com"
- "抖音网页版" → "douyin.com"
- "小红书" → "xiaohongshu.com"

**域名映射表**：
```json
{
  "微博": "weibo.com",
  "抖音": "douyin.com",
  "小红书": "xiaohongshu.com",
  "Facebook": "facebook.com",
  "Twitter": "twitter.com",
  "Instagram": "instagram.com",
  "微信": "weixin.qq.com",
  "知乎": "zhihu.com"
}
```

### Rule-302：社交媒体网站自动扩展
**触发条件**：用户提到"社交媒体网站"但未指定具体网站

**默认列表**：
```json
[
  {"domain": "weibo.com", "name": "微博", "block_type": "complete"},
  {"domain": "douyin.com", "name": "抖音网页版", "block_type": "complete"},
  {"domain": "xiaohongshu.com", "name": "小红书", "block_type": "complete"},
  {"domain": "facebook.com", "name": "Facebook", "block_type": "complete"},
  {"domain": "twitter.com", "name": "Twitter/X", "block_type": "complete"},
  {"domain": "instagram.com", "name": "Instagram", "block_type": "complete"}
]
```

## 5. 审批流程默认规则

### Rule-401：审批流程基础配置
**默认设置**（当需要审批时）：
```json
{
  "required": true,
  "approver": "ceo",
  "method": "online",
  "max_duration_hours": 4,
  "requires_reason": true,
  "auto_revoke_after_hours": 8,
  "notification_channels": ["email", "im"],
  "escalation_policy": "manager_chain"
}
```

### Rule-402：审批人映射规则
**用户说法** → **系统角色**：
- "BOSS" → "ceo"
- "直属主管" → "direct_manager"
- "HR" → "hr_department"
- "IT部门" → "it_department"

**逻辑处理**：
```python
def map_approver(user_term):
    mapping = {
        "BOSS": "ceo",
        "老板": "ceo",
        "CEO": "ceo",
        "主管": "direct_manager",
        "直属主管": "direct_manager",
        "经理": "direct_manager",
        "HR": "hr_department",
        "人事": "hr_department",
        "IT": "it_department",
        "技术": "it_department"
    }
    return mapping.get(user_term, user_term)
```

## 6. 配置生成规则

### Rule-501：策略ID生成
**格式**：`WEB_ACCESS_POLICY_{type}_{purpose}_{number}`

**type映射**：
- "specific_website" → "01"
- "global_website" → "02"

**purpose提取**：
- 从限制内容提取关键词（如：social_media, download, upload）
- 从时间提取关键词（如：work_hours, full_day）

**number规则**：三位数字，从001开始递增

### Rule-502：自动填充规则
**系统字段**：
- `created_at`：当前ISO 8601时间戳
- `created_by`：当前用户姓名(邮箱)
- `status`：默认"active"

**逻辑字段**：
- 从对话内容自动推导
- 使用默认值填补缺失信息
- 验证字段完整性

## 7. 对话模式规则

### Rule-601：多轮确认顺序
**必须顺序**：
1. 生效对象
2. 生效时间
3. 限制内容
4. 审批流程

**不允许跳过**：任何一轮未明确前不得进入下一轮

### Rule-602：Follow-up触发条件
**必须澄清**：
1. 当用户回答包含模糊术语（如"老板"、"管理人员"）
2. 当时间范围未指定具体时间段
3. 当限制内容只给出类型而未具体化
4. 当审批流程描述不完整

## 8. 规则优先级

### 应用顺序
1. **策略类型规则**（Rule-001, Rule-002） → 最高优先级
2. **对象解析规则**（Rule-101, Rule-102） → 第二步
3. **时间解析规则**（Rule-201, Rule-202） → 第三步
4. **限制内容规则**（Rule-301, Rule-302） → 第四步
5. **审批流程规则**（Rule-401, Rule-402） → 第五步
6. **配置生成规则**（Rule-501, Rule-502） → 最后

### 冲突解决
1. 用户明确指定 > 默认规则
2. 上下文相关规则 > 通用规则
3. 最新信息 > 历史信息

## 9. 规则验证与更新

### 验证时机
每次生成配置后：
1. 检查规则应用是否正确
2. 验证输出是否符合预期
3. 记录规则使用效果

### 更新条件
当出现以下情况时更新规则：
1. 新对话模式出现3次以上
2. 现有规则导致配置错误
3. 用户明确要求新功能

## 10. 规则库结构

```
rules/
├── strategy_type/     # 策略类型识别规则
├── target_users/      # 目标用户解析规则
├── schedule/         # 时间安排解析规则
├── restrictions/     # 限制内容处理规则
├── approval/         # 审批流程规则
└── generation/       # 配置生成规则
```

每个目录包含：
- `primary_rules.md`：核心规则
- `examples.md`：应用示例
- `validation.md`：验证方法