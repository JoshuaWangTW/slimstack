---
name: memory
description: |
  本地記憶系統。將決策紀錄、架構 memo、常用 pattern 存入本地筆記。
  當使用者說「記住這個」「記錄決策」「之前做過什麼」「查筆記」時觸發。
  純本地存放，不外傳任何資料。
---

# Memory — 本地記憶

你的工作是幫使用者把重要的決策和知識存入本地筆記系統，並在需要時取回。

## 設定

記憶檔案存放位置由使用者指定（例如 Obsidian vault、本地 docs 目錄等）。
首次使用時詢問存放路徑，之後記住。

預設路徑結構：
```
[筆記根目錄]/
└── slimstack-memory/
    ├── decisions/        ← 決策紀錄
    ├── architecture/     ← 架構 memo
    ├── patterns/         ← 可復用的解法
    ├── retro/            ← 回顧與教訓
    └── _index.md         ← 索引
```

使用者可依需求新增子目錄（例如依專案、依領域分類）。

## 寫入流程（Compact → Save）

每次寫入前必須先經過 compact，不要把對話原文直接存進筆記。

### Step 1：Compact（萃取精華）

從當前對話中提取結構化資訊，去除：
- 來回討論的過程（只保留結論）
- 重複提到的內容（合併為一條）
- 試錯過程（只保留最終方案）
- 客套語、確認語（「好」「了解」「可以」）

保留：
- 最終決策與理由
- 關鍵數據與參數
- 約束條件與限制
- 尚未解決的問題
- 具體的程式碼片段或指令（如果是 pattern 類型）

### Step 2：分類

根據內容判斷歸入哪個類別：
- `decisions/` — 有明確「選 A 不選 B」的判斷
- `architecture/` — 系統設計、schema、API 結構
- `patterns/` — 可復用的解法或工作流
- `retro/` — 回顧與教訓

### Step 3：格式化並寫入

用對應的模板格式化後寫入。寫入前向使用者展示摘要確認：

```
我整理了以下內容準備存入筆記：
📁 decisions/2026-04-05-supabase-vs-firebase.md
📝 摘要：選擇 Supabase 因為 RLS 原生支援、Realtime 訂閱、
   與 Vercel 整合成熟。Firebase 的 Firestore 查詢彈性不足。
   
要寫入嗎？
```

使用者確認後才寫入。

### Step 4：更新索引

寫入後自動更新 `_index.md`。

---

當使用者說「記住這個」或對話中產生了值得保留的決策時，執行上述流程：

### 決策紀錄格式
```markdown
---
type: decision
date: YYYY-MM-DD
project: [專案名稱]
tags: [相關標籤]
---

# [決策標題]

## 背景
[為什麼需要做這個決定]

## 選項
1. [選項 A] — 優點 / 缺點
2. [選項 B] — 優點 / 缺點

## 決定
[最終選擇 + 理由]

## 後續影響
[這個決定會影響什麼]
```

### 架構 Memo 格式
```markdown
---
type: architecture
date: YYYY-MM-DD
project: [專案名稱]
tags: [相關標籤]
---

# [系統/元件名稱]

## 概覽
[一段話描述]

## 組件
[列出主要組件與關係]

## 重要約束
[不能改動的部分與原因]
```

### Pattern 格式
```markdown
---
type: pattern
date: YYYY-MM-DD
tags: [相關標籤]
---

# [Pattern 名稱]

## 問題
[什麼情境下會用到]

## 解法
[具體做法，附程式碼範例]

## 注意事項
[陷阱或限制]
```

## 讀取（Recall）

當使用者問「之前怎麼決定的」「有沒有做過類似的」時：
1. 讀取 `_index.md`
2. 根據關鍵字搜尋相關檔案
3. 讀取對應的 memo
4. 整理摘要回覆

## 索引維護

每次寫入新檔案時，更新 `_index.md`：
```markdown
# SlimStack Memory Index

## 最近紀錄
| 日期 | 類型 | 標題 | 檔案 |
|---|---|---|---|
| 2026-04-05 | decision | 選用 Supabase 而非 Firebase | decisions/2026-04-05-supabase.md |
| ... | ... | ... | ... |
```

## 隱私保證

- 所有檔案只存在本地
- 不生成任何 ID
- 不連線任何外部服務
- 不寫入任何隱藏的 analytics 檔案

## 交接

- 記錄回顧結果 ← 來自 `retro`
- 記錄架構決策 ← 來自 `plan-eng`
- 記錄策略決定 ← 來自 `office-hours` / `plan-ceo`

---

## Compact Version

**流程**：Compact（萃取精華去雜訊）→ 分類（decisions/architecture/patterns/retro）→ 確認 → 寫入本地筆記

**規則**：寫入前必須 compact / 寫入前必須確認 / 純本地零外傳
