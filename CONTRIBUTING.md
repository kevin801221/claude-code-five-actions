# 一起改善五個動作

歡迎更正來源、回報失效範例與分享可重現案例。先從一個小變更開始。

## 提交前

1. 新行為要有可判定的條件。修 bug 先留下失敗案例。
2. 新增建議附一手來源；指令附版本、平台與實際輸出。
3. 區分「來源複查」與「實際執行」，不要只更新日期。
4. 執行 `python3 scripts/check_repo.py`。需要 Python 3.11+、Node.js 20+。
5. PR 寫清楚改了什麼、為什麼與如何驗證。影響原始課程內容時，先另提更正，保留署名與原稿。

## 可以從這裡開始

- [失效範例](https://github.com/kevin801221/claude-code-five-actions/issues/new?template=broken-example.yml)
- [內容更正](https://github.com/kevin801221/claude-code-five-actions/issues/new?template=correction.yml)
- [實戰案例](https://github.com/kevin801221/claude-code-five-actions/issues/new?template=case-study.yml)

檢查結果只證明測試涵蓋的條件。請在證據回報中列出未涵蓋範圍，移除私人資料與憑證。

## 原稿與權利

見 [ATTRIBUTION.md](ATTRIBUTION.md)。請只提交自己有權分享的內容；此版本尚未為整個 repo 指定統一的開放授權。
