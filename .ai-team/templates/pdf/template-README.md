<!-- 创建时间: 2026-06-22 01:28 -->
<!-- 最后修改: 2026-06-22 01:28 -->

# PDF模板说明

> 本目录存放PDF文档输出的LaTeX模板。

## 使用方式

将LaTeX模板文件命名为`template.tex`放置于此目录。Pandoc将使用XeLaTeX引擎基于此模板生成PDF。

## 模板要求

| 样式项 | 要求 |
|--------|------|
| 文档类 | article或report，A4纸 |
| 页边距 | 上下左右2.5cm |
| 中文字体 | CTeX方案，主字体宋体（SimSun） |
| 标题 | 黑体，各级标题加粗 |
| 正文 | 宋体，12pt，行距1.5倍 |
| 代码块 | listings或minted宏包，浅灰背景 |
| 表格 | booktabs宏包，三线表样式 |
| 页眉 | fancyhdr宏包，左侧文档标题 |
| 页脚 | fancyhdr宏包，居中页码 |
| 目录 | 自动生成，超链接 |

## 默认行为

若此目录无`template.tex`文件，Pandoc将使用默认LaTeX模板。
