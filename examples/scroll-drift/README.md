# 案例：畫面不漂移，使用者仍能捲動

[回首頁](../../README.md) · [驗收單](SPEC.md)

這個案例是刻意建立的最小教學 fixture，不是從真實產品擷取的事故或效能 benchmark。

## 1. 定義完成

看 [SPEC.md](SPEC.md)：閒置十個 timer tick 位置不變；手動向上、向下捲動仍有效；不能捲到起點之前。

## 2. 先看會失敗的版本

```bash
SCROLL_VARIANT=buggy node --test examples/scroll-drift/acceptance.test.mjs
```

在 repo 根目錄執行。這個命令**應該回傳 1**，因為閒置位置從 120 漂到 130。這是預期失敗，不是安裝出錯。環境變數的寫法適用 Bash / zsh；Windows 可直接跑下方的跨平台驗證器。

## 3. 檢查看似修好的版本

`overfixed` 保留位置不變，因此閒置檢查通過，但手動捲動與邊界條件失敗。它把功能一起關掉了。這是 reviewer 對照原始規格能抓到的缺口。

## 4. 完整修正並留下證據

```bash
node examples/scroll-drift/verify.mjs
```

驗證器會依序執行 `buggy`、`overfixed`、`fixed`，確認四個測試都執行、失敗名稱符合預期，且 fixed 全綠。任一結果不符，整個驗證器回傳失敗。

如需產生自己的執行紀錄：

```bash
node examples/scroll-drift/verify.mjs --record
```

[既有紀錄](evidence.json)包含當時環境與檔案雜湊，不能代表所有平台。這個 suite 驗證瀏覽器頁面共用的 policy 函式；不模擬 DOM、滑鼠事件或 Claude session。

## 5. 手動看畫面

在根目錄執行 `python3 -m http.server 8787 --bind 127.0.0.1`，再開啟 [案例頁](http://127.0.0.1:8787/examples/scroll-drift/)。切換版本、停下操作、在內容區滾動滑鼠滾輪。停止伺服器用 Ctrl+C。

## 教訓進結構

保留完整驗收 suite，未來只要修正又停用了手動捲動，就會重新變紅。參考 [LESSONS 範本](../../templates/LESSONS.md)。
