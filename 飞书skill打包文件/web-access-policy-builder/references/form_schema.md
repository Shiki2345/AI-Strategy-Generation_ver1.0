# Access Policy Form Schema Reference

Source: `config_template.json` v2.1

---

## 1. Form Fields

### 策略名称 (`policy_name`)
- **Type:** text
- **Required:** yes
- **Max length:** 24 characters
- **Hint:** Concise description of the policy purpose.

### 生效成员 (`effective_members`)
- **Type:** selector
- **Required:** yes
- **Options:** `所有成员` | `除BOSS外所有成员` | `指定成员`
- When `指定成员` is selected, provide `custom_members`.

### 生效平台账号 (`effective_accounts`)
- **Type:** selector
- **Required:** yes
- **Options:** `所有账号` | `指定账号`
- When `指定账号` is selected, provide `custom_accounts`.

### 生效时段 (`effective_period`)
- **Type:** compound
- **Required:** yes
- **Mode options:** `一直生效` | `指定时段生效`

When mode = `指定时段生效`, the following sub-fields become available:

| Sub-field | Field ID | Type | Value |
|---|---|---|---|
| 生效日期 | `effective_date_range` | date_range | `start_date` / `end_date` |
| 生效周期 | `effective_weekdays` | weekday_selector | Days: 一, 二, 三, 四, 五, 六, 七 |
| 生效时间 | `effective_time_range` | time_range | `start_time` / `end_time` |

### 访问策略描述 (`policy_description`)
- **Type:** textarea
- **Required:** no
- **Max length:** 400 characters

### 访问审批限制 (`approval_restrictions`)
- **Type:** checkbox_group
- **Options (independent checkboxes):**
  - `仅boss账号可审批`
  - `不允许申请访问`

---

## 2. tab_指定网页生效策略 (`specific_page_rules`)

Per-URL rules. Each entry defines a URL pattern with an access mode and optional behavior controls.

### URL Syntax Rules

| Feature | Symbol | Description |
|---|---|---|
| Protocol | `https://` | Required on every URL. |
| Wildcard | `*` | Fuzzy match across subdomains/TLDs. E.g., `https://*.amazon.*/orders-v3` matches all Amazon sites. |
| Terminator | `$` | Match domain root only; all sub-paths are blocked. E.g., `https://sellercentral-japan.amazon.com/$`. Use `[^/]*` before `$` to match any non-slash chars. |
| Query params | `?` | `preserve_params: false` (default) strips everything after `?`. `preserve_params: true` requires exact match including params. |

**Best practice:** Use `*` wildcards to cover multiple sites in one rule rather than listing each site separately.

### Rule Template

```
url:             <URL pattern>
preserve_params: true | false (default: false)
mode:            可访问 | 已限制
```

- **可访问** -- page is accessible; behavior_controls can restrict specific actions.
- **已限制** -- page is completely blocked; no behavior_controls needed.

### behavior_controls (applies only when mode = 可访问)

| Control | Options | Description |
|---|---|---|
| 复制 | `允许` / `允许且记录` / `限制且记录` | Copy from the browser environment |
| 文件上传 | `允许` / `允许且记录` / `限制且记录` | File upload operations |
| 文件下载 | `允许` / `允许且记录` / `限制且记录` | File download operations |
| 打印 | `允许` / `允许且记录` / `限制且记录` | Print operations |
| 鼠标点击 | `允许` / `限制` | Mouse click; if restricted, page is view-only |
| 键盘输入 | `允许` / `限制` | Keyboard input into text fields |
| 查看密码框 | `允许` / `限制` | View plaintext in password/secret fields |

---

## 3. tab_所有网页通用策略 (`global_page_rules`)

Global behavior rules applied to **all pages** in the account environment. Same 7 controls as above, same options:

| Control | Options |
|---|---|
| 复制 | `允许` / `允许且记录` / `限制且记录` |
| 文件上传 | `允许` / `允许且记录` / `限制且记录` |
| 文件下载 | `允许` / `允许且记录` / `限制且记录` |
| 打印 | `允许` / `允许且记录` / `限制且记录` |
| 鼠标点击 | `允许` / `限制` |
| 键盘输入 | `允许` / `限制` |
| 查看密码框 | `允许` / `限制` |

Note: The first four controls have a three-option scale (允许 / 允许且记录 / 限制且记录). The last three controls are binary (允许 / 限制).
