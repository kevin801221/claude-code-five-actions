# 維護教訓：讓錯誤能被重新抓到

## 完整通過需要核對執行數量

獨立審查發現：只檢查測試總數和失敗名稱，會把 skipped 的 fixed 測試也算成通過。現在驗證器核對 pass、fail、skipped、cancelled、todo；[回歸測試](../tests/test_acceptance_runner.py)會在暫存副本跳過一項驗收，要求驗證器拒絕假綠。

## 上游回應中斷仍需留下複查訊號

獨立審查以截斷的 HTTP chunked response 重現 IncompleteRead；先前例外會使監測中斷，來不及產生報告。現在此類 HTTPException 被記錄為 unreachable，舊基準保持不變。[回歸測試](../tests/test_sources.py)使用真正的本機 HTTP server 重現，避免只有正常抓取路徑被測到。
