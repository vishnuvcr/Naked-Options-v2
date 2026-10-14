#!/usr/bin/env python3
"""Render OPT-BUY-1.0 sanitized results into a manuscript and SVG plots."""
from __future__ import annotations
import html
import json
import math
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "reports" / "option_validation"
OUT = ROOT / "research" / "option-validation"
FIG = OUT / "figures"


def fmt(v, digits=2):
    try:
        x = float(v)
        return f"{x:,.{digits}f}" if math.isfinite(x) else "NA"
    except (TypeError, ValueError):
        return "NA"


def pct(v, digits=2):
    try:
        x = float(v)
        return f"{100*x:.{digits}f}%" if math.isfinite(x) else "NA"
    except (TypeError, ValueError):
        return "NA"


def esc(v):
    return html.escape(str(v), quote=True)


def placeholder(path, title, message):
    path.write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="450" viewBox="0 0 1100 450">'
        '<rect width="100%" height="100%" fill="white"/>'
        f'<text x="550" y="65" text-anchor="middle" font-family="Arial" font-size="26" font-weight="bold">{esc(title)}</text>'
        f'<text x="550" y="230" text-anchor="middle" font-family="Arial" font-size="18">{esc(message)}</text></svg>',
        encoding="utf-8",
    )


def pnl_chart(summary, performance, path):
    primary = summary.get("primary_candidates", [])
    if not primary:
        placeholder(path, "Primary net P&L comparison", "No primary comparison rows available")
        return
    rows = []
    for r in primary:
        base = performance[
            (performance.horizon == int(r["horizon"])) &
            (performance.structure == str(r["structure"])) &
            (performance["mode"] == "always_buy") &
            (performance.slippage_bps_per_side == 50) &
            (performance.brokerage_per_order_rupees == 10)
        ]
        base_mean = float(base.iloc[0]["mean_net_pnl_rupees_daily"]) if len(base) else float(r.get("benchmark_mean_net_daily_pnl_rupees", 0))
        base_lo = float(base.iloc[0].get("ci95_net_pnl_rupees_daily_low", float("nan"))) if len(base) else float("nan")
        base_hi = float(base.iloc[0].get("ci95_net_pnl_rupees_daily_high", float("nan"))) if len(base) else float("nan")
        vals = [
            float(r.get("candidate_mean_net_daily_pnl_rupees", 0)),
            float(r.get("candidate_pnl_ci95_low_rupees", float("nan"))),
            float(r.get("candidate_pnl_ci95_high_rupees", float("nan"))),
            base_mean, base_lo, base_hi
        ]
        rows.append((r, vals))
    all_vals = [0.0]
    for _, v in rows:
        all_vals.extend(x for x in v if math.isfinite(float(x)))
    ymin, ymax = min(all_vals), max(all_vals)
    span = max(ymax-ymin, 1.0)
    ymin -= span*0.12
    ymax += span*0.12
    W, H = 1150, 650
    L, R, T, B = 100, 35, 80, 155
    PH = H-T-B
    PW = W-L-R
    def y(v): return T + (ymax-float(v))/(ymax-ymin)*PH
    zero = y(0)
    els = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="575" y="32" text-anchor="middle" font-family="Arial" font-size="25" font-weight="bold">Alert-filtered option buying vs always-buy</text>',
        '<text x="575" y="56" text-anchor="middle" font-family="Arial" font-size="14">Daily net P&amp;L per one-lot-proxy slot; Rs 10/order; 50 bps adverse slippage per premium side</text>',
    ]
    for t in range(6):
        v = ymax-(ymax-ymin)*t/5
        yy = y(v)
        els.append(f'<line x1="{L}" y1="{yy:.1f}" x2="{W-R}" y2="{yy:.1f}" stroke="#dddddd"/>')
        els.append(f'<text x="{L-12}" y="{yy+4:.1f}" text-anchor="end" font-family="Arial" font-size="13">{fmt(v,0)}</text>')
    els.append(f'<line x1="{L}" y1="{zero:.1f}" x2="{W-R}" y2="{zero:.1f}" stroke="#444" stroke-width="1.5"/>')
    groupw = PW/max(len(rows),1)
    bw = min(42, groupw*.22)
    for i,(r,v) in enumerate(rows):
        center = L + (i+.5)*groupw
        series = [
            (v[0],v[1],v[2],"#2864a5"),
            (v[3],v[4],v[5],"#ed8a24")
        ]
        for j,(mean,lo,hi,color) in enumerate(series):
            cx = center + (j-.5)*(bw+14)
            ym = y(mean)
            els.append(f'<rect x="{cx-bw/2:.1f}" y="{min(zero,ym):.1f}" width="{bw:.1f}" height="{max(abs(zero-ym),1):.1f}" fill="{color}" rx="2"/>')
            if math.isfinite(lo) and math.isfinite(hi):
                els.append(f'<line x1="{cx:.1f}" y1="{y(lo):.1f}" x2="{cx:.1f}" y2="{y(hi):.1f}" stroke="#222" stroke-width="2"/>')
                els.append(f'<line x1="{cx-7:.1f}" y1="{y(lo):.1f}" x2="{cx+7:.1f}" y2="{y(lo):.1f}" stroke="#222" stroke-width="2"/>')
                els.append(f'<line x1="{cx-7:.1f}" y1="{y(hi):.1f}" x2="{cx+7:.1f}" y2="{y(hi):.1f}" stroke="#222" stroke-width="2"/>')
            els.append(f'<text x="{cx:.1f}" y="{ym+(16 if mean<0 else -8):.1f}" text-anchor="middle" font-family="Arial" font-size="11">{fmt(mean,0)}</text>')
        lab = f'{int(r["horizon"])}-session {r["structure"]}'
        els.append(f'<text x="{center:.1f}" y="{H-B+28}" text-anchor="middle" font-family="Arial" font-size="12">{esc(lab)}</text>')
    legendy = H-55
    els.extend([
        f'<rect x="{W/2-190}" y="{legendy-12}" width="15" height="15" fill="#2864a5"/>',
        f'<text x="{W/2-168}" y="{legendy}" font-family="Arial" font-size="13">Alert-filtered</text>',
        f'<rect x="{W/2+20}" y="{legendy-12}" width="15" height="15" fill="#ed8a24"/>',
        f'<text x="{W/2+42}" y="{legendy}" font-family="Arial" font-size="13">Always-buy</text>',
        f'<text x="{L}" y="{H-16}" font-family="Arial" font-size="11" fill="#555">Whiskers represent 95% circular moving-block bootstrap intervals.</text>',
        '</svg>'
    ])
    path.write_text("\n".join(els)+"\n",encoding="utf-8")


