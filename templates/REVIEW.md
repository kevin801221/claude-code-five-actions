# 獨立審查 / Independent review

交給未參與實作過程的 reviewer；提供 SPEC、diff 與驗證證據。

```text
Review this diff against the original SPEC and repository standards.
Check every acceptance criterion and the behaviors that must remain intact.
Report reproducible correctness gaps, their impact, and the missing check.
Distinguish measured observations from hypotheses. Skip style-only preferences.
Do not modify the implementation during this review.
```

| 規格條件 | 是否實作 | 證據是否涵蓋 | 缺口與影響 |
| --- | --- | --- | --- |
| 填寫原始條件 | 是／否／不明 | 足夠／不足 | 說明重現方式 |

若沒有影響正確性的發現，明確寫出審查範圍與未涵蓋處。不要為了產出建議而添加新需求。
