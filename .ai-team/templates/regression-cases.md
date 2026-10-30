<!-- 创建时间: 2026-10-30 21:20 -->
<!-- 最后修改: 2026-10-30 21:20 -->

# 回归用例集模板

## D8 字段（4 项）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| case_id | string | 是 | `RC-NNN`，全局唯一 |
| inputs | string | 是 | 输入文件/参数（可多个） |
| expected | string | 是 | 期望退出码或期望字段值 |
| assert_cmd | string | 是 | 可执行命令，禁止"人工判断"作唯一断言 |

## 用例表

| case_id | inputs | expected | assert_cmd |
|---------|--------|----------|-----------|
| RC-001 | {输入} | exit 0 | `python tools/scripts/gate_check.py --task {id} --gate G3` |
| RC-002 | {输入} | exit 1，含 {原因} | `python tools/scripts/link_check.py` |

## 执行口径

| 项 | 要求 |
|----|------|
| 执行 | 逐条真实执行，记录退出码 |
| 通过 | expected 与实际一致 |
| 失败 | 任一不一致即整体 fail（E-RGN-01） |
| 归档 | 结果写入 intake 记录的 regression 字段 |
