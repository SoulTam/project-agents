<!-- 创建时间: 2026-06-22 01:28 -->
<!-- 最后修改: 2026-06-22 01:28 -->

---
name: java-development
description: 'Spring Boot项目初始化(Spring Initializr+Docker Compose)和企业级Java全栈开发。当需要实现Java后端功能代码时使用。'
---

# java-development

## 适用Agent
Java开发Agent

## 触发条件
任务分配Agent产出任务分配文档后，按分配顺序轮到Java任务时触发。

## 前置检查

| 序号 | 检查项 | 执行方式 |
|------|--------|----------|
| 1 | Java版本 | 执行 `java -version` 确认Java 21+已安装 |
| 2 | Docker环境 | 执行 `docker --version` 和 `docker compose version` 确认已安装 |
| 3 | 项目状态 | 检查 `output/code/` 下是否已有项目结构，若无则执行项目初始化 |

## 项目初始化（仅首次）

当项目尚未初始化时，按以下步骤创建Spring Boot项目骨架：

| 序号 | 步骤 | 详细执行方式 |
|------|------|-------------|
| I-1 | 下载项目模板 | 执行 `curl https://start.spring.io/starter.zip -d artifactId={项目名} -d bootVersion=3.4.5 -d dependencies=lombok,configuration-processor,web,data-jpa,postgresql,data-redis,data-mongodb,validation,cache,testcontainers -d javaVersion=21 -d packageName={基础包名} -d packaging=jar -d type=maven-project -o starter.zip` |
| I-2 | 解压项目 | 执行 `unzip starter.zip -d output/code/{项目名}` |
| I-3 | 清理临时文件 | 执行 `rm -f starter.zip` |
| I-4 | 添加额外依赖 | 在 `pom.xml` 中添加：springdoc-openapi-starter-webmvc-ui（API文档）、archunit-junit5（架构测试） |
| I-5 | 配置application.properties | 添加SpringDoc配置（swagger-ui）、Redis配置（host/port/password）、JPA配置（PostgreSQL连接/hbm2ddl/show-sql）、MongoDB配置（host/port/auth/database） |
| I-6 | 创建docker-compose.yaml | 在项目根目录创建，包含：redis:6（密码/port/卷映射）、postgresql:17（密码/port/卷映射）、mongo:8（root账号/port/卷映射） |
| I-7 | 更新.gitignore | 添加 `redis_data/`、`postgres_data/`、`mongo_data/` |
| I-8 | 验证项目 | 执行 `./mvnw clean test` 确认项目可正常编译测试 |

## 执行步骤

| 序号 | 步骤 | 详细执行方式 |
|------|------|-------------|
| 1 | 读取任务定义 | 读取`agent-doc/task/`下最新任务分配文档，提取分配给Java开发Agent的任务列表及其依赖的技术设计章节 |
| 2 | 读取技术设计 | 读取`agent-doc/technical-design/`下最新技术设计文档，提取与当前任务相关的数据模型定义和API接口定义 |
| 3 | 创建项目结构 | 若项目尚未初始化，执行上方"项目初始化"流程；若已初始化，确认目录结构完整：`src/main/java/{包路径}/controller/`、`service/`、`service/impl/`、`repository/`、`model/`、`dto/`、`config/`、`exception/`，`src/main/resources/`，`src/test/java/{包路径}/` |
| 4 | 编写数据模型代码 | 根据技术设计中的数据模型定义，编写JPA Entity类，包含：类名、字段（类型+注解）、主键标注、索引标注、关联关系标注，每个Entity类写入`model/`目录 |
| 5 | 编写DTO类 | 为每个API接口的请求和响应编写DTO类，包含字段、校验注解（@NotNull/@Size等），写入`dto/`目录 |
| 6 | 编写Repository层 | 为每个Entity编写Repository接口，继承JpaRepository或自定义查询方法，写入`repository/`目录 |
| 7 | 接口类型决策 | 读取技术设计文档中的接口类型决策结果，对每个交互点按`.ai-team/knowledge-base/api-strategies/interface-selection-strategy.md`确认接口类型：Interface类型的创建Interface接口文件和Impl实现类文件，接口文件写入`service/`目录，实现类写入`service/impl/`目录；程序直接调用类型的在调用方直接注入实现类，无需Interface抽象 |
| 8 | 编写Service层 | 为每个功能模块编写Service类，包含业务逻辑方法，方法内调用Repository操作数据，事务边界用@Transactional标注，写入`service/`目录 |
| 9 | 编写Controller层 | 为每个API接口编写Controller方法，使用@RestController和@RequestMapping标注，方法参数使用DTO接收并加@Valid校验，返回统一响应格式，写入`controller/`目录 |
| 10 | 编写异常处理 | 在`exception/`目录创建全局异常处理类（@RestControllerAdvice），异常包装时使用`new CustomException("描述", originalException)`保留原始异常信息和堆栈，禁止用自定义消息覆盖原始异常 |
| 11 | 编写配置类 | 在`config/`目录创建必要的配置类（数据源配置、安全配置、OpenAPI配置等），使用@Configuration和@Bean标注 |
| 12 | 代码输出 | 所有源代码文件写入`output/code/`目录下对应包路径，保持标准Maven项目结构 |

## 输出规范

| 序号 | 规范项 | 要求 |
|------|--------|------|
| 1 | 代码规范 | 遵循阿里巴巴Java开发手册规范 |
| 2 | 异常处理 | 必须保留原始异常堆栈，禁止覆盖 |
| 3 | 禁止伪代码 | 所有代码必须可编译运行，不得出现TODO、FIXME、mock实现 |
| 4 | 注释 | 类和public方法必须有Javadoc注释 |
| 5 | 日志 | 使用SLF4J+Logback，关键操作必须记录日志 |
| 6 | API文档 | 使用springdoc-openapi自动生成，Controller方法必须添加@Operation注解 |
| 7 | 架构测试 | 关键架构规则使用ArchUnit验证（分层规则、包依赖规则） |
| 8 | 集成测试 | 使用Testcontainers进行数据库集成测试 |
