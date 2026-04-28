# Excel样式配置说明

> 本目录存放Excel文档输出的样式配置文件。

## 使用方式

将样式配置文件命名为`style-config.json`放置于此目录。openpyxl将基于此配置应用Excel样式。

## 配置项说明

```json
{
  "headerStyle": {
    "fontName": "微软雅黑",
    "fontSize": 11,
    "bold": true,
    "alignment": "center",
    "fillColor": "4472C4",
    "fontColor": "FFFFFF"
  },
  "dataStyle": {
    "fontName": "微软雅黑",
    "fontSize": 10,
    "alignment": "left",
    "numberAlignment": "right"
  },
  "conditionalFormat": {
    "已完成": "C6EFCE",
    "进行中": "FFEB9C",
    "未开始": "D9D9D9",
    "阻塞": "FFC7CE"
  },
  "columnWidth": {
    "maxWidth": 50,
    "padding": 2
  },
  "printSetup": {
    "paperSize": "A4",
    "orientation": "landscape",
    "fitToWidth": 1,
    "repeatRows": 1
  }
}
```

## 默认行为

若此目录无`style-config.json`文件，将使用上述默认配置。
