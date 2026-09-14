# Program Analysis: FIELDCHAIN

## 1. Overview

| Item | Value |
|------|-------|
| Program Name | FIELDCHAIN |
| Type | RPGLE |
| Entry Point | MAIN (line 2) |
| Files Used | 2 (ORDERS, ITEMS) |
| Data Areas | 1 (PRTCTL) |
| Program Calls | 0 |
| External References | /COPY QRPGLESRC,INITSRV |

---

## 2. Program Flow

```mermaid
flowchart TD
    Entry[PROGRAM ENTRY - line 2] --> Init[INITIALIZE / COPY INITSRV]
    Init --> Decl[DECLARE FILES & DATA AREA]
    
    Decl --> Loop{DOW NOT %EOF ORDERS}
    Loop -->|Not EOF| Chain[CHAIN ORDERS - Read Record]
    Loop -->|EOF| Exit[PROGRAM EXIT - *INLR = *ON]
    
    Chain --> PriceCalc[PRICE CALCULATION]
    Chain --> CustType[CUSTOMER TYPE PROCESSING]
    Chain --> PrintCtrl[PRINT CONTROL]
    
    PriceCalc --> Update1[UPDATE ORDERS - line 71]
    CustType --> Update2[UPDATE ORDERS - line 85]
    
    Update1 --> WriteDA[OUT PRTCTL - line 97]
    Update2 --> WriteDA
    
    WriteDA --> ReadNext[READ ORDERS - Next Record]
    ReadNext --> Loop
```

---

## 3. Field Propagation Chains

### 3.1 Price Calculation Chain

```mermaid
flowchart LR
    A[SALESPRICE<br/>DB Field] --> B[W_RAW_PRICE<br/>line 47]
    
    B --> C{DISCRATE > 0?}
    C -->|Yes| D[W_DISCOUNT_AMT<br/>= W_RAW_PRICE * DISCRATE<br/>line 51]
    C -->|No| E[W_DISCOUNT_AMT<br/>= 0<br/>line 53]
    
    D --> F[W_NET_PRICE<br/>= W_RAW_PRICE - W_DISCOUNT_AMT<br/>line 56]
    E --> F
    
    F --> G{CUSTTYPE = 'V'?}
    G -->|Yes VIP| H[W_NET_PRICE<br/>*= 0.95<br/>line 60]
    G -->|No| I[W_NET_PRICE<br/>unchanged]
    
    H --> J[W_TAX_AMT<br/>= W_NET_PRICE * 0.08<br/>line 65]
    I --> J
    
    J --> K[W_FINAL_AMT<br/>= W_NET_PRICE + W_TAX_AMT<br/>line 68]
    K --> L[ORD_FINAL_AMT<br/>= W_FINAL_AMT<br/>line 71]
    
    L --> M[WRITE TO ORDERS]
```

### 3.2 Customer Priority Chain

```mermaid
flowchart LR
    A[CUSTTYPE<br/>DB Field] --> B[W_CUSTOMER_TYPE<br/>= CUSTTYPE<br/>line 75]
    
    B --> C{W_CUSTOMER_TYPE?}
    C -->|'= V' VIP| D[W_PRIORITY = 'H'<br/>line 78]
    C -->|'= B' Business| E[W_PRIORITY = 'M'<br/>line 80]
    C -->|Other| F[W_PRIORITY = 'N'<br/>line 82]
    
    D --> G[ITEMPRIO<br/>= W_PRIORITY<br/>line 85]
    E --> G
    F --> G
    
    G --> H[WRITE TO ORDERS]
```

### 3.3 Print Control Chain

```mermaid
flowchart LR
    A[W_PRIORITY] --> B[PRTCTL_DS.PRIORITY<br/>line 89]
    
    C[Constant 1] --> D[PRTCTL_DS.COPIES<br/>line 89]
    
    E[%DATE : *YMD] --> F[PRTCTL_DS.PRINT_DATE<br/>line 91]
    
    G[Constant 'ROUTE01'] --> H[PRTCTL_DS.ROUTE_CODE<br/>line 89]
    
    B --> I[OUT PRTCTL<br/>line 97]
    D --> I
    F --> I
    H --> I
    
    I --> J[WRITE TO DATA AREA]
```

