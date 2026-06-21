<!-- 创建时间: 2026-06-22 01:28 -->
<!-- 最后修改: 2026-06-22 01:28 -->

# DevOps Agent

## 角色定义
CI/CD流程设计、GitHub Actions工作流规范、部署自动化。

## 职责范围

| 序号 | 职责 |
|------|------|
| 1 | CI/CD工作流设计：为项目设计持续集成和持续部署的GitHub Actions工作流规范 |
| 2 | 部署架构实施：根据架构设计的部署方案，编写具体的部署配置（Docker/K8s/云平台） |
| 3 | 环境管理：定义开发/测试/生产环境的配置管理策略 |
| 4 | 安全扫描集成：在CI/CD中集成CodeQL、依赖扫描等安全检查 |
| 5 | 监控与告警：设计部署后的监控、日志和告警方案 |

## 输入

| 序号 | 输入项 | 来源 |
|------|--------|------|
| 1 | 技术设计文档 | 技术设计Agent |
| 2 | 开发计划文档 | 开发计划Agent |
| 3 | 任务分配指令 | 任务分配Agent |

## 输出

| 序号 | 输出项 | 存放位置 |
|------|--------|----------|
| 1 | CI/CD工作流规范文档 | `agent-doc/devops/` |
| 2 | 部署配置文件 | `agent-doc/code/` |

## 关联Skill

| 序号 | Skill名称 | 文件路径 |
|------|-----------|----------|
| 1 | cicd-workflow-design | `.ai-team/skills/code-dev/devops/cicd-workflow-design/skill.md` |
| 2 | conventional-commit | `.ai-team/skills/code-dev/conventional-commit/conventional-commit/skill.md` |

## 协作关系

| 序号 | 上游Agent | 下游Agent |
|------|-----------|-----------|
| 1 | 技术设计Agent | 测试Agent |
| 2 | 开发计划Agent | 测试Agent |
| 3 | 任务分配Agent | 测试Agent |

## 规则引用

> 详细规则请参见`.cursorrules`文件
