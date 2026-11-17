# 補充篇：驗證產物，也驗證你的檢查

[回首頁](../README.md) · [完整原稿](guide.zh-TW.md) · [產物驗收表](../templates/ARTIFACT-CHECKS.md)

這份補充篇取材自 2026-11-17 使用者提供的同名課程增補稿，保留 **@Luo Zih-Jia** 的作者署名。來源是[這份 Claude Artifact](https://claude.ai/artifact/WqUjxX1zCcjWqSp79bGgyh#6832ad0f-0456)的使用者貼文全文；分享頁要求登入，未將連結可讀性當成內容驗證。以下是編輯後的教學建議，原始講義保持不變。

## 1. 把「程式能跑」接到「產物符合需求」

Build 通過證明程式能建置；摘要正確、圖可讀、信寄給對的人，還需要各自的證據。先問讀者最後會收到什麼，再決定驗收方式。

| 產物 | 可量的條件 | 仍要判斷的部分 |
| --- | --- | --- |
| 網頁 | 關鍵操作能完成、目標尺寸無溢出、錯誤可見 | 資訊層級、文案是否易懂 |
| 圖表 | 標籤沒有被裁切、在交付尺寸可讀、資料與已知答案一致 | 閱讀順序、是否傳達正確關係 |
| 摘要 | 對照標註資料，決議與待辦沒有遺漏或憑空增加 | 語意、歧義、發言脈絡 |
| 信件 | 本次執行的收件人、內容與圖片皆正確 | 是否適合對外發送、誰有權核准 |

用三種互補的證據：**量測數字、查看截圖、實際操作**。自動量測抓確定的缺陷，截圖檢查整體閱讀效果，操作驗證完整流程。選擇與需求有關的方式，不要求每個任務都湊齊三種。[官方驗證建議](https://code.claude.com/docs/en/best-practices#give-claude-a-check-to-run)可作方法參考。

## 2. 新檢查必須抓得到一個已知錯誤

檢查也可能寫錯。例如只驗證 SVG 檔案存在，字被裁掉照樣會綠；只檢查摘要有「待辦」標題，待辦全漏也會綠。

每條重要驗收都準備一個**故意做錯的樣本**：刪掉一項決議、把字縮小、換成別次執行的信件。確認檢查在正確的條件上失敗，再讓正確樣本通過。無法讀取、無法量測或沒有執行到的條件，回報「未驗證」或失敗，不能直接略過算綠。

這正是本 repo [捲動案例](../examples/scroll-drift/README.md)的做法：保留 buggy 與 overfixed，確認它們分別敗在預期條件；只有 fixed 全過。把這個思路帶到文件、圖表與信件，使用[產物驗收表](../templates/ARTIFACT-CHECKS.md)。

## 3. 「好看」能拆出檢查，不能只剩數字

補充稿提出字級 16px、最多 12 個節點、留白與比例上限。這些適合當**團隊試用的起點**，不是所有圖表的通用標準。先寫明展示尺寸、圖表類型與讀者，再拿真實樣本校準。

Mermaid 要先渲染再量測，並留意以下限制：

- 等字型載入後再量；CSS 字級仍會受到 SVG 縮放與最後展示尺寸影響。[字型載入規範](https://www.w3.org/TR/css-font-loading-3/#font-face-set-ready)、[SVG viewBox](https://www.w3.org/TR/SVG2/coords.html#ViewBoxAttribute)
- 圓形、菱形的外接矩形不能證明文字位於形狀內。這是依[外接矩形定義](https://drafts.csswg.org/cssom-view/#dom-element-getboundingclientrect)得出的幾何限制；需限定支援形狀或另做形狀檢查。
- 選取器找不到節點、標籤或外框時，要明確失敗；[HTML labels 設定](https://mermaid.js.org/config/schema-docs/config.html#htmllabels)與版本差異都可能改變可量測的結構。
- 自動量測過關後，仍在最終交付尺寸查看截圖；布局、線條交叉與內容語意不會因幾個門檻通過就自動正確。

本次沒有把增補稿的 `check_mermaid_style.py` 收為已驗證程式；以上列的是實作它之前的驗收要求。可直接拿去討論的完整設計見[會議記錄幫手](cases/meeting-notes.md)。

## 4. 規劃隨風險調整，共用語言先固定

小、可逆、已知如何驗收的修改，用一段目標與檢查即可開始。跨模組、資料遷移或外部副作用，先寫 SPEC、保留行為與回復方式。規劃重量由做錯的影響決定，不必替流派選邊。

術語有歧義時，在專案的 GLOSSARY 記錄「名稱、定義、單位、例子、排除什麼」。例如良率的分母是 wafer、die 還是測試次數？共用定義會同時影響需求、程式命名、資料與圖表。[半導體四個情境](cases/semiconductor.md)示範如何把這些定義接上驗收。

## 5. 邊界必須對準真正執行動作的地方

工具呼叫可用，不代表它的所有副作用都受限。把資料、檔案、網路與寄送目的地的限制放在會真正執行它們的環境或服務，並用禁止案例驗證。

| 增補稿的說法 | 採用時補上的條件 |
| --- | --- |
| 只有 exit 2 才會阻擋 Stop | Command hook 可用 exit 2；也有合法 decision JSON 的方式，契約依事件而異。[Hooks](https://code.claude.com/docs/en/hooks#exit-code-output) |
| 沒綠就不能結束 | Stop 有中斷與持續阻擋上限等情況；交付仍需獨立的 CI／合併檢查。[Stop](https://code.claude.com/docs/en/hooks#stop) |
| deny 加 sandbox 就隔離金鑰 | Read 規則不涵蓋所有程式自行開檔；shell sandbox 有設定與工具範圍，需實測禁止存取。[Permissions](https://code.claude.com/docs/en/permissions#what-read-and-edit-rules-cover)、[Sandbox 範圍](https://code.claude.com/docs/en/sandboxing#what-runs-outside-the-sandbox) |
| 加 --max-turns 就能放心批次跑 | 它限制 print mode 的 agentic turns，不限制路徑；批次總時間、預算、結果與停止條件另管。[CLI reference](https://code.claude.com/docs/en/cli-reference#cli-flags) |

既有 [Stop wrapper](../templates/boundaries/README.md)可用來體驗通過／失敗路徑；其程式測試不代表所有 Claude session 都做過整合驗證。

## 6. 團隊導入用「過關條件」，不保證幾週完成

| 階段 | 先做什麼 | 何時進下一階段 |
| --- | --- | --- |
| 一個任務 | SPEC、既有檢查、一次證據回報 | 另一人能照步驟重現結果 |
| 一個專案 | 統一檢查入口、已知錯誤樣本、CI | 正確樣本綠，過去錯誤會紅，未驗證項目可見 |
| 一個團隊 | 把常用步驟變成 skill，把重犯變成結構 | 新人能依文件交付，不必每次口頭補充 |
| 有限自主執行 | 從少量、可逆的批次任務開始 | 完成、邊界、停止、交付與簽核五問都有答案 |

統一入口負責彙整**已列明的條件**，不能宣稱它是所有品質的唯一標準。內容正確性、未涵蓋情境與人工核准仍須列在證據回報。

## 本次取捨與來源範圍

採用：驗證實際產物、檢查的失敗樣本、共用語言、風險決定規劃、團隊導入門檻與兩組案例。流派優劣、TDD 普及程度、演講中的模型名稱與 14%／89% 數字，未因這次增補而升格為已查證事實。原稿仍保留，待查項目見[驗證紀錄](verification.md)。本次上列技術連結於 2026-11-17 做來源複查，沒有執行真實 Claude hook、STT、Mermaid 或寄信整合。
