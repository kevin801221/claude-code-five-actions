# Artifact Insights Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 將使用者提供的補充稿，整理為可採用、可驗收且有來源界線的教材。

**Architecture:** 保留原始講義與雜湊，以獨立補充篇承接新觀點。案例連回既有五個動作範本，區分可執行 fixture、來源複查與尚未實作的設計案例。

**Tech Stack:** Markdown；既有 Python 3.11+ / Node.js 20+ 離線檢查。

### Task 1: 篩選與來源查核

- 比對原稿，只補新增價值：實際產物、驗收的反例、風險與規劃、共用語言。
- 查核 Stop hook、權限、sandbox、執行上限與 Mermaid 量測的適用範圍。
- 在 `docs/field-notes.zh-TW.md` 記錄採用方式與未採用的絕對化說法。

### Task 2: 範本與案例

- 新增 `templates/ARTIFACT-CHECKS.md`，讓規格對應產物、檢查、失敗樣本與證據。
- 補強 `templates/EVIDENCE.md` 與 `templates/REVIEW.md` 對檢查本身的驗收。
- 新增 `docs/cases/meeting-notes.md` 與 `docs/cases/semiconductor.md`；不加入假指令或未實作腳本。
- 更新中英文 README、quickstart、署名、驗證範圍與 changelog。

### Task 3: 驗證與交付

- 基線先執行 `python3 scripts/check_repo.py`：23 項 Python 測試與三個捲動版本符合預期。
- 編輯後重跑相同檢查，確認原稿雜湊不變；文件變更不新增鏡像測試。
- 獨立審查來源、連結、過度承諾、範例狀態與私人資料。
- 確認 GitHub owner、SSH 身分與 remote 後，提交 PR 並依既有授權整合至公開 repo。
