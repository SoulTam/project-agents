**FREE
// ============================================================
// 订单处理程序 - 完整示例
// 功能：读取订单、计算金额、更新状态、写入日志
// ============================================================

/COPY QRPGLESRC,INITSRV
/COPY QPROTOSRC,UTIL_H

// ─── 文件声明 ───
DCL-F ORDERH DISK USAGE(I) KEY;           // 订单主表（只读）
DCL-F ORDERD DISK USAGE(IO) KEY;          // 订单明细（读写）
DCL-F CUSTMAST DISK USAGE(I) KEY;         // 客户主数据（只读）
DCL-F PRODMAST DISK USAGE(I);             // 产品主数据（只读）
DCL-F ORDLOG DISK USAGE(O);               // 订单日志（只写）

// ─── Data Area 声明 ───
DCL-DTAARA ORDCTL TYPE(*CHAR) LEN(200);   // 订单控制区

// ─── Data Area DS 拆解 ───
DCL-DS ORDCTL_DS LEN(200) QUALIFIED;
  STATUS CHAR(1);                         // 状态：A=有效, I=无效
  COUNTER PACKED(5:0);                    // 处理计数器
  ORDER_DATE CHAR(8);                     // 订单日期
  CUSTOMER_CODE CHAR(5);                  // 客户代码
  ERROR_FLAG CHAR(1);                     // 错误标志
END-DS;

// ─── 工作变量 ───
DCL-S W_TOTAL PACKED(11:2);              // 金额合计
DCL-S W_TAX PACKED(9:2);                 // 税额
DCL-S W_COUNT INT(5);                     // 计数器
DCL-S W_STATUS CHAR(1);                   // 状态码

// ============================================================
// 主程序
// ============================================================

// 读取订单主表
SETLL *START ORDERH;
READ ORDERH;

// 初始化 Data Area
IN ORDCTL;
ORDCTL_DS.COUNTER = 0;
ORDCTL_DS.ERROR_FLAG = 'N';

// 处理订单明细循环
DOW NOT %EOF(ORDERD);
  CHAIN ORDERD;

  // 跳过已取消的明细
  IF DTLSTS = 'C';
    READ ORDERD;
    ITER;
  ENDIF;

  // 查找产品信息
  CHAIN PRODCD PRODMAST;
  IF NOT %FOUND;
    ORDCTL_DS.ERROR_FLAG = 'Y';
    READ ORDERD;
    ITER;
  ENDIF;

  // 计算金额（单价 × 数量）
  W_TOTAL = PRICE * QTY;

  // 计算税额（8%）
  W_TAX = W_TOTAL * 0.08;

  // 更新明细记录
  ORDAMT = W_TOTAL;
  ORDTAX = W_TAX;
  ORDSTS = 'P';  // 处理中
  UPDATE ORDERD;

  // 查找客户信息
  CHAIN CUSTCD CUSTMAST;
  IF NOT %FOUND;
    CUSTNAME = '*UNKNOWN';
  ENDIF;

  // 更新客户累计金额
  CUSTTOTAL = CUSTTOTAL + W_TOTAL;
  UPDATE CUSTMAST;

  // 计数器递增
  ORDCTL_DS.COUNTER = ORDCTL_DS.COUNTER + 1;
  ORDCTL_DS.CUSTOMER_CODE = CUSTCD;
  ORDCTL_DS.ORDER_DATE = ORDDT;

  READ ORDERD;
ENDDO;

// 更新订单主表状态
IF ORDCTL_DS.ERROR_FLAG = 'N';
  ORDSTS = 'C';  // 完成
ELSE;
  ORDSTS = 'E';  // 有错误
ENDIF;
UPDATE ORDERH;

// 写入日志
LOGORD = ORDNO;
LOGSTS = ORDSTS;
LOGCNT = ORDCTL_DS.COUNTER;
LOGTIME = %TIMESTAMP();
WRITE ORDLOG;

// 写回 Data Area
OUT ORDCTL;

// 调用其他程序
CALL 'ORDNOTI';
CALLP SENDMAIL(ORDNO: CUSTCD: W_TOTAL);

// SQL 操作
EXEC SQL
  UPDATE ORDERH
  SET STATUS = :ORDSTS,
      UPDATE_TIME = CURRENT_TIMESTAMP
  WHERE ORDNO = :ORDNO;

// 结束
*INLR = *ON;
RETURN;