---

## 4. Data Area Structure

**PRTCTL** (100 bytes, CHAR)

| Offset | Field | Source | Value | Line |
|--------|-------|--------|-------|------|
| 0 | PRINT_DATE | %CHAR(%DATE(): *YMD) | Current date (YMD) | 91 |
| 8 | PRINT_TIME | - | - | - |
| 14 | COPIES | Constant | 1 | 89 |
| 17 | PRIORITY | W_PRIORITY | H/M/N | 89 |
| 18 | ROUTE_CODE | Constant | 'ROUTE01' | 89 |

---

## 5. Business Logic

| Rule | Condition | Action | Line |
|------|-----------|--------|------|
| Discount calculation | DISCRATE > 0 | W_DISCOUNT_AMT = W_RAW_PRICE * DISCRATE | 51 |
| No discount | DISCRATE = 0 | W_DISCOUNT_AMT = 0 | 53 |
| VIP discount | CUSTTYPE = 'V' | W_NET_PRICE *= 0.95 | 60 |
| Tax rate | Always | W_TAX_RATE = 0.08 | 64 |
| VIP priority | W_CUSTOMER_TYPE = 'V' | W_PRIORITY = 'H' | 78 |
| Business priority | W_CUSTOMER_TYPE = 'B' | W_PRIORITY = 'M' | 80 |
| Normal priority | Other | W_PRIORITY = 'N' | 82 |

---

## 6. Table Operations

**ORDERS** (INPUT/OUTPUT)

| Field | Operation | Expression | Written | Line |
|-------|-----------|------------|---------|------|
| W_RAW_PRICE | ASSIGN | SALESPRICE | ✅ | 47 |
| W_DISCOUNT_AMT | ASSIGN | W_RAW_PRICE * DISCRATE | ✅ | 51 |
| W_DISCOUNT_AMT | ASSIGN | 0 | ✅ | 53 |
| W_NET_PRICE | ASSIGN | W_RAW_PRICE - W_DISCOUNT_AMT | ✅ | 56 |
| W_NET_PRICE | ASSIGN | W_NET_PRICE * 0.95 | ✅ | 60 |
| W_TAX_RATE | ASSIGN | 0.08 | ✅ | 64 |
| W_TAX_AMT | ASSIGN | W_NET_PRICE * W_TAX_RATE | ✅ | 65 |
| W_FINAL_AMT | ASSIGN | W_NET_PRICE + W_TAX_AMT | ✅ | 68 |
| ORD_FINAL_AMT | ASSIGN | W_FINAL_AMT | ✅ | 71 |
| W_CUSTOMER_TYPE | ASSIGN | CUSTTYPE | ✅ | 75 |
| W_PRIORITY | ASSIGN | 'H' / 'M' / 'N' | ✅ | 78-82 |
| ITEMPRIO | ASSIGN | W_PRIORITY | ✅ | 85 |

---

## 7. Migration Notes

### Key Fields for Java Migration

| RPG Field | Java Equivalent | Type | Description |
|-----------|-----------------|------|-------------|
| SALESPRICE | order.salesPrice | BigDecimal | Source price from DB |
| DISCRATE | order.discRate | BigDecimal | Discount rate |
| CUSTTYPE | customer.type | String | Customer type (V/B/other) |
| ORD_FINAL_AMT | order.finalAmount | BigDecimal | Final calculated amount |
| ITEMPRIO | order.itemPriority | String | Priority level (H/M/N) |

### Business Rules to Preserve

1. Discount only applies when DISCRATE > 0
2. VIP customers get additional 5% discount
3. Tax rate is fixed at 8%
4. Priority mapping: V→H, B→M, others→N
5. PRTCTL Data Area stores print control info

### Calculation Formula

```
finalAmount = salesPrice 
              - (salesPrice * discRate if discRate > 0 else 0)
              * (0.95 if custType = 'V' else 1.0)
              * 1.08
```
