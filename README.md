# SlimStack

模組化 AI 開發工作流技能系統 — 19 個可組合的 skill，支援意圖路由與漸進式撤除（SKILL0）。

Modular AI skill system for dev workflows — 19 composable skills with intent-based routing and progressive offloading (SKILL0).

---

## 目錄 / Table of Contents

- [簡介 / Introduction](#簡介--introduction)
- [運作原理 / How It Works](#運作原理--how-it-works)
- [安裝 / Installation](#安裝--installation)
- [快速上手 / Quick Start](#快速上手--quick-start)
- [技能總覽 / Skills Reference](#技能總覽--skills-reference)
- [使用指南 / Usage Guide](#使用指南--usage-guide)
  - [策略與規劃 / Strategy & Planning](#1-策略與規劃--strategy--planning)
  - [開發 / Development](#2-開發--development)
  - [維運與安全 / Operations & Safety](#3-維運與安全--operations--safety)
  - [內容與行銷 / Content & Marketing](#4-內容與行銷--content--marketing)
  - [知識管理 / Knowledge Management](#5-知識管理--knowledge-management)
- [工作流管線 / Workflow Pipelines](#工作流管線--workflow-pipelines)
- [技能組合 / Skill Combinations](#技能組合--skill-combinations)
- [漸進式撤除 SKILL0 / Progressive Offloading](#漸進式撤除-skill0--progressive-offloading)
- [自訂 / Customization](#自訂--customization)
- [專案結構 / Project Structure](#專案結構--project-structure)
- [常見問題 / FAQ](#常見問題--faq)

---

## 簡介 / Introduction

SlimStack 是一套由 19 個可組合「技能」組成的系統，讓 AI 助手成為結構化的開發夥伴。每個技能是一個專注的 SKILL.md 檔案，定義了特定角色、工作流程和輸出格式。中央路由器根據使用者意圖按需載入技能，保持最小的 context 佔用。

SlimStack is a collection of 19 composable "skills" that turn an AI assistant into a structured development partner. Each skill is a focused SKILL.md file that defines a specific role, workflow, and output format. A central router loads skills on demand based on user intent, keeping context usage minimal.

### 核心特性 / Key Features

- **意圖路由 / Intent-based routing** — 路由器自動偵測你要做什麼，載入對應技能 / The router detects what you're trying to do and loads the right skill(s) automatically
- **漸進式撤除 SKILL0 / Progressive offloading** — 技能從完整版開始，隨使用次數自動精簡。基於 [SKILL0 論文](https://arxiv.org/abs/2604.02268) / Skills start at full detail, then compact to minimal prompts as the AI internalizes patterns
- **可組合 / Composable** — 同時載入最多 2 個技能（例如 `review` + `careful` 進行高風險 code review）/ Load up to 2 skills simultaneously for combined workflows
- **省 Token / Token-efficient** — 只有路由器常駐 context；技能按需載入，完成後釋放 / Only the router stays in context; skills load on demand and release after use

---

## 運作原理 / How It Works

```
┌──────────────────────────────────────────────────────────┐
│  你：「Review 一下這段 code，等等要推到 prod」               │
│  You: "Review this code before I push to prod"           │
│                        ↓                                 │
│  路由器偵測：code review + 部署意圖                         │
│  Router detects: code review + deployment intent         │
│                        ↓                                 │
│  載入：review/SKILL.md + ship/SKILL.md                    │
│  Loads: review/SKILL.md + ship/SKILL.md                  │
│                        ↓                                 │
│  AI 角色：偏執的資深工程師 + 部署把關員                       │
│  AI acts as: paranoid senior engineer + deploy gatekeeper │
│                        ↓                                 │
│  產出：結構化 review → 部署檢查清單                          │
│  Output: structured review → deploy checklist            │
│                        ↓                                 │
│  技能卸載，context 釋放                                    │
│  Skills unloaded, context freed                          │
└──────────────────────────────────────────────────────────┘
```

路由器（根目錄 `SKILL.md`）是唯一常駐 context 的檔案（約 150 tokens）。19 個子技能按需載入，完成後釋放。

The router (`SKILL.md` at root) is the only file that stays in context permanently (~150 tokens). All 19 sub-skills load on demand and release after use.

---

## 安裝 / Installation

### Claude Code

**步驟 1：Clone repo / Step 1: Clone**

```bash
git clone https://github.com/JoshuaWangTW/slimstack.git ~/.claude/skills/slimstack
```

**步驟 2：加入專案的 CLAUDE.md / Step 2: Add to your project's CLAUDE.md**

```markdown
## Skills

SlimStack skills are installed at ~/.claude/skills/slimstack/

When the user's intent matches a skill, read the root SKILL.md for routing,
then load the corresponding sub-skill's SKILL.md and follow its instructions.

Routing examples:
- Architecture discussion → load plan-eng/SKILL.md
- "Review this code" → load review/SKILL.md
- "Ship it" → load ship/SKILL.md
- Vague requirements → load deep-interview/SKILL.md
```

**步驟 3（選用）：建立 slash commands / Step 3 (Optional): Create slash commands**

```bash
mkdir -p .claude/commands

# /review 指令
echo 'Load ~/.claude/skills/slimstack/review/SKILL.md and review the current changes.' > .claude/commands/review.md

# /plan 指令
echo 'Load ~/.claude/skills/slimstack/plan-eng/SKILL.md and design the system architecture for: $ARGUMENTS' > .claude/commands/plan.md

# /retro 指令
echo 'Load ~/.claude/skills/slimstack/retro/SKILL.md and run a retrospective.' > .claude/commands/retro.md
```

使用方式 / Usage:
```
> /review
> /plan a user authentication system with OAuth
> /retro
```

### Claude Projects (claude.ai)

1. 建立新 Project / Create a new Project
2. 在 Project Instructions 貼入根目錄 `SKILL.md` 內容 / Paste the root `SKILL.md` content into Project Instructions
3. 將常用子技能的 SKILL.md 上傳到 Project Knowledge / Upload frequently used sub-skill files to Project Knowledge
4. AI 會根據你的訊息自動路由到正確的技能 / The AI will route to the correct skill based on your messages

### 其他 AI 工具 / Other AI assistants (ChatGPT, Cursor, etc.)

將根目錄 `SKILL.md` 複製到你的 system prompt 中。觸發技能時，貼入對應子技能的內容。每個子技能都是獨立的，可以單獨使用。

Copy the root `SKILL.md` into your system prompt. When a skill is triggered, paste the corresponding sub-skill's content. Each sub-skill is self-contained and works independently.

---

## 快速上手 / Quick Start

安裝後直接用自然語言對話，路由器會自動處理：

After installation, just talk naturally. The router handles the rest:

```
你：我想做一個書籤管理 app，但細節還沒想清楚。
You: I want to build a bookmark manager app, but I haven't figured out the details yet.

AI → 路由到 deep-interview（偵測到需求模糊）
AI → Routes to deep-interview (detects vague requirements)
   → 結構化提問：為什麼？給誰用？核心流程是什麼？
   → Asks structured questions: Why? For whom? What's the core flow?
   → 完成後產出需求規格書
   → Produces a requirements spec when done
   → 建議：「需求確認了，要載入 plan-eng 做架構設計嗎？」
   → Suggests: "Requirements confirmed. Load plan-eng for architecture?"
```

```
你：設計這個系統的資料庫 schema。
You: Design the database schema for this.

AI → 路由到 plan-eng（偵測到架構設計意圖）
AI → Routes to plan-eng (detects architecture intent)
   → 產出：技術選型 + DB Schema + API 設計 + 目錄結構
   → Produces: tech stack selection, DB schema, API design, directory structure
```

```
你：Review 我的改動，等等要推。
You: Review my changes before I push.

AI → 路由到 review + ship（偵測到 review + 部署意圖）
AI → Routes to review + ship (detects review + deployment intent)
   → 跑安全性/效能/可維護性檢查清單
   → Runs security/performance/maintainability checklist
   → 再跑部署檢查：git status、測試、build、環境變數
   → Then runs deploy checklist: git status, tests, build, env vars
```

---

## 技能總覽 / Skills Reference

### 策略層 / Strategy Layer

| 技能 Skill | 角色 Role | 觸發情境 Trigger |
|---|---|---|
| `office-hours` | 策略顧問 Strategy advisor | 「我想做 X 但⋯」釐清方向、挑戰假設 / Clarifying direction, challenging assumptions |
| `plan-ceo` | 產品策略師 Product strategist | 產品市場契合、定價、10 星體驗 / Product-market fit, pricing, 10-star experience |
| `deep-interview` | 需求訪談師 Requirements interviewer | 需求模糊、新專案啟動 / Vague requirements, new project kickoff |

### 工程層 / Engineering Layer

| 技能 Skill | 角色 Role | 觸發情境 Trigger |
|---|---|---|
| `plan-eng` | 系統架構師 System architect | DB schema、API 設計、技術選型 / DB schema, API design, tech selection |
| `task-decompose` | 任務拆解師 Task breakdown | Epic → Story → Task 拆解 / Task decomposition |
| `implement` | TDD 工程師 TDD engineer | 寫程式碼、實作功能 / Writing code, building features |
| `review` | Code 審查員 Code reviewer | 找生產炸彈，不是 style nitpick / Finding production bombs |
| `investigate` | 除錯偵探 Debugger | Bug、錯誤訊息、非預期行為 / Bugs, error messages |

### 維運層 / Operations Layer

| 技能 Skill | 角色 Role | 觸發情境 Trigger |
|---|---|---|
| `ship` | 部署把關員 Deploy gatekeeper | 推送、PR、部署 / Git push, PR, deploy |
| `git-auto` | Git 自動化 Git automation | 寫 commit message、changelog / Commit messages, changelog |
| `careful` | 安全攔截器 Safety interceptor | rm -rf、DROP TABLE、force-push / Dangerous commands |
| `confidence-check` | 信心度評估 Pre-flight check | 重大操作前信心度評分 / Confidence scoring before major changes |

### 內容層 / Content Layer

| 技能 Skill | 角色 Role | 觸發情境 Trigger |
|---|---|---|
| `brand-review` | 品牌稽核 Brand auditor | 視覺/語調一致性 / Visual/tone consistency |
| `research` | 研究分析師 Research analyst | 市場調查、技術比較 / Market analysis, tech comparison |
| `social-intel` | 趨勢掃描 Social trends scanner | Threads/IG 話題掃描 / Topic scanning, content calendar |
| `document` | 技術寫手 Technical writer | API 文件、release notes / API docs, release notes |
| `video-produce` | 影片製作人 Video producer | 腳本、Remotion、行銷影片 / Scripts, Remotion projects |

### 後設層 / Meta Layer

| 技能 Skill | 角色 Role | 觸發情境 Trigger |
|---|---|---|
| `retro` | 回顧引導師 Retrospective facilitator | 週回顧、Sprint 覆盤 / Weekly retros, lessons learned |
| `memory` | 本地記憶 Local memory | 決策紀錄、架構 memo / Decision logs, architecture memos |

---

## 使用指南 / Usage Guide

### 1. 策略與規劃 / Strategy & Planning

#### `office-hours` — 先想清楚再動手 / Think before you build

適用：你有想法但還沒驗證「為什麼」。
Best for: You have an idea but haven't validated the "why" yet.

```
你：我在考慮幫我的 SaaS 加一個即時通知系統。
You: I'm thinking about adding a real-time notification system to my SaaS.

AI (office-hours):
  → 「為什麼現在做這個很重要？觸發點是什麼？」
  → "Why is this important right now? What triggered this?"
  → 「如果不做會怎樣？」
  → "If you don't build it, what happens?"
  → 「有沒有更簡單的方式驗證這個需求？」
  → "What's the simplest way to validate this need?"
  → 產出：釐清摘要（重新定義的問題 + 下一步）
  → Produces: Clarification Summary with redefined problem + next steps
```

#### `plan-ceo` — 找到 10 星體驗 / Find the 10-star experience

適用：產品市場契合度評估、定價、競爭策略。
Best for: Product-market fit evaluation, pricing, competitive strategy.

```
AI (plan-ceo):
  → 評估目前體驗（例如 5/10）/ Rates current experience (e.g., 5/10)
  → 描述 10 星版本 / Describes the 10-star version
  → 找出達到 10 星的最大一步 / Identifies the single biggest step
  → 產出：CEO Review 摘要 + 90 天 roadmap
  → Produces: CEO Review Summary with 90-day roadmap
```

#### `deep-interview` — 把模糊想法變規格 / Turn vague ideas into specs

適用：新專案，需求還不清楚。
Best for: New projects where requirements are unclear.

```
AI (deep-interview):
  Round 1 — Why：「要解決什麼問題？誰會用？」/ "What problem? Who uses it?"
  Round 2 — What：「核心流程一句話描述？」/ "Core flow in one sentence?"
  Round 3 — How：「技術限制？要整合什麼？」/ "Tech constraints? Integrations?"
  Round 4 — 驗證：「成功標準？最優先的三件事？」/ "Success criteria? Top 3?"
  → 產出：需求規格摘要 / Produces: Requirements Spec
```

規則：每輪最多問 3 題，訪談過程中不寫任何程式碼。
Rules: Max 3 questions per round. Never writes code during the interview.

### 2. 開發 / Development

#### `plan-eng` — 從需求到架構 / From requirements to architecture

```
AI (plan-eng):
  → 技術選型（附理由）/ Tech stack selection with rationale
  → 完整 DB Schema（CREATE TABLE）/ Complete DB schema
  → API Endpoint 清單（method + path + auth + 回應格式）/ API endpoint list
  → 目錄結構 / Directory structure
  → 風險評估 / Risk assessment
```

你可以編輯 `plan-eng/SKILL.md` 自訂預設技術棧。
You can customize the default tech stack by editing `plan-eng/SKILL.md`.

#### `task-decompose` — 大任務拆小 / Break it down

```
AI (task-decompose):
  Epic: 使用者認證 / User Authentication
  
  Story 1: Email/密碼註冊 / Email/Password Registration
  - [ ] Task 1.1: 建立 users table migration (~30min)
        驗證 / Verify: Migration 跑完，table 存在
        依賴 / Depends: 無 / none
  - [ ] Task 1.2: 建立註冊 API endpoint (~1hr)
        驗證 / Verify: POST /api/auth/register 回傳 201
        依賴 / Depends: Task 1.1
```

規則：每個 Task 30 分鐘到 2 小時，最多 20 個 Task，高風險排最前。
Rules: Each task 30min–2hr. Max 20 tasks. Highest-risk tasks first.

#### `implement` — TDD 導向實作 / TDD-driven coding

```
AI (implement):
  1. 確認範圍和要改的檔案 / Confirms scope and files
  2. 先寫失敗測試 / Writes failing test first
  3. 寫最少程式碼讓測試通過 / Writes minimal code to pass
  4. 自我檢查：hardcode？錯誤處理？型別安全？/ Self-checks
  → 完成後交接給 review / Hands off to review when done
```

#### `review` — 找生產炸彈 / Find production bombs

```
AI (review):
  🔴 必須修（會在生產爆炸）/ MUST FIX (production bomb):
  1. src/api/auth.ts:42 — 密碼明文儲存 / Password stored in plain text
     修正 / Fix: 使用 bcrypt，salt rounds ≥ 10

  🟡 建議修（技術債）/ SHOULD FIX (tech debt):
  1. src/api/auth.ts:18 — 登入沒有 rate limiting
     修正 / Fix: 加 rate limiter middleware

  🟢 觀察（知道就好）/ NOTE:
  1. 考慮用 zod 做 request validation
```

檢查順序：安全性 → 資料完整性 → 效能 → 可維護性
Checklist: Security → Data integrity → Performance → Maintainability

#### `investigate` — 系統性除錯 / Systematic debugging

```
AI (investigate):
  Phase 1 — 複現 / Reproduce: 完整錯誤訊息？Stack trace？
  Phase 2 — 縮小範圍 / Narrow down: 最後正常是什麼時候？改了什麼？
  Phase 3 — 根因分析 / Root cause: 找到確切的檔案、行數、原因
  Phase 4 — 最小修正 + 驗證 / Minimal fix + verify no side effects
```

規則：一次追一個假說、讀 log、不擴大修改範圍。
Rules: One hypothesis at a time. Read the logs. Don't expand the fix scope.

### 3. 維運與安全 / Operations & Safety

#### `ship` — 安全部署 / Deploy with confidence

```
AI (ship):
  部署前檢查 / Pre-deploy checklist:
  ✅ git status — 沒有意外的未追蹤檔案 / no untracked files
  ✅ git diff --staged — 已審查 / reviewed
  ✅ 沒有 .env 或密鑰被 commit / No secrets in commit
  ✅ 測試通過 / Tests pass
  ✅ Build 成功 / Build succeeds
  ✅ 新環境變數已設定 / New env vars set
  → 生成 commit message → 執行 git add, commit, push
```

#### `careful` — 安全攔截器 / Safety interceptor

```
你：rm -rf ./data

AI (careful):
  🔴 危險：rm -rf 會永久刪除 ./data/
  🔴 DANGEROUS: rm -rf will permanently delete ./data/
  
  這個目錄包含 847 個檔案，包括你的 SQLite 資料庫。
  This directory contains 847 files including your SQLite database.
  
  更安全的替代方案 / Safer alternatives:
  1. mv ./data ./data-backup-$(date +%Y%m%d)
  2. rm -ri ./data（互動模式 / interactive mode）
  
  說「確認」繼續 / Say "confirm" to proceed.
```

攔截：`rm -rf`、`DROP TABLE`、`git push --force`、`chmod 777`、無 WHERE 的 DELETE。
Intercepts: `rm -rf`, `DROP TABLE`, `git push --force`, `chmod 777`, DELETE without WHERE.

#### `confidence-check` — 信心度評估 / Pre-flight confidence scoring

```
AI (confidence-check):
  | 維度 Dimension   | 分數 Score | 說明 Notes                   |
  |------------------|-----------|------------------------------|
  | 理解程度 Understanding | 20/25 | Migration script 已審查      |
  | 影響範圍 Impact scope  | 15/25 | 3 個相依服務未測試            |
  | 回復能力 Rollback plan | 10/25 | 備份未驗證                   |
  | 驗證方式 Verification  | 20/25 | Staging 測試通過              |
  | **總分 Total**        | **65/100** |                         |

  ⚠️ < 70 分 — 暫停。建議先驗證備份、測試相依服務。
  ⚠️ Score < 70 — PAUSE. Verify backup, test dependent services.
```

#### `git-auto` — 自動生成 Commit message

```
AI (git-auto):
  → 讀取 git diff --staged / Reads git diff --staged
  → 產出 / Generates: "feat: 新增使用者登入功能，支援 email/password 和 OAuth"
```

格式 / Format: `<type>: <description>` (feat/fix/refactor/docs/style/test/chore)

### 4. 內容與行銷 / Content & Marketing

#### `research` — 深度結構化研究 / Deep, structured research

```
AI (research):
  1. 定義 2-3 個研究問題 / Defines 2-3 research questions
  2. 第一輪（廣）：了解全貌 / Layer 1 (broad): survey the landscape
  3. 第二輪（深）：深入重要來源 / Layer 2 (deep): dive into top sources
  4. 第三輪（驗證）：交叉比對 / Layer 3 (verify): cross-reference
  → 產出：研究報告（摘要/發現/不同觀點/結論/來源）
  → Produces: Research Report (summary/findings/perspectives/conclusion/sources)
```

來源品質排序 / Source quality ranking: 官方文件 > 同行評審 > 產業報告 > 具名部落格 > 論壇

#### `social-intel` — 社群趨勢掃描 / Trend scanning

```
AI (social-intel):
  → 話題矩陣：熱門話題 + 互動量 / Topic Matrix with engagement levels
  → 高價值主題：為什麼值得做 + 建議切角 / High-value themes + suggested angle
  → 內容提案：主題 + 切角 + 形式 + 建議發布時間 / Content proposals
```

#### `video-produce` — 從腳本到成品 / Script to screen

```
AI (video-produce):
  | 時間 Time | 畫面 Visual    | 文字 Text/VO        | 備註 Note    |
  |----------|---------------|---------------------|-------------|
  | 0-3s     | App icon zoom | 「還在為⋯煩惱？」    | Hook 抓注意力 |
  | 3-10s    | 問題展示       | 痛點描述             | 建立共鳴     |
  | 10-25s   | 功能 walkthrough | 解決方案           | 核心價值     |
  | 25-30s   | CTA 畫面      | 「立即免費試用」      | 導流轉換     |
  
  → 也可以建立 Remotion 專案骨架 / Can also scaffold a Remotion project
```

### 5. 知識管理 / Knowledge Management

#### `memory` — 本地決策紀錄 / Local-first decision log

```
你：記住我們選用 Supabase 的決定。
You: Remember our decision to use Supabase.

AI (memory):
  Step 1 — Compact：萃取關鍵資訊，去除來回討論雜訊
           Extract key info, remove back-and-forth noise
  Step 2 — 分類 / Classify: decisions/（這是「選 A 不選 B」的決策）
  Step 3 — 預覽 / Preview:
    📁 decisions/2026-04-05-supabase-vs-firebase.md
    📝 選擇 Supabase：RLS 支援、Realtime 訂閱、Vercel 整合。
       拒絕 Firebase：Firestore 查詢限制。
    寫入嗎？/ Write to notes? [y/n]
  Step 4 — 儲存 + 更新 _index.md / Save + update index
```

儲存位置：任何本地目錄（Obsidian vault、~/docs、專案 docs/）。首次使用時詢問路徑。所有資料純本地，零外部連線。

Storage: any local directory (Obsidian vault, ~/docs, project docs/). Asks on first use. All data stays local — zero external calls.

#### `retro` — 週回顧 / Weekly retrospective

```
AI (retro):
  → 讀取 git log --since="1 week ago"
  → 提問：哪些做得好？哪裡卡住？學到什麼？
  → Asks: what went well? what was frustrating? what did you learn?
  → 產出 / Produces:
    ✅ 做得好 / Went well: 2 天內完成 auth（清楚的規格幫了大忙）
    🔄 可改善 / Improve: 花 3 小時在 CSS bug 上（應該用現有元件）
    💡 學到的 / Learned: Supabase RLS 比自訂 middleware 簡單
    
    下週行動 / Next week:
    1. [ ] 建立元件庫避免 CSS bug / Set up component library
    2. [ ] 寫 auth 整合測試 / Write integration tests for auth
    3. [ ] 文件化部署流程 / Document the deployment process
```

---

## 工作流管線 / Workflow Pipelines

SlimStack 的技能設計為可互相交接。以下是標準管線：

SlimStack skills are designed to hand off to each other. Standard pipelines:

### 新專案（完整生命週期）/ New Project (full lifecycle)
```
deep-interview → plan-eng → task-decompose → implement → review → ship
（釐清需求）     （架構設計）  （拆解任務）     （實作）     （審查）  （部署）
 clarify         design       break down      build       check    deploy
```

### 日常開發 / Daily Development
```
implement → review → ship
（實作）     （審查）  （推送）
```

### 除錯 / Bug Fix
```
investigate → implement → review → ship
（找根因）     （修正）     （驗證）  （部署）
```

### 高風險操作 / High-Risk Operation
```
confidence-check + careful → [操作 operation] → review
（信心度評估 + 安全攔截）                        （事後審查）
```

### 策略到執行 / Strategy → Execution
```
office-hours → plan-ceo → research → deep-interview → plan-eng
（為什麼？）    （值得做嗎？）（找資料）  （細化需求）      （架構設計）
```

### 內容行銷 / Content Marketing
```
social-intel → video-produce → brand-review → careful
（掃描趨勢）    （製作內容）     （品牌稽核）    （發布前確認）
```

### 週回顧 / Weekly Retrospective
```
retro → memory → office-hours
（覆盤） （記錄）  （規劃下週）
```

完整工作流指南見 [`references/workflow.md`](references/workflow.md)。

---

## 技能組合 / Skill Combinations

同時最多載入 **2 個技能**。強力組合：

Load up to **2 skills simultaneously**. Powerful combos:

| 情境 Scenario | 技能 Skills | 原因 Why |
|---|---|---|
| 高風險 code review | `review` + `careful` | 同時抓邏輯 bug 和危險操作 / Catch both logic bugs and dangerous operations |
| 生產環境部署 | `ship` + `careful` | 部署清單 + 危險攔截 / Deploy checklist + danger interception |
| 第一次做某系統 | `implement` + `confidence-check` | 實作同時評估準備度 / Code with readiness scoring |
| 生產除錯 | `investigate` + `careful` | 找 bug 同時防止改壞更多 / Find the bug without making it worse |

路由器偵測到重疊意圖時會自動組合，你也可以明確要求：

The router handles combinations automatically, or you can request explicitly:

```
你：Review 這段，要特別小心 — 這碰到了支付系統。
You: Review this with extra caution — it touches the payment system.
AI → 同時載入 review + careful / Loads review + careful simultaneously
```

---

## 漸進式撤除 SKILL0 / Progressive Offloading

SlimStack 實作 [SKILL0](https://arxiv.org/abs/2604.02268) 機制，隨技能內化自動減少 token 佔用：

### 三個層級 / Three Levels

| 層級 Level | 條件 Condition | 載入內容 Loaded | ~Tokens |
|---|---|---|---|
| **Full** | 使用 < 5 次 / Used < 5 times | 完整 SKILL.md / Complete file | 800-1500 |
| **Compact** | 5-14 次，近期無修正 / 5-14 times, no recent corrections | `## Compact Version` 區塊 / block only | 200-400 |
| **Zero** | ≥ 15 次，近期無修正 / ≥ 15 times, no recent corrections | 路由表一句話描述 / One-line from router | ~50 |

### 運作方式 / How It Works

1. 前 5 次使用：AI 每次都讀完整技能檔 / First 5 uses: full file every time
2. 持續使用且未被修正：AI 只讀精簡版 / Consistent use without corrections: compact summary only
3. 15 次以上：AI 不再讀檔 — 已內化 / 15+ uses: no file loaded — internalized

### 幫助度回升 / Helpfulness Rebound

如果 AI 在 Compact 或 Zero 層級的產出被修正：
- 該技能**立即回升到 Full** / That skill **immediately rebounds to Full**
- 修正被記錄 / The correction is logged
- 重新累積穩定次數 / The cycle restarts

確保「內化」是真正的內化，不是過早降級。

This prevents premature offloading — if the AI hasn't truly internalized a skill, it gets the full instructions again.

### 使用追蹤 / Usage Tracking

統計存在 `~/.slimstack/usage.json`：

```json
{
  "review": { "count": 12, "last_correction": 8 },
  "ship": { "count": 7, "last_correction": null },
  "careful": { "count": 20, "last_correction": 3 }
}
```

隨時可以說「用完整版」強制載入 Full。
You can force full loading anytime by saying "use the full version."

---

## 自訂 / Customization

### 設定你的技術棧 / Configure your tech stack

編輯 `plan-eng/SKILL.md`，設定你偏好的預設值。預設建議：

Edit `plan-eng/SKILL.md` to set your preferred defaults. Current suggestions:

```
- Frontend: Next.js (App Router) + React + Tailwind CSS
- Backend: Next.js API Routes 或獨立 API 框架 / or standalone API framework
- Database: PostgreSQL（Supabase / PlanetScale / 自建 self-hosted）
- Auth: Cookie-based Session / OAuth / JWT
- Hosting: Vercel / Railway / Fly.io
```

### 設定程式碼風格 / Configure code style

編輯 `implement/SKILL.md`，改成你的慣例：

Edit `implement/SKILL.md` to match your conventions.

### 設定記憶存放路徑 / Configure memory storage

`memory` 技能將筆記存在本地。首次使用時會詢問路徑。常見設定：

The `memory` skill stores notes locally. On first use, it asks for your path. Common setups:

```
# Obsidian vault
~/Documents/ObsidianVault/slimstack-memory/

# 簡單本地目錄 / Simple local docs
~/docs/slimstack-memory/

# 專案內 / Inside your project
./docs/decisions/
```

### 新增自訂技能 / Adding your own skills

**步驟 1 / Step 1：** 建立目錄和 SKILL.md / Create directory with SKILL.md:

```bash
mkdir -p ~/.claude/skills/slimstack/my-skill
```

**步驟 2 / Step 2：** 依照模板撰寫 / Write following this template:

```markdown
---
name: my-skill
description: |
  何時觸發這個技能。明確描述使用者意圖的關鍵字。
  When to trigger. Be specific about user intent keywords.
---

# Skill Name — 角色名稱 / Role Title

[描述 AI 在此技能中的角色 / Describe the AI's role]

## 工作流程 / Workflow

### Step 1: [第一階段 / First Phase]
[做什麼 / What to do]

### Step 2: [第二階段 / Second Phase]
[做什麼 / What to do]

## 輸出格式 / Output Format

[結構化輸出模板 / Template for structured output]

## 交接 / Handoff

- 下一步 A → `other-skill`
- 下一步 B → `another-skill`

---

## Compact Version

**角色 / Role**: [一句話 / One line]
**流程 / Flow**: [Step 1] → [Step 2] → [Step 3]
**交接 / Handoff**: [去哪裡 / Where to go next]
```

**步驟 3 / Step 3：** 在根目錄 `SKILL.md` 加入路由條目 / Add routing entry in root `SKILL.md`.

### 移除不需要的技能 / Removing unused skills

直接刪除目錄，路由器會跳過不存在的技能：

Simply delete the directory. The router skips missing skills:

```bash
rm -rf ~/.claude/skills/slimstack/video-produce
```

然後移除根 `SKILL.md` 路由表中對應的行。
Then remove the corresponding line from the router table.

---

## 專案結構 / Project Structure

```
slimstack/
├── SKILL.md                  ← 路由器 Router（常駐 context，~150 tokens）
├── README.md
├── LICENSE
├── .gitignore
├── references/
│   └── workflow.md           ← 工作流指南 Workflow guide
├── memory/
│   ├── SKILL.md
│   └── store/.gitkeep        ← 本地記憶存放 Local memory (gitignored)
│
│  ── 策略 Strategy ──
├── office-hours/SKILL.md     ← 策略顧問 Strategic advisor
├── plan-ceo/SKILL.md         ← 產品策略師 Product strategist
├── deep-interview/SKILL.md   ← 需求訪談師 Requirements interviewer
│
│  ── 工程 Engineering ──
├── plan-eng/SKILL.md         ← 系統架構師 System architect
├── task-decompose/SKILL.md   ← 任務拆解師 Task breakdown
├── implement/SKILL.md        ← TDD 工程師 TDD engineer
├── review/SKILL.md           ← Code 審查員 Code reviewer
├── investigate/SKILL.md      ← 除錯偵探 Debugger
│
│  ── 維運 Operations ──
├── ship/SKILL.md             ← 部署把關員 Deploy gatekeeper
├── git-auto/SKILL.md         ← Git 自動化 Git automation
├── careful/SKILL.md          ← 安全攔截器 Safety interceptor
├── confidence-check/SKILL.md ← 信心度評估 Pre-flight check
│
│  ── 內容 Content ──
├── brand-review/SKILL.md     ← 品牌稽核 Brand auditor
├── research/SKILL.md         ← 研究分析師 Research analyst
├── social-intel/SKILL.md     ← 趨勢掃描 Social trends scanner
├── document/SKILL.md         ← 技術寫手 Technical writer
├── video-produce/SKILL.md    ← 影片製作人 Video producer
│
│  ── 後設 Meta ──
└── retro/SKILL.md            ← 回顧引導師 Retrospective facilitator
```

---

## 常見問題 / FAQ

### 需要用到全部 19 個技能嗎？/ Do I need all 19 skills?

不用。用你需要的就好。可以刪除不用的技能目錄並移除路由條目。最小配置可能只需要 `implement` + `review` + `ship`。

No. Use what you need. Delete unused skill directories and remove their routing entries. A minimal setup might be just `implement` + `review` + `ship`.

### 只支援繁體中文嗎？/ Does it only work in Traditional Chinese?

技能檔案用繁體中文撰寫，但 AI 會根據你使用的語言回應。你用英文對話，AI 就用英文回應，同時遵循中文指令。你也可以將技能檔翻譯成你偏好的語言。

Skill files are in Traditional Chinese, but the AI responds in whatever language you use. Speak English, get English responses — while the AI follows the Chinese instructions internally. You can also translate the files.

### 路由怎麼運作？我不用 slash command 也可以嗎？/ How does routing work without slash commands?

路由器匹配的是**意圖**，不是特定指令。說「我覺得支付流程有 bug」就會載入 `investigate`。說「我們來想想這個功能值不值得做」就會載入 `office-hours`。你不需要明確指定技能名稱。

The router matches **intent**, not specific commands. Say "I think there's a bug in the payment flow" and it loads `investigate`. Say "let's think about whether this feature is worth building" and it loads `office-hours`. You never need to name a skill explicitly.

### 可以在 Claude Code 以外的地方使用嗎？/ Can I use it outside Claude Code?

可以。技能檔案是純 Markdown，適用於任何接受 system prompt 或 context 檔案的 AI 工具。SKILL0 漸進式撤除需要持久化檔案系統（存 `usage.json`），在 Claude Code 或類似有本地檔案存取的工具上效果最好。

Yes. The skill files are plain Markdown and work with any AI that accepts system prompts or context files. The SKILL0 progressive offloading feature requires a persistent filesystem (for `usage.json`), so it works best with Claude Code or similar tools with local file access.

### SlimStack 佔多少 context？/ How much context does SlimStack use?

- 路由器（常駐）/ Router (permanent): ~150 tokens
- 一個載入的技能 / One loaded skill: ~800-1500 tokens (Full) / ~200-400 (Compact) / ~50 (Zero)
- 任何時刻最大值 / Maximum at any time: 路由器 + 2 技能 ≈ 3,000-3,200 tokens

這只佔大多數 AI context window（100K-200K tokens）的一小部分。

This is a fraction of most AI context windows (100K-200K tokens).

### `office-hours` 跟 `plan-ceo` 差在哪？/ What's the difference?

`office-hours` 幫你**釐清要做什麼** — 挑戰假設、問「為什麼」、找到真正的問題。`plan-ceo` 評估**值不值得做** — 給產品打分、找 10 星體驗、建 roadmap。先用 `office-hours` 釐清方向，再用 `plan-ceo` 驗證。

`office-hours` helps you **clarify what to do** — challenges assumptions, asks "why", finds the real problem. `plan-ceo` evaluates **whether to do it** — scores your product, finds the 10-star version, builds a roadmap. Use `office-hours` first when confused, then `plan-ceo` for validation.

### `review` 跟 `careful` 差在哪？/ What's the difference?

`review` 是**結構化 code review**，檢查安全性、資料完整性、效能、可維護性。`careful` 是**即時攔截器**，在危險指令執行前攔住。它們互補 — merge 前用 `review`，操作中用 `careful`。

`review` is a **structured code review** checking security, data integrity, performance, maintainability. `careful` is a **real-time interceptor** catching dangerous commands before execution. They complement each other — use `review` before merging, `careful` during live operations.

---

## 語言 / Language

技能檔案以**繁體中文**撰寫。AI 助手能原生處理，不影響對話語言。如需要，你可以翻譯成偏好的語言。

Skill files are written in **Traditional Chinese (繁體中文)**. The AI processes them natively regardless of conversation language. Translate to your preferred language if needed.

## 授權 / License

[MIT](LICENSE)

## 作者 / Author

Built by [@JoshuaWangTW](https://github.com/JoshuaWangTW)
