**FREE
// ============================================================
// 字段传递链路 + 条件逻辑示例
// ============================================================

/COPY QRPGLESRC,INITSRV

// ─── 文件声明 ───
DCL-F ORDERS DISK USAGE(IO);              // 订单文件
DCL-F ITEMS DISK USAGE(IO);               // 明细文件

// ─── Data Area 声明 ───
DCL-DTAARA PRTCTL TYPE(*CHAR) LEN(100);

// ─── Data Area DS 拆解 ───
DCL-DS PRTCTL_DS LEN(100) QUALIFIED;
  PRINT_DATE CHAR(8);
  PRINT_TIME CHAR(6);
  COPIES PACKED(3:0);
  PRIORITY CHAR(1);
  ROUTE_CODE CHAR(10);
END-DS;

// ─── 工作变量 ───
DCL-S W_RAW_PRICE PACKED(11:2);
DCL-S W_DISCOUNT_RATE PACKED(5:2);
DCL-S W_DISCOUNT_AMT PACKED(11:2);
DCL-S W_NET_PRICE PACKED(11:2);
DCL-S W_TAX_RATE PACKED(3:2);
DCL-S W_TAX_AMT PACKED(9:2);
DCL-S W_FINAL_AMT PACKED(11:2);
DCL-S W_CUSTOMER_TYPE CHAR(1);
DCL-S W_PRIORITY CHAR(1);
DCL-S W_ROUTE CHAR(10);

// ============================================================
// 主程序
// ============================================================

SETLL *START ORDERS;
READ ORDERS;

DOW NOT %EOF(ORDERS);
  CHAIN ORDERS;

  // ─── 链路1: SALESPRICE → W_RAW_PRICE → W_DISCOUNT_AMT → W_NET_PRICE → W_FINAL_AMT → ORD_FINAL_AMT (FILE) ───
  W_RAW_PRICE = SALESPRICE;

  // 条件: 折扣计算
  IF DISCRATE > 0;
    W_DISCOUNT_AMT = W_RAW_PRICE * DISCRATE;
  ELSE;
    W_DISCOUNT_AMT = 0;
  ENDIF;

  W_NET_PRICE = W_RAW_PRICE - W_DISCOUNT_AMT;

  // 条件: VIP客户额外折扣
  IF CUSTTYPE = 'V';
    W_NET_PRICE = W_NET_PRICE * 0.95;
  ENDIF;

  // 计算税额
  W_TAX_RATE = 0.08;
  W_TAX_AMT = W_NET_PRICE * W_TAX_RATE;

  // 最终金额
  W_FINAL_AMT = W_NET_PRICE + W_TAX_AMT;

  // 写入文件
  ORD_FINAL_AMT = W_FINAL_AMT;
  UPDATE ORDERS;

  // ─── 链路2: CUSTTYPE → W_CUSTOMER_TYPE → W_PRIORITY → ITEMPRIO (FILE) ───
  W_CUSTOMER_TYPE = CUSTTYPE;

  IF W_CUSTOMER_TYPE = 'V';
    W_PRIORITY = 'H';
  ELSEIF W_CUSTOMER_TYPE = 'B';
    W_PRIORITY = 'M';
  ELSE;
    W_PRIORITY = 'N';
  ENDIF;

  ITEMPRIO = W_PRIORITY;
  UPDATE ITEMS;

  // ─── 链路3: W_PRIORITY → PRTCTL_DS.PRIORITY (DS) ───
  PRTCTL_DS.PRIORITY = W_PRIORITY;
  PRTCTL_DS.COPIES = 1;
  PRTCTL_DS.PRINT_DATE = %CHAR(%DATE(): *YMD);
  PRTCTL_DS.ROUTE_CODE = 'ROUTE01';

  READ ORDERS;
ENDDO;

OUT PRTCTL;

*INLR = *ON;
RETURN;
