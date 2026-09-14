# Program Analysis: ORDPROC

## 1. Overview

| Item | Value |
|------|-------|
| Program Name | ORDPROC |
| Type | RPGLE |
| Entry Points | MAIN (line 2) |
| Files | 5 (ORDERH, ORDERD, CUSTMAST, PRODMAST, ORDLOG) |
| Data Areas | 1 (ORDCTL) |
| Program Calls | 2 (ORDNOTI, SENDMAIL) |
| COPY/INCLUDE | 2 (QRPGLESRC/INITSRV, QPROTOSRC/UTIL_H) |

---

## 2. Program Flow

```mermaid
flowchart TD
    Entry[ENTRY - line 2] --> Init[COPY INITSRV, UTIL_H]
    Init --> Decl[Declare Files & Data Area]
    Decl --> ReadH[SETLL *START ORDERH - line 40]
    ReadH --> ReadH2[READ ORDERH - line 41]
    ReadH2 --> InDa[IN ORDCTL - line 44]
    InDa --> InitDa[Initialize Data Area]
    InitDa --> Loop{DOW NOT %EOF ORDERD - line 49}
    
    Loop -->|Not EOF| ChainD[CHAIN ORDERD - line 50]
    ChainD --> ChkCancel{DTLSTS = 'C'?}
    ChkCancel -->|Yes Cancel| Skip[READ ORDERD - line 54]
    ChkCancel -->|No| ChkProd[CHAIN PRODCD PRODMAST - line 59]
    
    ChkProd --> ChkFound{%FOUND?}
    ChkFound -->|No| ErrFlag[ERROR_FLAG = 'Y' - line 61]
    ChkFound -->|Yes| Calc[Calculate Amounts]
    
    Calc --> WTotal[W_TOTAL = PRICE * QTY - line 67]
    WTotal --> WTax[W_TAX = W_TOTAL * 0.08 - line 70]
    WTax --> UpdD[Update ORDERD - line 76]
    
    UpdD --> ChkCust[CHAIN CUSTCD CUSTMAST - line 79]
    ChkCust --> ChkCustFound{%FOUND?}
    ChkCustFound -->|No| Unk[CUSTNAME = '*UNKNOWN' - line 81]
    ChkCustFound -->|Yes| UpdCust[Update CUSTTOTAL - line 85]
    Unk --> UpdCust
    
    UpdCust --> IncCnt[Increment Counter - line 89]
    IncCnt --> ReadNext[READ ORDERD - line 93]
    ReadNext --> Loop
    ErrFlag --> ReadNext
    Skip --> Loop
    
    Loop -->|EOF| ChkErr{ERROR_FLAG = 'N'?}
    ChkErr -->|Yes| SetC[ORDSTS = 'C' - line 98]
    ChkErr -->|No| SetE[ORDSTS = 'E' - line 100]
    
    SetC --> UpdH[UPDATE ORDERH - line 102]
    SetE --> UpdH
    
    UpdH --> WriteLog[Write ORDLOG - line 109]
    WriteLog --> OutDa[OUT ORDCTL - line 112]
    OutDa --> CallProg[Call Programs]
    
    CallProg --> Call1[CALL 'ORDNOTI' - line 115]
    Call1 --> Call2[CALLP SENDMAIL - line 116]
    Call2 --> Sql[EXEC SQL UPDATE - line 119]
    Sql --> Exit[*INLR = *ON - line 126]
```

---

## 3. Data Flow

### 3.1 Amount Calculation Chain

```mermaid
flowchart LR
    A[PRICE<br/>DB Field] -->|line 67| B[W_TOTAL<br/>= PRICE * QTY]
    C[QTY<br/>DB Field] -->|line 67| B
    
    B -->|line 70| D[W_TAX<br/>= W_TOTAL * 0.08]
    
    B -->|line 73| E[ORDAMT<br/>= W_TOTAL]
    D -->|line 74| F[ORDTAX<br/>= W_TAX]
    
    B -->|line 85| G[CUSTTOTAL<br/>+= W_TOTAL]
```

### 3.2 Status Control Chain

```mermaid
flowchart LR
    A[ORDCTL_DS.ERROR_FLAG] -->|line 97| B{ERROR_FLAG = 'N'?}
    B -->|Yes| C[ORDSTS = 'C'<br/>Complete]
    B -->|No| D[ORDSTS = 'E'<br/>Error]
    
    C -->|line 102| E[UPDATE ORDERH]
    D -->|line 102| E
    
    E -->|line 106| F[LOGSTS = ORDSTS]
```

