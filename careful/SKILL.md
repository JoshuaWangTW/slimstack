---
name: careful
description: |
  安全把關模式。攔截危險指令並要求確認。
  當使用者說「小心」「be careful」或即將執行高風險操作時觸發。
  也可搭配其他 skill 同時載入（例如 review + careful）。
---

# Careful — 安全把關

啟用後，對以下指令類型發出警告並要求使用者明確確認：

## 攔截規則

### 🔴 高危（必須確認）
- `rm -rf` / `rm -r`（特別是指向 home 或根目錄）
- `DROP TABLE` / `DROP DATABASE` / `TRUNCATE`
- `git push --force` / `git reset --hard`
- `chmod 777`
- 任何涉及生產資料庫的 DELETE / UPDATE（不帶 WHERE 或 WHERE 條件太寬）
- `vercel --prod` 直接部署到生產

### 🟡 中危（提醒）
- `git checkout -b` 從 main 以外的分支建立新分支
- 大量檔案的批次操作
- 修改 `.env` 或設定檔
- 安裝未知的 npm 套件

## 行為

1. 偵測到危險指令時，**停下來**
2. 清楚說明這個指令會做什麼、影響範圍
3. 提供安全的替代方案（如果有）
4. 等使用者明確說「確認執行」才繼續

## 搭配使用

`careful` 設計為可與其他 skill 同時載入：
- `review` + `careful`：code review 時同時攔截危險操作
- `ship` + `careful`：部署時雙重把關
- `investigate` + `careful`：除錯時防止意外修改

---

## Compact Version

**角色**：安全攔截器。

**🔴攔截**：rm -rf / DROP TABLE / force-push / chmod 777 / 無 WHERE 的 DELETE

**行為**：停下 → 說明影響 → 給替代方案 → 等確認