def slippage_chart(performance,path):
    if performance.empty or "mean_net_pnl_rupees_daily" not in performance.columns:
        placeholder(path,"Slippage sensitivity","Required P&L sensitivity rows are unavailable")
        return
    d=performance[(performance["mode"]=="model_filtered")&(performance.brokerage_per_order_rupees==10)].copy()
    if d.empty:
        placeholder(path,"Slippage sensitivity","No model-filtered sensitivity rows available")
        return
    hs=sorted(d.horizon.dropna().astype(int).unique())
    sts=sorted(d.structure.dropna().astype(str).unique())
    slips=sorted(d.slippage_bps_per_side.dropna().astype(int).unique())
    colors=["#2864a5","#d9534f","#32965d","#8258a5"]
    vals=pd.to_numeric(d.mean_net_pnl_rupees_daily,errors="coerce").dropna().tolist()+[0.0]
    ymin,ymax=min(vals),max(vals); span=max(ymax-ymin,1.0); ymin-=span*.12; ymax+=span*.12
    W,H=1150,590; L,R,T,B=100,40,82,120; PW=W-L-R; PH=H-T-B
    def x(i): return L+(i/max(1,len(slips)-1))*PW
    def y(v): return T+(ymax-float(v))/(ymax-ymin)*PH
    els=[
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="575" y="35" text-anchor="middle" font-family="Arial" font-size="24" font-weight="bold">Slippage sensitivity: model-filtered strategy</text>',
        '<text x="575" y="59" text-anchor="middle" font-family="Arial" font-size="14">Mean daily net P&amp;L (Rs per one-lot-proxy slot); brokerage Rs 10/order</text>',
    ]
    for i in range(6):
        v=ymax-(ymax-ymin)*i/5; yy=y(v)
        els.append(f'<line x1="{L}" y1="{yy:.1f}" x2="{W-R}" y2="{yy:.1f}" stroke="#ddd"/>')
        els.append(f'<text x="{L-12}" y="{yy+4:.1f}" text-anchor="end" font-family="Arial" font-size="12">{fmt(v,0)}</text>')
    els.append(f'<line x1="{L}" y1="{y(0):.1f}" x2="{W-R}" y2="{y(0):.1f}" stroke="#444" stroke-width="1.5"/>')
    for i,s in enumerate(slips):
        els.append(f'<text x="{x(i):.1f}" y="{H-B+25}" text-anchor="middle" font-family="Arial" font-size="13">{s}</text>')
    series=[]
    for h in hs:
        for st in sts:
            g=d[(d.horizon==h)&(d.structure==st)].sort_values("slippage_bps_per_side")
            series.append((f"{h}-session {st}",g,colors[len(series)%len(colors)]))
    for label,g,color in series:
        pts=[]
        for _,r in g.iterrows():
            try:
                v=float(r.mean_net_pnl_rupees_daily)
                if math.isfinite(v): pts.append((x(slips.index(int(r.slippage_bps_per_side)),),y(v),v))
            except (ValueError,TypeError): pass
        if pts:
            els.append('<polyline fill="none" stroke="{}" stroke-width="3" points="{}"/>'.format(color," ".join(f"{a:.1f},{b:.1f}" for a,b,_ in pts)))
            for a,b,v in pts:
                els.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="4" fill="{color}"/>')
                els.append(f'<text x="{a:.1f}" y="{b+15:.1f}" text-anchor="middle" font-family="Arial" font-size="10" fill="{color}">{fmt(v,0)}</text>')
    for i,(label,g,color) in enumerate(series):
        col=i%2; row=i//2; xx=L+col*400; yy=H-45+row*18
        els.append(f'<line x1="{xx}" y1="{yy-4}" x2="{xx+24}" y2="{yy-4}" stroke="{color}" stroke-width="3"/>')
        els.append(f'<text x="{xx+32}" y="{yy}" font-family="Arial" font-size="12">{esc(label)}</text>')
    els.append(f'<text x="575" y="{H-11}" text-anchor="middle" font-family="Arial" font-size="12">Adverse slippage per premium side (basis points)</text>')
    els.append('</svg>')
    path.write_text("\n".join(els)+"\n",encoding="utf-8")