### 3.3 Data Area Flow

```mermaid
flowchart LR
    A[IN ORDCTL<br/>line 44] --> B[ORDCTL_DS]
    
    B --> C[COUNTER = 0<br/>line 45]
    B --> D[ERROR_FLAG = 'N'<br/>line 46]
    
    E[Loop Processing] --> F[COUNTER += 1<br/>line 89]
    E --> G[ERROR_FLAG = 'Y'<br/>line 61]
    E --> H[CUSTOMER_CODE = CUSTCD<br/>line 90]
    E --> I[ORDER_DATE = ORDDT<br/>line 91]
    
    F --> J[OUT ORDCTL<br/>line 112]
    G --> J
    H --> J
    I --> J
```

---

## 4. Business Logic

### 4.1 Calculations

| Formula | Expression | Line | Condition |
|---------|------------|------|-----------|
| Total Amount | PRICE * QTY | 67 | Always |
| Tax Amount | W_TOTAL * 0.08 | 70 | Always |
| Customer Total | CUSTTOTAL + W_TOTAL | 85 | Always |

### 4.2 Business Rules

| Rule | Condition | Action | Line |
|------|-----------|--------|------|
| Skip cancelled | DTLSTS = 'C' | Skip to next record | 53-56 |
| Product not found | NOT %FOUND | Set error flag, skip | 60-64 |
| Customer not found | NOT %FOUND | Set name to '*UNKNOWN' | 80-82 |
| Order complete | ERROR_FLAG = 'N' | Set status 'C' | 98 |
| Order error | ERROR_FLAG = 'Y' | Set status 'E' | 100 |

### 4.3 Constants

| Constant | Value | Usage | Line |
|----------|-------|-------|------|
| Tax Rate | 0.08 | 8% tax rate | 70 |
| Processing Status | 'P' | Order detail processing | 75 |
| Complete Status | 'C' | Order completed | 98 |
| Error Status | 'E' | Order has errors | 100 |
| Cancelled Status | 'C' | Detail cancelled | 53 |
| Unknown Customer | '*UNKNOWN' | Default name | 81 |

---

## 5. Data Dictionary

| Field | Type | Source | Business Meaning | Line |
|-------|------|--------|------------------|------|
| ORDNO | CHAR(10) | DB | Order number | 105 |
| ORDDT | CHAR(8) | DB | Order date | 91 |
| ORDSTS | CHAR(1) | DB | Order status (C/E/P) | 75/98/100 |
| CUSTCD | CHAR(5) | DB | Customer code | 79/90 |
| CUSTNAME | CHAR(30) | DB | Customer name | 81 |
| CUSTTOTAL | PACKED(11:2) | DB | Customer cumulative total | 85 |
| PRODCD | CHAR(10) | DB | Product code | 59 |
| PRICE | PACKED(11:2) | DB | Unit price | 67 |
| QTY | PACKED(5:0) | DB | Quantity | 67 |
| DTLSTS | CHAR(1) | DB | Detail status (C=Cancelled) | 53 |
| ORDAMT | PACKED(11:2) | DB | Order amount (written) | 73 |
| ORDTAX | PACKED(9:2) | DB | Order tax (written) | 74 |
| W_TOTAL | PACKED(11:2) | Work | Calculated total | 67 |
| W_TAX | PACKED(9:2) | Work | Calculated tax | 70 |
| W_COUNT | INT(5) | Work | Counter | 32 |
| W_STATUS | CHAR(1) | Work | Status code | 33 |

---

## 6. Table Operations

### ORDERH (INPUT)

| Field | Operation | Expression | Condition | Written | Line |
|-------|-----------|------------|-----------|---------|------|
| LOGORD | ASSIGN | ORDNO | Always | Y | 105 |
| LOGSTS | ASSIGN | ORDSTS | Always | Y | 106 |
| LOGCNT | ASSIGN | ORDCTL_DS.COUNTER | Always | Y | 107 |
| LOGTIME | ASSIGN | %TIMESTAMP() | Always | Y | 108 |

### ORDERD (INPUT/OUTPUT)

