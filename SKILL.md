---
name: slimstack
description: |
  開發工作流路由器。當使用者提到以下任何情境時觸發：
  策略討論、需求釐清、架構設計、code review、部署推送、
  commit 訊息、品牌稽核、趨勢掃描、影片製作、回顧覆盤、
  深度研究、任務分解、除錯、安全把關、信心度檢查、記憶紀錄。
  觸發後讀取對應子目錄的 SKILL.md 並依指令執行。
  即使使用者沒有明確使用 slash command，只要意圖吻合也應主動路由。
---

# SlimStack Router

你是 模組化開發工作流系統。根據使用者意圖，載入對應 skill 執行。

## SKILL0 漸進式撤除機制

參考 SKILL0 論文（arxiv:2604.02268），每個 skill 有三個載入層級：

| 層級 | 條件 | 載入內容 | Token 量 |
|---|---|---|---|
| **Full** | 使用 < 5 次 | 完整 SKILL.md | ~800-1500 |
| **Compact** | 使用 5-14 次，且近 3 次無修正 | 只讀 `## Compact Version` 區塊 | ~200-400 |
| **Zero** | 使用 ≥ 15 次，且近 5 次無修正 | 不載入檔案，僅用路由表的一句話描述 | ~50 |

### 判斷流程

1. 讀取 `~/.slimstack/usage.json`；目錄或檔案不存在時，建立並初始化為 `{}`
2. 查詢目標 skill 的使用次數與修正紀錄
3. 根據上表決定載入層級
4. 如果使用者明確說「用完整版」或任務特別複雜，**強制 Full**

### 使用紀錄更新

每次 skill 執行完成後，更新 `~/.slimstack/usage.json`：
```json
{
  "review": { "count": 12, "last_correction": 8 },
  "ship": { "count": 7, "last_correction": null },
  "careful": { "count": 20, "last_correction": 3 }
}
```
- `count`：累計使用次數
- `last_correction`：最後一次使用者要求修正的使用次數（null = 從未修正）

如果 `count - last_correction < 3`（近期有修正），**回升到 Full**，重新學習。

### SKILL0 狀態診斷指令

使用者說「SKILL0 狀態」時，讀取 usage.json，輸出各 skill 的表格：skill 名 / count / 目前層級（依上表推算）/ last_correction。檔案不存在則回報「尚無使用紀錄」。

### 幫助度回升（Helpfulness Rebound）

「修正」指以下任一情況：
- 使用者明確指出 skill 產出有錯或不符預期
- 使用者要求同一 skill 重做或改寫產出
- 使用者推翻 skill 產出的關鍵結論

單純追問、補充需求、風格微調**不算**修正。

如果使用者在 Compact 或 Zero 層級下的輸出被修正：
- 該 skill 立即回升到 Full
- `last_correction` 更新為當前 count
- 重新累積穩定次數

這確保「內化」是真正的內化，不是假性降級。

## 路由規則

一次最多載入 **2 個 skill**。完成後釋放。

| 意圖 | 載入 |
|---|---|
| 策略方向、挑戰假設、釐清問題 | `office-hours/SKILL.md` |
| CEO 視角、產品 review、市場契合 | `plan-ceo/SKILL.md` |
| 需求模糊、要先訪談再動手 | `deep-interview/SKILL.md` |
| 系統架構、技術決策、DB schema | `plan-eng/SKILL.md` |
| 大任務拆解、Epic → Story → Task | `task-decompose/SKILL.md` |
| 寫程式碼、實作功能、TDD | `implement/SKILL.md` |
| Code review、找生產炸彈 | `review/SKILL.md` |
| 推送、PR、部署前檢查 | `ship/SKILL.md` |
| Commit message、changelog、README | `git-auto/SKILL.md` |
| 危險操作、rm -rf、DROP TABLE | `careful/SKILL.md` |
| Bug 除錯、根因分析 | `investigate/SKILL.md` |
| 執行前確認、信心度評估 | `confidence-check/SKILL.md` |
| 品牌稽核、視覺一致性 | `brand-review/SKILL.md` |
| 深度研究、市場調查、技術探索 | `research/SKILL.md` |
| Threads/IG 趨勢、話題掃描 | `social-intel/SKILL.md` |
| 文件產出、技術文件、release notes | `document/SKILL.md` |
| 影片製作、Remotion、腳本 | `video-produce/SKILL.md` |
| 週回顧、Sprint 覆盤 | `retro/SKILL.md` |
| 記住決策、架構 memo、筆記 | `memory/SKILL.md` |

## 常見組合

以下情境可同時載入 2 個 skill：
- `review` + `careful`：高風險 code review
- `ship` + `careful`：部署前雙重把關
- `implement` + `confidence-check`：實作前先確認信心度
- `investigate` + `careful`：除錯時鎖定編輯範圍

## 工作流指南

完整的角色接力流程請讀取 `references/workflow.md`。

## Token 管理

你是唯一常駐 context 的檔案。所有子 skill 的 SKILL.md 僅在被路由時載入，完成後不再佔用 context。搭配 SKILL0 漸進式撤除，隨著使用次數增加，token 佔用會自動從 ~1500 降至 ~50。