def manuscript(summary, acquisition, quote, primary, performance):
    status=summary.get("overall_status","UNKNOWN")
    cls=summary.get("classifier",{})
    cut=cls.get("cut_date","NA")
    horizons=cls.get("horizons",{})
    cov=quote.get("eligible_date_coverage_by_structure",{})
    conflicts=int(quote.get("duplicate_conflict_groups",0))
    duplicate_groups=int(quote.get("duplicate_groups",0))
    conflict_rate=conflicts/max(duplicate_groups,1)
    lines=[
        "# Do volatility-expansion alerts make intraday NIFTY option buying profitable?",
        "",
        "**Study ID:** OPT-BUY-1.0. **Scope:** historical screening only; NIFTY-PRED-1.0 remains closed. **Decision:** " + str(status),
        "",
        "## Abstract",
        "",
        "This study evaluates whether a technical Logistic Regression classifier for 5- and 20-session volatility expansion can filter same-session long NIFTY option purchases. Each signal is available only after the preceding underlying-market close. On the next session, the candidate enters at the 09:20 five-minute bar open and exits at the 15:25 five-minute bar close, matching the same numeric strike. It compares an alert-filtered two-leg long straddle or one-step out-of-the-money strangle with buying that same structure on every eligible date. Brokerage, statutory/exchange charges and 0/25/50/100 basis-point adverse-slippage scenarios are included.",
        "",
        f"The underlying series contains {int(cls.get('data_rows',0)):,} daily rows from {cls.get('data_first_date','NA')} to {cls.get('data_last_date','NA')}; the chronological development/test cutoff is {cut}. The option data gate is {'PASS' if summary.get('data_gate_pass') else 'FAIL'}: straddle coverage is {pct(cov.get('straddle',0))}; strangle coverage is {pct(cov.get('strangle',0))}; conflicting quote groups are {pct(conflict_rate)} of duplicate groups. The prespecified limits are at least 80% coverage for each structure and no more than 1% conflict rate. When those gates fail, the outcome is inconclusive regardless of small comparison p-values. No live strategy is approved.",
        "",
        "## 1. Research question, aim and objectives",
        "",
        "**Question:** Do 5- or 20-session volatility-expansion alerts yield positive, robust net P&L for intraday long NIFTY options and improve results versus unconditional buying of the same structure?",
        "",
        "**Aim:** test the economic value of an already-developed volatility-expansion alert as an option-buying filter, without developing live execution software.",
        "",
        "**Objectives:** reconstruct alerts with purged chronological validation; source and validate historical rolling option quotes; match numeric entry/exit strikes; calculate statutory/broker/cost/slippage effects; compare alert filtering with always-buy using paired daily rupee P&L; apply fixed coverage, profitability, robustness and independent-review gates.",
        "",
        "## 2. Literature and rationale",
        "",
        "A forecast of volatility expansion is not automatically a forecast of positive long-option returns. Implied volatility prices expected movement as well as risk premia and liquidity; the buyer must overcome time decay and transaction costs. Bakshi and Kapadia documented negative average delta-hedged S&P 500 option gains consistent with a negative volatility risk premium; that design differs from these unhedged intraday positions but illustrates that a volatility forecast alone is insufficient (Review of Financial Studies, 2003; https://doi.org/10.1093/rfs/hhg002). Cao and Han related cross-sectional option returns to underlying volatility and frictions for single-stock options (Journal of Financial Economics, 2013; https://doi.org/10.1016/j.jfineco.2012.11.010). Cao et al. document a relation between volatility uncertainty and equity option returns (Quarterly Journal of Finance, 2023; https://doi.org/10.1142/s2010139223500052). These are general motivation, not replications of a NIFTY intraday strategy.",
        "",
        "DhanHQ’s expired-options endpoint provides rolling ATM-relative 5-minute option bars for up to five years with up to 30 calendar days per request, but not a historical bid/ask feed (https://dhanhq.co/docs/v2/expired-options-data/).",
        "",
        "## 3. Data and methodology",
        "",
        f"- **Underlying:** {int(cls.get('data_rows',0)):,} rows, {cls.get('data_first_date','NA')} to {cls.get('data_last_date','NA')}; 80/20 chronological split at {cut}.",
        f"- **Classifier:** standardized technical Logistic Regression with median imputation, class weighting, C=0.1; thresholds are 75th-percentile of purged, development-only four-fold OOF probabilities. Five-session threshold {fmt(horizons.get('5',{}).get('threshold'),4)}; 20-session threshold {fmt(horizons.get('20',{}).get('threshold'),4)}.",
        f"- **Option bars:** {int(quote.get('raw_rows',0)):,} raw rows before cleaning; {int(quote.get('usable_rows',0)):,} usable rows. Request mode MONTH, expiryCode=1; rolling offsets ATM−3 through ATM+3 for calls and puts.",
        "- **Entry/exit:** 09:20 five-minute bar open and 15:25 bar close on the next session; selected numeric strike must match both legs at entry and exact same strike at exit. Missing rows are skipped, never forward-filled. The test only enters and exits in one session.",
        "- **Structures:** long ATM straddle; long one-step OTM strangle must use CALL relative offset +1 and PUT offset −1 at entry, and both actual numeric strikes are followed to exit.",
        "- **Primary outcome:** daily net rupee P&L for one lot-size-proxy slot. Alert-filtered candidate is at zero on non-alert dates; always-buy purchases the same structure on every eligible date. Thus the paired comparison uses a common daily P&L basis, not a percentage denominator that varies by trade.",
        "- **Costs:** ₹10 per executed unique order baseline and ₹20 sensitivity; a complete two-leg round trip counts four orders; option-sale STT 0.10% through 2026-03-31 and 0.15% from 2026-04-01; stamp duty 0.003% on buyer turnover; SEBI fee ₹10/crore, official NSE exchange charge approximation, and 18% GST.",
        "- **Slippage:** each premium entry is worsened and each premium exit reduced by 0, 25, 50 or 100 bps per side. This is a stress approximation because historical bid/ask is unavailable.",
        "- **Statistics:** 2,000 circular moving-block bootstrap replicates; block length equals the forecast horizon; paired candidate-minus-always-buy daily P&L comparison; Holm correction across four primary comparisons; chronological-half and 100-bps stress gates.",
        "",
        "## 4. Frozen acceptance gates",
        "",
        "The data-quality gate requires an acquisition manifest without failed windows, at least 80% eligible fixed-strike dates for both structures, and a conflicting-duplicate rate at or below 1% after conflicts are discarded. For a candidate to pass it must also have at least 100 alert trades, positive mean daily net P&L with its 95% block-bootstrap lower bound above zero, positive result at 100 bps slippage, positive daily P&L in both chronological halves, and Holm-adjusted outperformance versus always-buy. The data gate cannot be relaxed because a p-value is small.",
        "",
        "## 5. Results",
        "",
        f"**Overall status: {status}. Data gate: {'PASS' if summary.get('data_gate_pass') else 'FAIL'}.**",
        "",
        "| Horizon | Structure | Alert trades | Filtered net P&L/day (₹) | 95% block CI (₹) | Always-buy P&L/day (₹) | Paired difference/day (₹) | Paired 95% CI (₹) | Holm p | 100 bps positive? | Both halves positive? | Candidate gate |",
        "|---:|---|---:|---:|---|---:|---:|---|---:|---|---|---|"
    ]
    for r in summary.get("primary_candidates",[]):
        lines.append("| {} | {} | {} | {} | {} to {} | {} | {} | {} to {} | {} | {} | {} | {} |".format(
            r.get("horizon"),r.get("structure"),r.get("n_alert_trades"),
            fmt(r.get("candidate_mean_net_daily_pnl_rupees")),
            fmt(r.get("candidate_pnl_ci95_low_rupees")),fmt(r.get("candidate_pnl_ci95_high_rupees")),
            fmt(r.get("benchmark_mean_net_daily_pnl_rupees")),fmt(r.get("paired_mean_difference_rupees")),
            fmt(r.get("paired_ci95_pnl_low_rupees")),fmt(r.get("paired_ci95_pnl_high_rupees")),
            fmt(r.get("p_holm"),4),bool(r.get("positive_at_100bps")),
            bool(r.get("both_halves_positive")),bool(r.get("positive_candidate_gate"))))
    lines += [
        "",
        "![Primary net P&L comparison](figures/net_pnl_comparison.svg)",
        "",
        "![Slippage stress test](figures/slippage_sensitivity.svg)",
        "",
        "A positive paired difference against an always-buy baseline can mean the filter reduces losses relative to an even worse baseline; it is not proof of profitable option buying. Negative candidate mean P&L or a negative confidence interval lower/upper range is a rejection of the current candidate, and failure of data coverage/conflict gates makes the statistical conclusion inconclusive.",
        "",
        "## 6. Discussion",
        "",
        "The key distinction is between forecasting higher realized volatility and identifying an option premium that will appreciate enough to cover implied volatility, decay and execution costs. The label spans 5 or 20 sessions, but the trade is closed on the first alerted session’s close. That deliberate mismatch means this is a limited test of immediate monetization, not a direct position held for the classifier’s full target horizon. The rolling contract source also lacks historical bid/ask and stable expiry-specific contract identity, so slippage and lot-sizing remain proxies.",
        "",
        "## 7. Strengths",
        "",
        "- Chronological held-out origins with a development-only OOF threshold and horizon purge.",
        "- Same-session actual strike matching; missing quotes are skipped rather than filled or substituted.",
        "- Brokerage, statutory/exchange charges, slippage scenarios, block confidence intervals and Holm correction are prespecified.",
        "- An independent audit recomputes ledger arithmetic, primary outcomes, bootstrap intervals and multiple-comparison adjustment from the sanitized ledger.",
        "",
        "## 8. Limitations",
        "",
        "- If coverage is below 80% or conflict rate above 1%, no strategy inference is accepted even if a comparison p-value is small.",
        "- Rolling options are not the same as stable, expiry-identified option contracts across multiple days; overnight/multi-day P&L is not tested.",
        "- OHLC fills do not equal historical executable bid/ask; the slippage stress may understate tail events.",
        "- Lot size uses a trade-date proxy rather than a contract-master reconstruction for the exact expiry.",
        "- Only one chronological test window is analyzed; there is no prospective paper-trading period.",
        "",
        "## 9. Conclusion",
        "",
        f"**{status}.** No option-buying strategy is validated or approved. If the current candidates have negative net daily P&L, a significant paired improvement only establishes reduced losses versus the unconditional baseline; it does not establish a profitable edge. The next bounded run enforces the exact one-step OTM strangle and reruns the quality gates without changing thresholds or relaxing criteria.",
        "",
        "## 10. Future direction",
        "",
        "Research directions after this bounded study: acquire verified expiry/contract/lot-size and historical bid/ask data; align the target horizon with the holding period using a one-session intraday volatility-expansion label; test implied-versus-realized volatility pricing and event costs; require multiple walk-forward test periods and a locked untouched final holdout; then consider a prospective paper-trading period only after a separate independent test passes.",
        "",
        "## Appendix A — transaction accounting",
        "",
        "- Gross P&L = (combined exit premium points − combined entry premium points) × lot-size proxy.",
        "- Slippage cost = (entry premium + exit premium) × (bps/10,000) × lot-size proxy.",
        "- Net P&L = gross P&L − slippage − brokerage − STT − stamp duty − SEBI fee − exchange charges − GST.",
        "- Two legs opened and closed mean four executed orders per completed trade.",
        "",
        "## Appendix B — references",
        "",
        "1. DhanHQ, Expired Options Data API v2: https://dhanhq.co/docs/v2/expired-options-data/",
        "2. NSE, STT schedule for equity derivatives: https://www.nseindia.com/static/products-services/equity-derivatives-securities-transaction-tax",
        "3. NSE Circular (equity options exchange charges from 2026-03-01): https://nsearchives.nseindia.com/content/circulars/FA73061.pdf",
        "4. NSE, SEBI turnover fees, stamp duty, STT and other levies: https://www.nseindia.com/static/invest/first-time-investor-sebi-turnover-fees-stt-other-levies",
        "5. Paytm Money, F&O brokerage FAQ: https://www.paytmmoney.com/stocks/customer/fno-faq/onboarding-and-kyc/account-segment-activation/how-to-activate-fo-from-mobile-app-web",
        "6. Bakshi, G. & Kapadia, N. (2003). Delta-Hedged Gains and the Negative Market Volatility Risk Premium. Review of Financial Studies 16(2), 527–566. https://doi.org/10.1093/rfs/hhg002",
        "7. Cao, J. & Han, B. (2013). Cross section of option returns and idiosyncratic stock volatility. Journal of Financial Economics 108(1), 231–249. https://doi.org/10.1016/j.jfineco.2012.11.010",
        "8. Cao, J. J., Vasquez, A., Xiao, X. & Zhan, X. (2023). Why Does Volatility Uncertainty Predict Equity Option Returns? The Quarterly Journal of Finance 13(1), 2350005. https://doi.org/10.1142/s2010139223500052",
        "",
        "## Appendix C — reproducibility files",
        "",
        "- Acquisition summary: ../../reports/option_validation/acquisition_summary.json",
        "- Quote quality: ../../reports/option_validation/quote_quality.json",
        "- Results: ../../reports/option_validation/results_summary.json",
        "- Primary comparisons: ../../reports/option_validation/primary_comparisons.csv",
        "- Cost/slippage matrix: ../../reports/option_validation/performance.csv",
        "- Sanitized trade ledger: ../../reports/option_validation/trade_ledger.csv",
        "- Restricted raw quote responses are stored only in the Actions cache and are not published.",
        "",
        "**Independent tester handoff:** recompute quote coverage/conflict counts, fixed-strike matching, P&L/cost arithmetic, bootstrap intervals and Holm adjustment from raw/cached inputs and the sanitized ledger. Block if any gate fails."
    ]
    (OUT/"MANUSCRIPT.md").write_text("\n".join(lines)+"\n",encoding="utf-8")


def main():
    FIG.mkdir(parents=True,exist_ok=True)
    summary=json.loads((REPORT/"results_summary.json").read_text(encoding="utf-8"))
    acquisition=json.loads((REPORT/"acquisition_summary.json").read_text(encoding="utf-8"))
    quote=json.loads((REPORT/"quote_quality.json").read_text(encoding="utf-8"))
    primary=pd.read_csv(REPORT/"primary_comparisons.csv")
    performance=pd.read_csv(REPORT/"performance.csv")
    pnl_chart(summary,performance,FIG/"net_pnl_comparison.svg")
    slippage_chart(performance,FIG/"slippage_sensitivity.svg")
    manuscript(summary,acquisition,quote,primary,performance)
    print(json.dumps({
        "manuscript":"research/option-validation/MANUSCRIPT.md",
        "figures":["research/option-validation/figures/net_pnl_comparison.svg","research/option-validation/figures/slippage_sensitivity.svg"],
        "overall_status":summary.get("overall_status"),
        "data_gate_pass":summary.get("data_gate_pass")
    },indent=2))


if __name__ == "__main__":
    main()
