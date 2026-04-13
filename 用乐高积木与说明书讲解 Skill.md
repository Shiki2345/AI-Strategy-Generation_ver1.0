
## 基础概念对应

| 乐高概念 | Skill 对应概念 |
|---|---|
| 零散积木颗粒 | Claude 的基础工具（Read、Edit、Bash…） |
| 主题说明书（如星战飞船） | 一个 Skill（如 `/commit`、`/simplify`） |
| 按说明书拼出的成品 | Skill 执行后的完整结果 |
| 说明书封面的适用场景 | Skill 的触发条件（TRIGGER when…） |

---

## 没有 Skill 的情况

> 想象你面前有一堆散装乐高，却**没有说明书**。

你需要自己决定：先拼底盘还是先拼驾驶舱？用哪块砖？顺序是什么？

对应 Claude：每次都要从头思考用哪些工具、以什么顺序执行复杂任务。

---

## 有了 Skill 之后

> 你拿到了官方说明书 —— 打开第一页，步骤清晰：

```
第1步：检查零件清单（git status）
第2步：确认拼装差异（git diff）
第3步：按图纸组装（生成 commit message）
第4步：完成拼装（git commit）
```

说明书不增加新积木，只是**把现有积木按最佳顺序组合起来**。

---

## Skill 的三个关键部分（对应说明书三要素）

**1. 封面标题** = Skill 名称

```
/commit   /simplify   /loop   /claude-api
```

**2. 适用场景提示**（说明书封面写的"适合8岁以上"）

```
TRIGGER when: 用户要提交代码时
TRIGGER when: 代码导入 anthropic SDK 时
```

**3. 拼装步骤**（说明书内页）

```
展开为完整的指令序列 →
Claude 按步骤逐一执行工具调用
```

---

## `Skill` 工具本身 = 拿起说明书这个动作

```python
Skill({ skill: "commit" })
```

> 就像你从积木盒里翻出正确的说明书，然后开始按图索骥。

---

## 目前可用的说明书（已安装的 Skill 套装）

| 说明书（Skill） | 能拼出什么 |
|---|---|
| `simplify` | 代码质量审查 + 重构 |
| `loop` | 定时重复执行某任务 |
| `claude-api` | 构建/调试 Claude API 应用 |
| `pm-market-research:*` | 市场调研、用户分析、竞品分析系列 |
| `update-config` | 修改 Claude Code 配置行为 |

---

## 一句话总结

Skill 就是乐高说明书 —— 它不给你新积木，但告诉你**用已有积木完成复杂作品的最佳步骤**。
