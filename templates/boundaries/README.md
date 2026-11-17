# 邊界與 Stop hook 範例

[回到五個動作](../../README.md)

先列出能碰的資料、路徑、服務與分支，以及需要人核准的交付動作。規則與 sandbox 各有作用範圍，依官方 [permissions](https://code.claude.com/docs/en/permissions) 與 [sandboxing](https://code.claude.com/docs/en/sandboxing) 文件配置；此範本不宣稱提供完整隔離。

## 用本 repo 體驗完成前檢查

[settings.example.json](settings.example.json) 是選配範例，需 Python 3.11+、Node.js 20+。先讀內容，再將 hooks 區塊手動整合到這個 repo 的 `.claude/settings.json`；保留原本的設定。不要把整份檔案覆蓋到個人的全域設定。

它執行 [Stop wrapper](../../scripts/stop_hook.py)，再跑 repo 檢查。子命令通過才允許結束；失敗、無法啟動或逾時會回傳 2 並附明確的 block decision，輸出保留在 stderr。依據是官方 [Stop hook 契約](https://code.claude.com/docs/en/hooks)。

可先手動確認兩條路徑（在 repo 根目錄執行）：

```bash
python3 scripts/stop_hook.py -- python3 -c 'print("check passed")'
python3 scripts/stop_hook.py -- python3 -c 'raise SystemExit(1)'
```

第一個命令回傳 0，第二個回傳 2。範本的 shell 命令適用 Bash / zsh；Windows 的 shell 設定需按官方文件調整。換專案時，把 wrapper 後方的命令換成該專案的真實驗收檢查。

## 驗證邊界

CI 測試的是 wrapper 的程式行為與設定 JSON 語法，尚未宣稱完成各版本 Claude session 的整合測試。Stop hook 可以被設定移除，也不能代替 PR 的 CI。這些機制都只攔截其實際涵蓋的條件。
