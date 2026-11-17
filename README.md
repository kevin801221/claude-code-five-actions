# Claude Code：五個動作，可靠交付

**讓 agent 的「完成了」，變成你能驗證的交付。**

五個動作 × 圖解指南 × 可用範本 × 可重現的失敗案例。

[English](README.en.md) · [五分鐘開始](docs/quickstart.md) · [完整圖文講義](docs/guide.zh-TW.md) · [產物驗收補充篇](docs/field-notes.zh-TW.md) · [驗證範圍](docs/verification.md)

[![Checks](https://github.com/kevin801221/claude-code-five-actions/actions/workflows/check.yml/badge.svg)](https://github.com/kevin801221/claude-code-five-actions/actions/workflows/check.yml)
[![Maintenance](https://github.com/kevin801221/claude-code-five-actions/actions/workflows/maintenance.yml/badge.svg)](https://github.com/kevin801221/claude-code-five-actions/actions/workflows/maintenance.yml)

![人定義完成與邊界，agent 實作、驗證與接受審查，再帶著證據交付。](images/01-cover.png)

## 你可能遇過

Agent 說測試都過了，你一跑卻壞掉。修好眼前的 bug，正常功能也一起被關掉。同一種錯，每個 PR 都要你再抓一次。

這個 repo 把處理這些問題的方法，整理成五個可操作的動作。適合已經使用 coding agent、希望提高交付可信度的開發者與小型團隊。

## 五個動作，現在就能用

| 動作 | 你要留下什麼 | 直接使用 |
| --- | --- | --- |
| 1. 定義完成 | 能判定通過或失敗的驗收條件 | [SPEC 範本](templates/SPEC.md) |
| 2. 自我驗證 | 執行指令、輸出與驗證範圍 | [證據回報範本](templates/EVIDENCE.md) |
| 3. 獨立審查 | 對照原始規格找到的正確性缺口 | [Reviewer prompt](templates/REVIEW.md) |
| 4. 確定性邊界 | 工具、環境與交付動作的限制 | [邊界與 Stop hook 範例](templates/boundaries/README.md) |
| 5. 教訓進結構 | 能攔下過去錯誤的新檢查 | [教訓轉檢查範本](templates/LESSONS.md) |

## 不只測程式，也驗收最後交付的東西

摘要有四個標題，不代表沒有漏決議；SVG 能輸出，不代表放進信件後仍然可讀。新補充篇把「數字量測、截圖審查、實際操作」接回五個動作，並要求重要檢查能抓到一個已知錯誤。

- [驗證產物，也驗證你的檢查](docs/field-notes.zh-TW.md)：六個可採用的觀點、團隊導入門檻與來源限制。
- [產物驗收表](templates/ARTIFACT-CHECKS.md)：把規格、產物、錯誤樣本與證據放在同一張表。
- [會議記錄幫手](docs/cases/meeting-notes.md)：STT → 摘要 → Mermaid → 測試信件的五步設計。
- [四個半導體情境](docs/cases/semiconductor.md)：regression 分類、Tcl 遷移、良率週報、IP 文件問答。

後兩項是教學設計，尚未實作應用；可立即執行的案例在下方。

## 一個案例，三種結果

「畫面閒置時，每 750ms 自己向下漂移。」

| 版本 | 閒置不漂移 | 手動捲動正常 | 完整驗收 |
| --- | --- | --- | --- |
| buggy：原始問題 | 失敗 | 通過 | 失敗 |
| overfixed：停用全部捲動 | 通過 | 失敗 | 失敗 |
| fixed：只移除閒置漂移 | 通過 | 通過 | 通過 |

這是刻意建立的最小教學案例。三個版本跑同一份驗收測試，讓你看見「一項變綠」與「完整符合規格」的差別。

```bash
git clone https://github.com/kevin801221/claude-code-five-actions.git
cd claude-code-five-actions
node examples/scroll-drift/verify.mjs
```

需要 Node.js 20+；不需安裝套件、不需 API key。預期輸出：

```text
buggy: 3/4 pass; 1 expected failures
overfixed: 1/4 pass; 3 expected failures
fixed: 4/4 pass; 0 expected failures
```

[讀完整案例](examples/scroll-drift/README.md) · [看實際執行紀錄](examples/scroll-drift/evidence.json)

## 選你的閱讀路徑

- **五分鐘帶回專案：**[快速開始](docs/quickstart.md)，從一份 SPEC 與一個檢查開始。
- **想看懂方法：**[完整圖文講義](docs/guide.zh-TW.md)，保留原始課程、8 張情境圖與講者提示。
- **正在比較流派：**[superpowers、Matt、pstack 的選擇方式](docs/comparison.md)。
- **要管理團隊：**[維護規則](MAINTENANCE.md)與[驗證紀錄](docs/verification.md)。

## 這份指南怎麼保持有用

每次 PR 都檢查本地連結、JSON、原稿完整性、Stop wrapper 與捲動驗收案例。每週一 09:17（Asia/Taipei），GitHub Actions 重跑檢查並比對追蹤中的上游來源。

來源有變更或抓取失敗時，建立或更新一張待複查 Issue。**來源變動不會自動變成新的建議，也不會自動更新「已驗證」日期。** 詳細範圍見 [MAINTENANCE.md](MAINTENANCE.md)。Maintenance 徽章代表工作執行情況，內容的新鮮度仍要看來源報告與待複查 Issue。

## 一起改進

- [回報失效範例](https://github.com/kevin801221/claude-code-five-actions/issues/new?template=broken-example.yml)
- [提供內容更正](https://github.com/kevin801221/claude-code-five-actions/issues/new?template=correction.yml)
- [分享你的實戰案例](https://github.com/kevin801221/claude-code-five-actions/issues/new?template=case-study.yml)

新增案例請附驗收條件、重現方式與結果。參考 [貢獻指南](CONTRIBUTING.md)、[更新紀錄](CHANGELOG.md)與[路線圖](ROADMAP.md)。

## 來源與署名

原始課程署名 **@Luo Zih-Jia**。本 repo 保留原稿，新增導覽、範本、教學程式與維護流程。流派作者與上游來源請見 [ATTRIBUTION.md](ATTRIBUTION.md)；授權範圍亦在該頁說明。
