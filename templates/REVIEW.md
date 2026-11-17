# 獨立審查 / Independent review

交給未參與實作過程的 reviewer；提供 SPEC、diff 與驗證證據。

```text
Review this diff against the original SPEC and repository standards.
Check every acceptance criterion and the behaviors that must remain intact.
Check that each important assertion rejects a known bad sample for the expected reason.
Check that evidence belongs to this run and that skipped or unmeasurable items are visible.
Report reproducible correctness gaps, their impact, and the missing check.
Distinguish measured observations from hypotheses. Skip style-only preferences.
Do not modify the implementation during this review.
```

| 規格條件 | 是否實作 | 證據是否涵蓋 | 缺口與影響 |
| --- | --- | --- | --- |
| 填寫原始條件 | 是／否／不明 | 足夠／不足 | 說明重現方式 |

產物型任務另附[驗收矩陣](ARTIFACT-CHECKS.md)。例如：缺少待辦但標題齊全的摘要，應被拒絕；查到舊信不能當成本次寄送成功。檢查不支援的格式或形狀，不能略過後宣稱已驗證。

若沒有影響正確性的發現，明確寫出審查範圍與未涵蓋處。不要為了產出建議而添加新需求。
