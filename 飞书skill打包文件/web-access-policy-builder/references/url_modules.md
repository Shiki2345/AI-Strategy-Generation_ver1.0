# Amazon URL 模块映射表

当用户按角色/功能模块配置策略时，使用以下映射表确定需要屏蔽或放行的 URL 通配符。

## 功能模块 → URL 规则

| 模块 | URL 通配符 | 说明 |
|------|----------|------|
| 账户/用户权限管理 | `https://*.amazon.*/sw/AccountInfo` | 账户详情/设置页 |
| | `https://*.amazon.*/user-manager` | 用户权限管理 |
| 商品管理(Inventory) | `https://*.amazon.*/inventory` | 库存管理 |
| | `https://*.amazon.*/product-search` | 产品上架 |
| 广告 | `https://*.amazon.*/advertising` | Seller Central广告板块 |
| | `https://advertising.amazon.com` | 广告独立控制台 |
| 买家消息(Communication) | `https://*.amazon.*/messaging/inbox` | 买家消息 |
| 订单(Orders) | `https://*.amazon.*/orders-v3` | 订单管理 |
| 财务/资金 | `https://*.amazon.*/payments` | 资金管理/支付报告 |
| | `https://*.amazon.*/gp/payments-account` | 结算汇总/财务报表 |
| 业务报告 | `https://*.amazon.*/business-reports` | 业务报告 |
| 发货计划(Shipment Plan) | `https://*.amazon.*/fba/sendtoamazon` | FBA发货计划 |

## 设置菜单（全部12个子页面）

当用户说"屏蔽设置下所有页面"时，使用以下完整列表：

| 菜单项 | URL 通配符 |
|-------|----------|
| 账户信息 | `https://*.amazon.*/global-dashboard` |
| 管理账户 | `https://*.amazon.*/account/management` |
| 通知首选项 | `https://*.amazon.*/notifications/preferences` |
| 登录设置 | `https://*.amazon.*/ap/cnep` |
| 退货设置 | `https://*.amazon.*/gp/returns/settings` |
| 礼品选项 | `https://*.amazon.*/gcx/gift-options` |
| 配送设置 | `https://*.amazon.*/sbr` |
| 税务设置 | `https://*.amazon.*/tax` |
| 用户权限 | `https://*.amazon.*/gp/account-manager/home.html` |
| 您的信息和政策 | `https://*.amazon.*/gp/help-content/home.html` |
| 亚马逊物流 | `https://*.amazon.*/fba/settings` |
| 卖家信息 | `https://*.amazon.*/sw/AccountInfo` |

## 买家号结账页面

当用户说"屏蔽买家号checkout/结账"时：

| 页面 | URL | 验证状态 |
|------|-----|---------|
| Secure Checkout结账页 | `https://www.amazon.com/checkout/` | 已验证 |
| 购物车页面 | `https://www.amazon.com/gp/cart/view.html` | 部分验证 |
| 旧版结账页 | `https://www.amazon.com/gp/buy/spc/handlers/display.html` | 兜底覆盖 |

## 金融/资金相关页面（完整）

当用户说"屏蔽金融/财务页面"时：

| 页面 | URL 通配符 |
|------|----------|
| 付款/结算页面 | `https://*.amazon.*/payments` |
| 银行账户页面 | `https://*.amazon.*/sw/AccountInfo/DepositMethod` |
| 付款信息汇总 | `https://*.amazon.*/global-dashboard/payment-information` |
| 卖家钱包新版 | `https://*.amazon.*/mario/sellerwallet/` |
| 卖家钱包计划 | `https://*.amazon.*/gc/sellerwallet-program` |
| 税务总面板 | `https://*.amazon.*/tax` |
| 税务身份认证 | `https://*.amazon.*/tax-interview` |
| 税务文档库 | `https://*.amazon.*/gp/tax/tax-library.html` |
| 税务信息汇总 | `https://*.amazon.*/global-dashboard/tax-information` |
| 税务报告 | `https://*.amazon.*/managetaxes/global-transaction-reports` |

## 使用规则

1. 角色策略用"穷举屏蔽"实现白名单效果：列出该角色不能访问的所有模块URL，没列的即可访问
2. 跨站点页面优先用 `https://*.amazon.*/路径` 一条规则覆盖，不逐站点列多条
3. 买家号页面使用精确域名 `https://www.amazon.com/`，不用通配符
