<!-- 创建时间: 2026-10-30 21:20 -->
<!-- 最后修改: 2026-10-30 21:20 -->

# content-verification 回归用例集

| case_id | inputs | expected | assert_cmd |
|---------|--------|----------|-----------|
| RC-001 | 蓝图缺"接口定义"章节 | 判定 fail，阻塞项含 chapter:interface | `python tools/scripts/gate_check.py --report <fixture>/G2-blueprint-report.json --task T2026-1030-01 --gate G2`（期望 exit 1） |
| RC-002 | API 条目缺"失败码"列 | 判定 fail，阻塞项含 API-00X | `python tools/scripts/gate_check.py --report <fixture>/api-missing-code.json --task T2026-1030-01 --gate G2`（期望 exit 1） |
| RC-003 | 表结构缺索引定义 | 判定 fail，阻塞项含 TBL-00X | `python tools/scripts/gate_check.py --report <fixture>/tbl-no-index.json --task T2026-1030-01 --gate G2`（期望 exit 1） |
| RC-004 | 蓝图 BLK 总数 42，SP 引用 41 | 判定 fail，原因含 uncovered BLK | `python tools/scripts/gate_check.py --task T2026-1030-01 --gate G3 --blueprint <fixture>/bp.md --plan-dir <fixture>/plan`（期望 exit 1） |
| RC-005 | SP 文档含跳转词"详见" | 判定 fail，原因含 jump words | `python tools/scripts/gate_check.py --task T2026-1030-01 --gate G3 --blueprint <fixture>/bp.md --plan-dir <fixture>/plan`（期望 exit 1，且 ESC-05 无省略词） |

## 说明

| 项 | 说明 |
|----|------|
| fixture | 用例运行时在临时目录构造，禁止污染仓库 |
| 通过判据 | 实际退出码与 expected 一致 |
| 维护 | 新增核查项时同步追加 RC-NNN |
