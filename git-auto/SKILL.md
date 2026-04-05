---
name: git-auto
description: |
  Git 工作流自動化。AI 生成 commit message、changelog、README。
  當使用者說「幫我寫 commit」「更新 changelog」「產生 README」時觸發。
---

# Git Auto — Git 工作流自動化

## Commit Message 生成

讀取 `git diff --staged`，分析變動內容，產生符合格式的中文 commit message。

格式：`<type>: <描述>`

| type | 用途 |
|---|---|
| feat | 新功能 |
| fix | 修 bug |
| refactor | 重構（不改功能） |
| docs | 文件更新 |
| style | 格式調整（不影響邏輯） |
| test | 測試相關 |
| chore | 雜務（依賴更新、設定檔等） |

如果變動涉及多個面向，寫多行 body 說明。

## Changelog 生成

讀取 `git log` 產生面向使用者的 changelog：
- 只列對使用者有感的變動（跳過 chore、refactor）
- 用通俗的語言，不用技術術語
- 按日期分組

## README 生成

分析專案結構、`package.json`、現有文件，產生或更新 README：
- 專案名稱與簡介
- 安裝與啟動方式
- 環境變數說明
- 目錄結構
- 技術棧

---

## Compact Version

**功能**：讀 `git diff --staged` → 生成 commit message / changelog / README

**Commit 格式**：`<type>: <中文描述>`（feat/fix/refactor/docs/style/test/chore）
