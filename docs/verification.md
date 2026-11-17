# 驗證紀錄與範圍

[回首頁](../README.md) · [維護方式](../MAINTENANCE.md)

此頁把「實際跑過」與「讀過來源」分開記錄。CI 通過不代表原始講義每一句話都已重新驗證。

| 項目 | 狀態 | 證據與邊界 |
| --- | --- | --- |
| 捲動案例的 JavaScript policy | 可執行檢查 | [同一份驗收測試](../examples/scroll-drift/acceptance.test.mjs)對三種版本執行；[紀錄](../examples/scroll-drift/evidence.json)含 Node 版本、時間與檔案雜湊 |
| Stop wrapper | 程式層級測試 | [subprocess 測試](../tests/test_stop_hook.py)檢查成功、失敗、找不到命令與逾時；不等於已在每個 Claude Code 版本做 session 整合測試 |
| Markdown、JSON、原稿完整性 | 可執行檢查 | `python3 scripts/check_repo.py`；只檢查本地文件連結，不把外部連結可達性當成語意正確 |
| Stop hook 的 exit 2 行為 | 官方來源複查 | 2026-11-17 閱讀 [Hooks reference](https://code.claude.com/docs/en/hooks)的 Stop 事件與 exit code 契約；行為依事件而異 |
| 專案 settings 的放置位置 | 官方來源複查 | 2026-11-17 閱讀 [Settings](https://code.claude.com/docs/en/settings)；範本需要手動整合，不自動覆寫 |
| 上游內容是否改變 | 自動觀察 | [來源清單](../maintenance/sources.json)與[指紋基準](../maintenance/upstream-baseline.json)；指紋相同不代表已完整實測 |
| 原稿中的模型名稱、二手演講數字與所有 CLI 範例 | 待逐項複查 | 保留原始署名與內容，不能以本 repo 的 CI 徽章替它們背書 |
| 瀏覽器 UI | 單次手動 smoke check | [觀察紀錄](../examples/scroll-drift/manual-browser-smoke.json)：fixed 能捲動、overfixed 滾輪不動、buggy 閒置會漂移；不是持續執行的瀏覽器整合 suite |
| 真實 Claude session | 尚未整合驗證 | 未宣稱在每個 Claude Code 版本測過 hook；見[路線圖](../ROADMAP.md) |
| 增補稿的技術限制 | 官方來源複查 | 2026-11-17 閱讀 Hooks、Permissions、Sandboxing、CLI reference、Mermaid config 與 W3C 幾何／字型規範；各主張與連結見[補充篇](field-notes.zh-TW.md)。未執行這些整合 |
| 會議記錄與半導體情境 | 設計教材，尚未實作 | [會議記錄](cases/meeting-notes.md)與[四個半導體情境](cases/semiconductor.md)列出條件、失敗樣本與邊界；沒有 STT、Mermaid 量測、Mailpit、EDA 或檢索問答的執行證據 |

新增「已驗證」項目時，需附環境、指令、輸出和來源；若只比對文件，使用「來源複查」狀態。