| Field | Operation | Expression | Condition | Written | Line |
|-------|-----------|------------|-----------|---------|------|
| W_TOTAL | ASSIGN | PRICE * QTY | Always | Y | 67 |
| W_TAX | ASSIGN | W_TOTAL * 0.08 | Always | Y | 70 |
| ORDAMT | ASSIGN | W_TOTAL | Always | Y | 73 |
| ORDTAX | ASSIGN | W_TAX | Always | Y | 74 |
| ORDSTS | ASSIGN | 'P' | Always | Y | 75 |

### CUSTMAST (INPUT)

| Field | Operation | Expression | Condition | Written | Line |
|-------|-----------|------------|-----------|---------|------|
| CUSTNAME | ASSIGN | '*UNKNOWN' | NOT %FOUND | Y | 81 |
| CUSTTOTAL | ASSIGN | CUSTTOTAL + W_TOTAL | Always | Y | 85 |

### ORDLOG (OUTPUT)

| Field | Operation | Expression | Condition | Written | Line |
|-------|-----------|------------|-----------|---------|------|
| LOGORD | ASSIGN | ORDNO | Always | Y | 105 |
| LOGSTS | ASSIGN | ORDSTS | Always | Y | 106 |
| LOGCNT | ASSIGN | ORDCTL_DS.COUNTER | Always | Y | 107 |
| LOGTIME | ASSIGN | %TIMESTAMP() | Always | Y | 108 |

---

## 7. Data Area: ORDCTL

| Field | Offset | Source | Value | Line |
|-------|--------|--------|-------|------|
| STATUS | 0 | - | - | - |
| COUNTER | 1 | Increment | 0 → N | 45/89 |
| ORDER_DATE | 6 | ORDDT | Order date | 91 |
| CUSTOMER_CODE | 14 | CUSTCD | Customer code | 90 |
| ERROR_FLAG | 19 | Flag | N/Y | 46/61 |

---

## 8. Error Handling

| Condition | Handling | Line |
|-----------|----------|------|
| EOF on ORDERD | Exit loop | 49 |
| Detail cancelled (DTLSTS='C') | Skip to next | 53-56 |
| Product not found | Set ERROR_FLAG='Y', skip | 60-64 |
| Customer not found | Set CUSTNAME='*UNKNOWN' | 80-82 |
| Any error occurred | Set ORDSTS='E' | 100 |

---

## 9. Program Calls

| Program | Type | Line | Purpose |
|---------|------|------|---------|
| ORDNOTI | CALL | 115 | Order notification |
| SENDMAIL | CALLP | 116 | Send email notification |

---

## 10. Migration Notes

### Field Mapping

| RPG Field | Java Field | Type | Notes |
|-----------|------------|------|-------|
| ORDNO | order.orderNo | String | Order number |
| ORDDT | order.orderDate | String | Order date |
| ORDSTS | order.status | String | C=Complete, E=Error |
| CUSTCD | customer.code | String | Customer code |
| CUSTNAME | customer.name | String | Customer name |
| CUSTTOTAL | customer.totalAmount | BigDecimal | Cumulative total |
| PRODCD | product.code | String | Product code |
| PRICE | product.price | BigDecimal | Unit price |
| QTY | orderDetail.quantity | int | Quantity |
| ORDAMT | orderDetail.amount | BigDecimal | Line amount |
| ORDTAX | orderDetail.tax | BigDecimal | Line tax |

### Business Rules to Preserve

1. Skip cancelled details (status = 'C')
2. Set error flag if product not found
3. Set customer name to '*UNKNOWN' if not found
4. Tax rate is fixed at 8%
5. Update customer cumulative total
6. Write audit log for each order
7. Call notification programs after processing
8. Update ORDERH status via SQL

### Calculation Formulas

```
lineAmount = unitPrice * quantity
lineTax = lineAmount * 0.08
customerTotal += lineAmount
orderStatus = (hasError) ? 'E' : 'C'
```

### Edge Cases

- Product not found: Error flag set, order continues
- Customer not found: Name set to '*UNKNOWN', amount still accumulated
- Cancelled detail: Skipped entirely
- Multiple errors: ERROR_FLAG stays 'Y' once set
- SQL update after RPG update: Potential race condition

### External Dependencies

- ORDNOTI: Order notification program (must exist)
- SENDMAIL: Email sending procedure (must exist)
- QRPGLESRC/INITSRV: Initialization routine
- QPROTOSRC/UTIL_H: Utility functions
