# SlimStack 工作流指南

## Skill 協作流程

### 新專案啟動
```
deep-interview → plan-eng → task-decompose → implement → review → ship
（釐清需求）   （架構設計）（拆解任務）   （實作）   （審查）（部署）
```

### 日常開發
```
implement → review → ship
（實作）   （審查）（推送）
```

### 高風險操作
```
confidence-check + careful → [操作] → review
（評估信心度 + 安全把關）         （事後審查）
```

### 除錯
```
investigate → implement → review → ship
（找根因）   （修正）   （確認）（推送）
```

### 策略規劃
```
office-hours → plan-ceo → research → deep-interview → plan-eng
（釐清方向）  （產品視角）（深度研究）（細化需求）   （技術規劃）
```

### 內容行銷
```
social-intel → video-produce → brand-review → careful
（掃描趨勢）  （製作內容）   （品牌稽核）  （發布前確認）
```

### 週回顧
```
retro → memory → office-hours
（覆盤）（記錄）  （規劃下週）
```

## Skill 組合建議

| 情境 | 主 Skill | 搭配 Skill |
|---|---|---|
| 碰到 production bug | `investigate` | `careful` |
| 部署到生產環境 | `ship` | `careful` |
| 第一次做某個系統 | `implement` | `confidence-check` |
| Review 涉及資料庫操作 | `review` | `careful` |

## 角色互相稽核

| 規劃 Skill | 建議搭配的 Review |
|---|---|
| `plan-eng` | `review`（技術審查） |
| `plan-ceo` | `office-hours`（挑戰假設） |
| 任何對外內容 | `brand-review` + `careful` |

## Token 管理提醒

- Router 常駐佔用 ~150 tokens
- 一次最多載入 2 個 skill
- skill 完成任務後自動釋放
- 如果 context 太長，優先釋放 skill 再繼續

---

*最後更新：2026-04-05*
