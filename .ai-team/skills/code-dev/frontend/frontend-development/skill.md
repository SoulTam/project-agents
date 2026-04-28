---
name: frontend-development
description: 'TypeScript全栈开发，包括类型定义、API集成、状态管理、组件开发和Hooks。当需要实现前端功能代码时使用。'
---

# frontend-development

## 适用Agent
前端开发Agent

## 触发条件
任务分配Agent产出任务分配文档后，按分配顺序轮到前端任务时触发。

## 执行步骤

| 序号 | 步骤 | 详细执行方式 |
|------|------|-------------|
| 1 | 读取任务定义 | 读取`output/task/`下最新任务分配文档，提取分配给前端开发Agent的任务列表及其依赖的技术设计章节 |
| 2 | 读取技术设计 | 读取`output/technical-design/`下最新技术设计文档，提取与当前任务相关的API接口定义和页面交互需求 |
| 3 | 创建项目结构 | 若项目尚未初始化，按照标准前端项目结构创建目录：`src/components/`、`src/pages/`、`src/services/`、`src/store/`、`src/utils/`、`src/styles/`、`src/types/`、`src/hooks/` |
| 4 | 定义TypeScript类型 | 根据API接口的请求/响应结构，在`src/types/`目录下定义对应的TypeScript接口/类型，字段名和类型与后端API严格对应 |
| 5 | 编写API服务层 | 在`src/services/`目录下编写API调用函数，每个函数封装一个接口调用，包含：请求URL、HTTP方法、请求参数类型、响应类型、错误处理，使用axios或fetch实现 |
| 6 | 编写状态管理 | 在`src/store/`目录下编写全局状态管理模块，定义state、actions/mutations，与API服务层对接 |
| 7 | 编写页面组件 | 在`src/pages/`目录下编写页面组件，每个页面组件包含：页面布局、数据展示、用户交互处理、API调用触发 |
| 8 | 编写公共组件 | 在`src/components/`目录下编写可复用组件，每个组件定义清晰的Props接口和Event接口 |
| 9 | 编写工具函数 | 在`src/utils/`目录下编写通用工具函数（格式化、校验、常量等），每个函数必须有TypeScript类型签名和JSDoc注释 |
| 10 | 编写自定义Hooks | 在`src/hooks/`目录下编写可复用的React Hooks或Vue Composables，封装通用逻辑 |
| 11 | 代码输出 | 所有源代码文件写入`output/code/`目录下对应前端项目结构 |

## 输出规范

| 序号 | 规范项 | 要求 |
|------|--------|------|
| 1 | 类型安全 | 所有代码必须使用TypeScript，禁止any类型 |
| 2 | 组件化 | 页面必须拆分为可复用组件，单一职责 |
| 3 | 禁止伪代码 | 所有代码必须可编译运行，不得出现TODO、FIXME、mock实现 |
| 4 | 样式规范 | 使用CSS Modules或Styled Components，禁止全局样式污染 |
| 5 | 性能 | 列表渲染使用虚拟滚动，图片使用懒加载，组件使用memo优化 |
