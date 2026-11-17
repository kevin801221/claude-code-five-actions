# 維護方式

## 完成的定義

每次變更需保留原稿、附適用來源或執行證據，並讓 `python3 scripts/check_repo.py` 通過。文件來源複查、程式測試與 Claude session 整合測試分開記錄，見 [驗證範圍](docs/verification.md)。

## 每次 PR

[Checks](.github/workflows/check.yml) 在 Python 3.11 / Node 20 與 Python 3.13 / Node 22 的 Ubuntu runner 上執行：本地 Markdown 目的地、JSON、原始課程雜湊、Python 測試與捲動案例。這是明列的測試矩陣，不代表其他作業系統已測過。執行環境以該次 Actions log 為準。

## 每週一 09:17，Asia/Taipei

[Maintenance](.github/workflows/maintenance.yml) 的 cron 使用 UTC 01:17。它在預設分支重跑檢查，再比對 [sources.json](maintenance/sources.json) 的來源與 [upstream-baseline.json](maintenance/upstream-baseline.json) 的觀察指紋。可在 Actions 頁面手動執行。

- `unchanged`：與觀察基準相同，沒有新增的來源變動訊號。
- `changed` / `new`：需要複查相關內容。
- `unreachable`：抓取失敗，保留舊基準，需判斷是網路或來源搬遷。

有待複查項目時，只建立或更新一張帶 `upstream-review` 標籤的 Issue；同樣的內容不重複留言或建單。乾淨結果不發通知。此流程不自動更新文章、合併 PR 或刷新驗證日期，不需要模型 API key。

GitHub 排程可能延遲；公開 repo 連續 60 天無活動時，平台會自動停用排程。每月維護時需確認排程仍啟用；詳見 [GitHub schedule 文件](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)。

## 收到上游複查 Issue 時

1. 閱讀官方來源或固定 commit 的差異，找出受影響的段落與範本。
2. 需要改動時，以 PR 修改並補上能重現問題的檢查。
3. 跑相關範例；在 docs/verification.md 記錄來源、版本、日期、證據與限制。
4. 完成複查後，刻意刷新觀察基準：

```bash
python3 scripts/watch_sources.py --refresh
python3 scripts/check_repo.py
```

5. 審查基準差異後提交；合併並確認維護流程重新通過，再關閉對應 Issue。`--refresh` 只更新觀察基準，不會修改任何「已驗證」宣告；任一來源不可達時，不會覆寫基準。

## 每月

檢視未處理的更正與實戰案例、確認排程可用、移除過時內容。只有對使用者有實質影響的變更才整理 release。維護節奏可依實際使用量調整。

## 權限與責任

觀察步驟使用 GitHub Actions 內建 token 查詢 GitHub API，避免共用 runner 的匿名限流；只有 HTTPS api.github.com 請求附帶授權，其他來源與跨站重新導向不會收到 token。一般檢查只有 contents:read；每週觀察的 Issue 步驟另有 issues:write，不會推送 commit。不使用 pull_request_target 執行外部 PR 的程式。維護者 kevin801221 負責內容取捨與來源複查；外部貢獻方式見 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 已知範圍

上游追蹤是指定文件或路徑的版本變動，不涵蓋所有 skill 的實作、所有平台發布資訊或連結內容的語意。原稿待複查項目保留在 [驗證紀錄](docs/verification.md)與[路線圖](ROADMAP.md)。授權選擇仍由權利人確認，見 [ATTRIBUTION.md](ATTRIBUTION.md)。
