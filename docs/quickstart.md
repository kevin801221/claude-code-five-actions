# 五分鐘開始：先讓一個任務可以驗收

[回首頁](../README.md)

## 1. 選一個小任務，寫出完成條件

把 [SPEC 範本](../templates/SPEC.md)複製到自己的專案。寫下目標、可觀察的條件、必須保留的行為與限制。例如：「閒置不漂移」以及「手動捲動仍正常」。

## 2. 找一個真的能失敗的檢查

可以是測試、build、linter 或輸出比對。先確認它能抓到眼前的問題，再交給 agent 修改。用 [證據範本](../templates/EVIDENCE.md)回報實際執行結果。

想先體驗本 repo 的案例，安裝 Node.js 20+ 後，在 repo 根目錄執行：

```bash
node examples/scroll-drift/verify.mjs
```

三個版本的結果必須分別是 3/4、1/4、4/4 通過。前兩個版本的失敗是案例的必要證據；驗證器會檢查它們是否敗在正確的驗收條件。

## 3. 用新 reviewer 對照規格

把原始 SPEC、diff 與證據交給未參與實作的 reviewer。使用 [Reviewer prompt](../templates/REVIEW.md)，要求先報影響正確性的缺口。

## 4. 加一條適用的環境限制

參考 [邊界範例](../templates/boundaries/README.md)。先在一次性範例中測試通過與失敗情況，再整合到既有設定。此 repo 不會因為 clone 而替你安裝全域 hook。

## 5. 留下一個可重用的教訓

同一種錯再次發生，就填寫 [LESSONS](../templates/LESSONS.md)：哪個舊案例會失敗、新檢查放在哪裡、修正後如何通過。

## 手動觀察瀏覽器版本

在 repo 根目錄執行：

```bash
python3 -m http.server 8787 --bind 127.0.0.1
```

開啟 [本機案例頁](http://127.0.0.1:8787/examples/scroll-drift/)，切換三種版本。測完用 Ctrl+C 停止伺服器。這個頁面的手動觀察，與 Node 驗收測試的範圍不同；詳見[驗證紀錄](verification.md)。
