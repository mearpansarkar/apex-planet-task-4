import pandas as pd, numpy as np
from scipy import stats
df = pd.read_csv("cleaned_sales_with_segments.csv", parse_dates=["Order_Date"])
d25 = df[df.Order_Date < "2026-01-01"]
res = []
def ci_diff(a, b):
    d = a.mean() - b.mean(); se = np.sqrt(a.var(ddof=1)/len(a) + b.var(ddof=1)/len(b))
    dfw = se**4 / ((a.var(ddof=1)/len(a))**2/(len(a)-1) + (b.var(ddof=1)/len(b))**2/(len(b)-1))
    t = stats.t.ppf(.975, dfw); return d, d - t*se, d + t*se
def cohen_d(a, b):
    sp = np.sqrt(((len(a)-1)*a.var(ddof=1) + (len(b)-1)*b.var(ddof=1)) / (len(a)+len(b)-2)); return (a.mean()-b.mean())/sp

# H1 gender
m, f = df[df.Gender=="Male"].Total_Sales, df[df.Gender=="Female"].Total_Sales
t, p = stats.ttest_ind(m, f, equal_var=False); d, lo, hi = ci_diff(m, f)
res.append(("T1","Welch t-test","Mean order value differs between male and female customers",f"Male {m.mean():,.0f} vs Female {f.mean():,.0f}; diff {d:,.0f} (95% CI {lo:,.0f} to {hi:,.0f}); d={cohen_d(m,f):.2f}",f"t={t:.2f}",p))
# H2 Q4 vs Q3
q4, q3 = d25[d25.Order_Quarter=="Q4"].Total_Sales, d25[d25.Order_Quarter=="Q3"].Total_Sales
t, p = stats.ttest_ind(q4, q3, equal_var=False); d, lo, hi = ci_diff(q4, q3)
res.append(("T2","Welch t-test","Mean order value in Q4 differs from Q3 (2025)",f"Q4 {q4.mean():,.0f} (n={len(q4)}) vs Q3 {q3.mean():,.0f} (n={len(q3)}); diff {d:,.0f} (95% CI {lo:,.0f} to {hi:,.0f}); d={cohen_d(q4,q3):.2f}",f"t={t:.2f}",p))
# H2b order counts Q4 vs Q3 chi-square GOF (equal days: Q3 92, Q4 92)
o = np.array([len(q3), len(q4)]); chi, p2 = stats.chisquare(o)
res.append(("T3","Chi-square goodness of fit","Order count in Q3 and Q4 is the same (both quarters have 92 days)",f"Q3 {o[0]} orders vs Q4 {o[1]} orders",f"chi2={chi:.2f}",p2))
# H3 ANOVA categories
groups = [g.Total_Sales.values for _, g in df.groupby("Category")]
F, p = stats.f_oneway(*groups); H, pk = stats.kruskal(*groups)
means = df.groupby("Category").Total_Sales.mean().round(0).to_dict()
res.append(("T4","One-way ANOVA (Kruskal-Wallis check p=%.3f)"%pk,"Mean order value differs across product categories",str(means),f"F={F:.2f}",p))
# H4 chi-square segment x category
ct = pd.crosstab(df.Segment, df.Category); chi, p, dof, _ = stats.chi2_contingency(ct)
v = np.sqrt(chi/(ct.values.sum()*(min(ct.shape)-1)))
res.append(("T5","Chi-square test of independence","Category mix differs across the 4 customer segments",f"Cramer's V={v:.3f}",f"chi2={chi:.2f}, dof={dof}",p))
ct2 = pd.crosstab(df.Segment, df.Age_Group); chi, p, dof, _ = stats.chi2_contingency(ct2)
res.append(("T6","Chi-square test of independence","Age-group mix differs across the 4 customer segments",f"Cramer's V={np.sqrt(chi/(ct2.values.sum()*(min(ct2.shape)-1))):.3f}",f"chi2={chi:.2f}, dof={dof}",p))
# H5 age correlation
r, p = stats.pearsonr(df.Age, df.Total_Sales); rho, ps = stats.spearmanr(df.Age, df.Total_Sales)
res.append(("T7","Pearson correlation (Spearman check p=%.3f)"%ps,"Customer age is related to order value",f"r={r:.3f}",f"r={r:.3f}",p))
# H5b Electronics order share vs 2 of 6 products
k = int((df.Category=="Electronics").sum()); bt = stats.binomtest(k, len(df), 2/6)
ci = bt.proportion_ci(confidence_level=.95)
res.append(("T8","Binomial test","Electronics share of orders differs from 33.3% (2 of the 6 products)",f"Electronics {k}/{len(df)} = {k/len(df):.1%} (95% CI {ci.low:.1%} to {ci.high:.1%})",f"k={k}",bt.pvalue))
# H6 big spenders concentration: bootstrap CI for revenue share of Big Spenders
rng = np.random.default_rng(42); shares=[]
for _ in range(5000):
    s = df.sample(len(df), replace=True, random_state=int(rng.integers(1e9)))
    shares.append(s[s.Segment=="Big Spenders"].Total_Sales.sum()/s.Total_Sales.sum())
lo, hi = np.percentile(shares, [2.5, 97.5])
print("Big Spenders revenue share", df[df.Segment=="Big Spenders"].Total_Sales.sum()/df.Total_Sales.sum(), "bootstrap CI", lo, hi)
bl, bh = np.percentile([df.sample(len(df),replace=True,random_state=int(rng.integers(1e9))).Total_Sales.mean() for _ in range(5000)],[2.5,97.5])
print("AOV", df.Total_Sales.mean(), "95% CI", bl, bh)
out = pd.DataFrame(res, columns=["ID","Test","Hypothesis (H1 = difference/relationship exists)","Key numbers","Statistic","p_value"])
out["Significant_at_0.05"] = out.p_value < 0.05; out["Bonferroni_significant_at_0.05/8"] = out.p_value < 0.05/8
out.to_csv("hypothesis_test_results.csv", index=False)
pd.set_option("display.width", 250, "display.max_colwidth", 200)
print(out.drop(columns="Hypothesis (H1 = difference/relationship exists)").to_string(index=False))
