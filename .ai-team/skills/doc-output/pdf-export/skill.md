<!-- 创建时间: 2026-06-22 01:28 -->
<!-- 最后修改: 2026-06-22 01:28 -->

---
name: pdf-export
description: 'Markdown转PDF(Pandoc+XeLaTeX+template.tex中文支持)。当需要将Markdown文档转换为PDF格式时使用。'
---

# pdf-export

## 适用Agent
文档输出Agent

## 触发条件
PM Agent指定输出PDF格式文档时触发。

## 执行步骤

| 序号 | 步骤 | 详细执行方式 |
|------|------|-------------|
| 1 | 读取源文档 | 读取`output/`下指定的Markdown源文件，解析文档结构 |
| 2 | 检查模板 | 检查`.ai-team/templates/pdf/template.tex`是否存在，不存在则使用Pandoc默认LaTeX模板并输出警告 |
| 3 | 内容预处理 | 将Mermaid代码块转为图片引用，处理LaTeX特殊字符转义（&、%、$、#、_、{、}、~、^、\），配置中文字体为CTeX方案 |
| 4 | 执行Pandoc转换 | 执行命令：`pandoc {源文件}.md --template=.ai-team/templates/pdf/template.tex --pdf-engine=xelatex -o {输出文件}.pdf --toc --toc-depth=3 --number-sections -V CJKmainfont="SimSun" -V mainfont="SimSun"`，使用XeLaTeX引擎支持中文 |
| 5 | 校验PDF | 检查生成的PDF：书签是否完整、超链接是否可点击、中文字体是否正常显示、图片是否嵌入、页码是否连续 |
| 6 | 输出文档 | 将PDF文档写入`agent-doc/doc/`目录，文件命名格式：`{源文档名}-{yyyy-MM-dd}.pdf` |

## 输出规范

| 序号 | 规范项 | 要求 |
|------|--------|------|
| 1 | 模板 | 必须使用`.ai-team/templates/pdf/template.tex`模板 |
| 2 | 引擎 | 使用XeLaTeX引擎确保中文支持 |
| 3 | 目录 | 自动生成目录，深度3级，带书签 |
| 4 | 章节编号 | 标题自动编号 |
| 5 | 字体 | 中文使用宋体（SimSun），英文使用默认衬线字体 |
| 6 | 页面 | A4纸，上下左右边距2.5cm，页眉含文档标题，页脚居中页码 |
