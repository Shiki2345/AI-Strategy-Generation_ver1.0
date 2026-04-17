# Web访问策略JSON Schema

## 基本结构
```json
{
  "policy_id": "WEB_ACCESS_POLICY_001",
  "policy_name": "策略名称",
  "policy_type": "specific_website 或 global_website",
  "description": "策略描述",
  "status": "active 或 inactive",
  "created_at": "2026-04-10T10:15:55+08:00",
  "created_by": "创建人姓名 (邮箱)",
  
  "target_users": {},
  "schedule": {},
  "restrictions": {},
  "approval_process": {},
  "enforcement": {},
  "monitoring": {}
}
```

## target_users（目标用户）
```json
"target_users": {
  "scope": "all_employees 或 department_specific",
  "exclusions": ["ceo", "management"],
  "includes_contractors": true/false,
  "includes_interns": true/false,
  "includes_remote_employees": true/false,
  "departments": ["产品部", "技术部"] // 当scope为department_specific时
}
```

## schedule（时间安排）
```json
"schedule": {
  "timezone": "Asia/Shanghai",
  "recurrence": "daily 或 weekly 或 monthly",
  "weekdays": ["monday", "tuesday", "wednesday", "thursday", "friday"],
  "weekend_days": ["saturday", "sunday"],
  "time_ranges": [
    {
      "start": "09:00",
      "end": "18:00"
    }
  ],
  "exclude_holidays": true,
  "holiday_schedule": "national_holidays"
}
```

## restrictions（限制内容）

### specific_website类型
```json
"restrictions": {
  "type": "website_blocking",
  "websites": [
    {
      "domain": "weibo.com",
      "name": "微博",
      "block_type": "complete 或 partial",
      "subdomains": ["*.weibo.com"]
    }
  ],
  "block_level": "domain_level 或 url_pattern",
  "exceptions": {
    "allowed_urls": ["weibo.com/business"],
    "allowed_ips": []
  }
}
```

### global_website类型
```json
"restrictions": {
  "type": "operation_control",
  "allowed_operations": ["browse", "view"],
  "blocked_operations": ["download", "print", "upload", "copy"],
  "file_types": {
    "blocked": ["exe", "zip", "rar"],
    "allowed": ["pdf", "docx", "xlsx"]
  }
}
```

## approval_process（审批流程）
```json
"approval_process": {
  "required": true,
  "approver": "ceo 或 manager 或 hr 或 it_department",
  "method": "online 或 offline",
  "max_duration_hours": 4,
  "requires_reason": true,
  "auto_revoke_after_hours": 8,
  "notification_channels": ["email", "im"],
  "escalation_policy": "manager_chain"
}
```

## enforcement（执行机制）
```json
"enforcement": {
  "action": "block_with_notification 或 redirect 或 warning",
  "notification_message": "访问受限提示信息",
  "redirect_url": "重定向URL（可为空）",
  "logging_level": "basic 或 detailed 或 none",
  "grace_period_minutes": 5,
  "remediation_steps": ["申请特殊权限", "联系IT支持"]
}
```

## monitoring（监控机制）
```json
"monitoring": {
  "alert_threshold": 5,
  "report_frequency": "daily 或 weekly 或 monthly",
  "notify_admins": ["it_department", "hr_department", "security_team"],
  "metrics": ["access_attempts", "approval_requests", "violations"],
  "retention_days": 90
}
```

## 字段说明表

| 字段路径 | 类型 | 必填 | 默认值 | 说明 |
|---------|------|------|--------|------|
| policy_id | string | ✓ | - | 策略唯一标识符 |
| policy_name | string | ✓ | - | 策略显示名称 |
| policy_type | enum | ✓ | - | specific_website或global_website |
| description | string | ✓ | - | 策略功能描述 |
| status | enum | ✓ | active | active/inactive |
| created_at | timestamp | ✓ | 当前时间 | ISO 8601格式 |
| created_by | string | ✓ | 当前用户 | 姓名(邮箱)格式 |
| target_users.scope | enum | ✓ | all_employees | 用户范围定义 |
| target_users.exclusions | array | ✗ | [] | 排除的用户组 |
| target_users.includes_* | boolean | ✗ | true | 各类员工包含性 |
| schedule.timezone | string | ✓ | Asia/Shanghai | 时区设置 |
| schedule.recurrence | enum | ✓ | weekly | 时间循环周期 |
| schedule.weekdays | array | ✓ | 所有工作日 | 生效工作日 |
| schedule.time_ranges | array | ✓ | 9:00-18:00 | 生效时间段 |
| restrictions.type | enum | ✓ | - | 限制类型 |
| restrictions.websites | array | 条件 | - | specific_website时必填 |
| restrictions.blocked_operations | array | 条件 | - | global_website时必填 |
| approval_process.required | boolean | ✓ | true | 是否需审批 |
| approval_process.approver | enum | ✓ | ceo | 审批人角色 |
| approval_process.method | enum | ✓ | online | 审批方式 |
| approval_process.max_duration_hours | number | ✓ | 4 | 最长有效期 |
| enforcement.action | enum | ✓ | block_with_notification | 执行动作 |
| enforcement.logging_level | enum | ✓ | detailed | 日志级别 |
| monitoring.alert_threshold | number | ✓ | 5 | 告警阈值 |
| monitoring.report_frequency | enum | ✓ | weekly | 报告频率 |

## 验证规则

1. **policy_id格式**：必须匹配正则 `^WEB_ACCESS_POLICY_\d{3}$`
2. **时间范围验证**：`schedule.time_ranges`中所有时间范围不得重叠
3. **域名格式**：`restrictions.websites[*].domain`必须是有效域名格式
4. **时区验证**：`schedule.timezone`必须是IANA时区数据库中的有效时区
5. **审批人存在性**：如果`approval_process.required=true`，则`approver`不能为空

## 示例值

```json
{
  "policy_id": "WEB_ACCESS_POLICY_001",
  "policy_name": "工作时间社交媒体访问限制策略",
  "policy_type": "specific_website",
  "description": "在工作时间限制员工访问社交媒体网站，提高工作效率",
  "status": "active",
  "created_at": "2026-04-10T10:15:55+08:00",
  "created_by": "何青杨 (qingyang_he@fzzixun.com)"
}
```