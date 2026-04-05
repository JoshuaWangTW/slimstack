---
name: ship
description: |
  推送與部署。處理 git commit、push、PR 建立、部署前檢查。
  當使用者說「推上去」「開 PR」「部署」「ship it」時觸發。
---

# Ship — 推送與部署

你的工作是確保程式碼安全地從本地到達生產環境。

## 部署前檢查清單

1. **程式碼狀態**
   - `git status` 確認沒有意外的 unstaged 檔案
   - `git diff --staged` review 即將 commit 的內容
   - 確認不會把 .env、密鑰、或測試資料 commit 進去

2. **測試**
   - 跑一次完整測試
   - 確認沒有 skip 的測試
   - 確認沒有 console.log 殘留

3. **Build**
   - `npm run build` / `next build` 確認 build 成功
   - 檢查 build warning（特別是 TypeScript 錯誤）

4. **環境變數**
   - 新增的環境變數有沒有在 Vercel Dashboard 設定？
   - 有沒有用到 `NEXT_PUBLIC_` 前綴的敏感值？

## 部署流程

```
git add .
git commit -m "[commit message]"
git push origin [branch]
```

如果需要開 PR：提供 PR 標題和描述的建議。

## Git Commit Message 格式

使用中文描述：
- `feat: 新增使用者登入功能`
- `fix: 修正價格計算溢位問題`
- `refactor: 重構 API 路由結構`
- `docs: 更新 README 部署說明`

## 交接

- 部署出問題 → `investigate`
- 部署後要寫 release notes → `document`

---

## Compact Version

**角色**：部署把關。

**檢查**：git status → test → build → 環境變數

**Commit 格式**：`feat/fix/refactor/docs: 中文描述`

**交接**：出問題→`investigate` | release notes→`document`
