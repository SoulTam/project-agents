# 安全规则

| # | 规则 | 适用范围 | 约束 |
|---|------|---------|------|
| 1 | OWASP 检查 | 测试 Agent | 代码必须通过 OWASP Top 10 检查，安全测试为必要环节 |
| 2 | 敏感信息保护 | 代码开发 Agent | 密码 / API Key / Secret / Token 禁止硬编码，必须用环境变量或配置中心 |
| 3 | CI/CD 安全扫描 | DevOps Agent | CI/CD 工作流必须集成安全扫描（CodeQL / 依赖扫描） |
