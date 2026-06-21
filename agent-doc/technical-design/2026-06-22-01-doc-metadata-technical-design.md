<!-- 创建时间: 2026-06-22 01:28 -->
<!-- 最后修改: 2026-06-22 01:28 -->

# 技术设计文档：文档元数据时间戳规则

## 时间格式与命令
- 格式：`yyyy-MM-dd HH:mm`
- 获取命令：PowerShell `Get-Date -Format "yyyy-MM-dd HH:mm"`

## 文件头格式
```
<!-- 创建时间: 2026-06-22 01:23 -->
<!-- 最后修改: 2026-06-22 01:23 -->
```

## 创建文件时
1. `$now = Get-Date -Format "yyyy-MM-dd HH:mm"`
2. 写入文件头：创建时间=最后修改=$now

## 更新文件时
1. 读取文件第1行（创建时间），保持不动
2. `$now = Get-Date -Format "yyyy-MM-dd HH:mm"`
3. 替换第2行（最后修改）的时间戳
4. 保存文件

## 批量更新脚本思路
```powershell
$files = Get-ChildItem -Path "." -Recurse -Filter "*.md" -File
$now = Get-Date -Format "yyyy-MM-dd HH:mm"
foreach ($file in $files) {
    $content = Get-Content -LiteralPath $file.FullName -Raw
    if ($content -match "^<!-- 创建时间:") {
        # 已有头部，更新最后修改
        $content = $content -replace "(<!-- 最后修改: )[\d\-: ]+", "`$1$now"
    } else {
        # 无头部，插入
        $content = "<!-- 创建时间: $now -->`r`n<!-- 最后修改: $now -->`r`n`r`n" + $content
    }
    Set-Content -LiteralPath $file.FullName -Value $content -Encoding UTF8
}
```
