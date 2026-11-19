# Task 4: Hypothesis Testing Summary

**Data:** cleaned sales dataset (1,000 orders). Significance level 0.05; with 8 tests, a stricter Bonferroni cut-off of 0.05/8 = 0.006 is also reported.
**Note:** the data has no A/B experiment, so I tested the claims made in Tasks 2 and 3 instead.

## Tests
| ID | Hypothesis (H1) | Test | Result | p-value | Significant? |
|---|---|---|---|---|---|
| T1 | Mean order value differs between male and female customers | Welch t-test | Male 141,807 vs Female 136,883; difference 4,924 (95% CI -9,232 to 19,080); Cohen's d = 0.04 | 0.495 | No |
| T2 | Mean order value in Q4 differs from Q3 (2025) | Welch t-test | Q4 144,511 vs Q3 128,163; difference 16,349 (95% CI -3,570 to 36,267); d = 0.14 | 0.107 | No |
| T3 | Order counts differ between Q3 and Q4 (both 92 days) | Chi-square goodness of fit | Q3 237 vs Q4 259 orders; chi2 = 0.98 | 0.323 | No |
| T4 | Mean order value differs across the 5 categories | One-way ANOVA (Kruskal-Wallis p = 0.735) | F = 0.72; category means range 127K to 145K | 0.580 | No |
| T5 | Category mix differs across the 4 segments | Chi-square independence | chi2 = 13.86, dof = 12; Cramer's V = 0.068 | 0.310 | No |
| T6 | Age-group mix differs across the 4 segments | Chi-square independence | chi2 = 15.51, dof = 12; Cramer's V = 0.072 | 0.215 | No |
| T7 | Age is related to order value | Pearson correlation (Spearman p = 0.854) | r = 0.001 | 0.967 | No |
| T8 | Electronics share of orders differs from 33.3% (2 of 6 products) | Binomial test | 354 of 1,000 = 35.4% (95% CI 32.4% to 38.5%) | 0.169 | No |

For every test, H0 is "no difference / no relationship". **None of the eight tests rejects H0**, with or without the Bonferroni correction.

## Confidence intervals (bootstrap, 5,000 resamples)
- Average order value: 139,399 (95% CI 132,330 to 146,575).
- Revenue share of Big Spenders (segment from Task 3): 52.5% (95% CI 48.6% to 56.4%). The lower bound is close to half of revenue, so the concentration finding is solid. Note the segment is defined by price and quantity, so this measures how concentrated revenue is, not a discovered group.

## Business conclusions
1. **The Q4 lead is not proven.** Q4 earned more than Q3 (37.4M vs 30.4M) and had a higher average order value, but the gaps in order count (p = 0.32) and order value (p = 0.11) are both within normal random variation. Do not plan budgets around "Q4 is stronger" without more data.
2. **Electronics' 36% revenue share does not show customer preference.** Its order share (35.4%) is statistically the same as the 33.3% expected from having 2 of 6 products.
3. **Gender, age and category do not predict order value** (T1, T4, T7). Targeting on these would not help.
4. **Segments are behavioural.** Category and age mix are statistically similar across segments (T5, T6), so target by basket size and price tier.
5. **Revenue concentration is real:** Big Spenders bring in roughly half of revenue (CI 48.6% to 56.4%).

## Limitations
- A non-significant result means "no evidence of a difference", not "no difference". For example, the gender CI still allows a gap of up to about 19K (14%), so the sample is not large enough to rule out moderate differences.
- To detect a 10% difference in average order value between two groups at 80% power, an A/B test would need roughly 1,000 orders per group.
- Orders are treated as independent, but some Customer_IDs are reused (see Task 1).
- Unit prices do not differ by product, so the data appears synthetic.
