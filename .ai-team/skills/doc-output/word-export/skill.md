---
name: word-export
description: 'Markdown转Word(Pandoc+reference.docx模板)。当需要将Markdown文档转换为Word格式时使用。'
---

# word-export

## 适用Agent
文档输出Agent

## 触发条件
PM Agent指定输出Word格式文档时触发。

## 执行步骤

| 序号 | 步骤 | 详细执行方式 |
|------|------|-------------|
| 1 | 读取源文档 | 读取`output/`下指定的Markdown源文件，解析文档结构（标题层级、段落、表格、代码块、列表、图片引用） |
| 2 | 检查模板 | 检查`.ai-team/templates/word/reference.docx`是否存在，不存在则使用Pandoc默认模板并输出警告提示替换为企业模板 |
| 3 | 内容预处理 | 将Markdown中的Mermaid代码块转为图片占位符（需预先导出为PNG），将表格格式标准化为Pandoc可解析的Pipe Table，处理中文字体映射 |
| 4 | 执行Pandoc转换 | 执行命令：`pandoc {源文件}.md --reference-doc=.ai-team/templates/word/reference.docx -o {输出文件}.docx --toc --toc-depth=3 --number-sections`，生成包含目录和章节编号的Word文档 |
| 5 | 样式校验 | 检查生成的Word文档：封面页是否正确、目录是否生成、标题层级样式是否一致、表格是否有边框、代码块是否有底色背景、页眉页脚是否显示 |
| 6 | 输出文档 | 将Word文档写入`agent-doc/doc/`目录，文件命名格式：`{源文档名}-{yyyy-MM-dd}.docx` |

## 输出规范

| 序号 | 规范项 | 要求 |
|------|--------|------|
| 1 | 模板 | 必须使用`.ai-team/templates/word/reference.docx`参考模板 |
| 2 | 目录 | 自动生成目录，深度3级 |
| 3 | 章节编号 | 标题自动编号 |
| 4 | 表格 | 统一表格样式，表头加粗居中，边框完整 |
| 5 | 代码块 | 等宽字体，浅灰底色背景 |
| 6 | 页眉页脚 | 页眉含文档标题，页脚含页码 |
