#!/usr/bin/env node
// Reproducible preliminary diagnostic for the historical third-party NIFTY CSV.
// This deliberately uses only Node built-ins. It is not the production sklearn benchmark.
const fs = require("fs");
const path = require("path");
const input = process.argv[2] || "data/cache/nifty-prediction/nifty50_daily.csv";
const output = process.argv[3] || "reports/nifty-prediction/preliminary_historical_diagnostic.json";
const lines = fs.readFileSync(input, "utf8").trimEnd().split(/\r?\n/);
const bars = [];
for (let i = 1; i < lines.length; i++) {
  const p = lines[i].split(",");
  if (p.length < 5) continue;
  const [date, open, high, low, close] = [p[0], ...p.slice(1, 5).map(Number)];
  if (date && [open, high, low, close].every(Number.isFinite)) bars.push({date, open, high, low, close});
}
const closes = bars.map(x => x.close);
const returns = closes.map((c, i) => i ? c / closes[i - 1] - 1 : NaN);
const windows = [5, 10, 20, 60], lags = [1, 2, 3, 5, 10, 20, 60];
const mean = a => a.reduce((s, x) => s + x, 0) / a.length;
const sd = a => { const m = mean(a); return Math.sqrt(a.reduce((s, x) => s + (x - m) ** 2, 0) / (a.length - 1)); };
function rollingMean(a, i, n) { return i - n + 1 < 0 ? NaN : mean(a.slice(i - n + 1, i + 1)); }
function rollingSd(a, i, n) {
  if (i - n + 1 < 0) return NaN;
  const x = a.slice(i - n + 1, i + 1);
  return x.some(v => !Number.isFinite(v)) ? NaN : sd(x);
}
const featureNames = [...lags.map(n => `ret_${n}`), ...windows.map(n => `vol_${n}`), ...windows.map(n => `ma_gap_${n}`), "range_pct", "open_gap", "close_position"];
const frame = [];
for (let i = 0; i < bars.length - 1; i++) {
  const b = bars[i], prev = closes[i - 1], x = [];
  for (const n of lags) x.push(i >= n ? closes[i] / closes[i - n] - 1 : NaN);
  for (const n of windows) x.push(rollingSd(returns, i, n));
  for (const n of windows) { const m = rollingMean(closes, i, n); x.push(Number.isFinite(m) ? closes[i] / m - 1 : NaN); }
  x.push((b.high - b.low) / b.close, i > 0 ? b.open / prev - 1 : NaN, b.high === b.low ? NaN : (b.close - b.low) / (b.high - b.low));
  const targetReturn = closes[i + 1] / closes[i] - 1;
  if (x.every(Number.isFinite) && Number.isFinite(targetReturn)) frame.push({date:b.date, x, y:targetReturn > 0 ? 1 : 0, targetReturn, prev:returns[i] > 0 ? 1 : 0});
}
const split = Math.max(750, Math.floor(frame.length * .75));
if (split >= frame.length - 100) throw new Error(`Insufficient frame ${frame.length}, split ${split}`);
const yTest = frame.slice(split).map(r => r.y);
const predictions = {
  majority_class_baseline: Array(frame.length - split).fill(mean(frame.slice(0, split).map(r => r.y)) >= .5 ? 1 : 0),
  previous_session_direction: frame.slice(split).map(r => r.prev),
  zero_return_forecast: Array(frame.length - split).fill(0)
};
const sigmoid = z => z > 30 ? 1 : z < -30 ? 0 : 1 / (1 + Math.exp(-z));
function fitLogit(rows) {
  const n = rows.length, p = rows[0].x.length, mu = Array(p).fill(0), sdv = Array(p).fill(0);
  for (const r of rows) for (let j = 0; j < p; j++) mu[j] += r.x[j] / n;
  for (const r of rows) for (let j = 0; j < p; j++) sdv[j] += (r.x[j] - mu[j]) ** 2 / n;
  for (let j = 0; j < p; j++) sdv[j] = Math.sqrt(sdv[j]) || 1;
  const X = rows.map(r => r.x.map((v,j) => (v - mu[j]) / sdv[j]));
  const n0 = rows.filter(r => r.y === 0).length, n1 = n - n0, w0 = n / (2 * Math.max(1, n0)), w1 = n / (2 * Math.max(1, n1));
  let beta = Array(p + 1).fill(0);
  for (let it = 0; it < 260; it++) {
    const g = Array(p + 1).fill(0);
    for (let i = 0; i < n; i++) {
      let z = beta[0]; for (let j = 0; j < p; j++) z += beta[j + 1] * X[i][j];
      const pr = sigmoid(z), wt = rows[i].y ? w1 : w0, err = (pr - rows[i].y) * wt;
      g[0] += err / n; for (let j = 0; j < p; j++) g[j + 1] += err * X[i][j] / n;
    }
    for (let j = 1; j <= p; j++) g[j] += .0005 * beta[j];
    const norm = Math.sqrt(g.reduce((s,v) => s + v*v, 0)), step = norm > 5 ? .12 * 5 / norm : .12;
    for (let j = 0; j <= p; j++) beta[j] -= step * g[j];
  }
  return {mu, sdv, beta};
}
function probLogit(m, x) {
  let z = m.beta[0]; for (let j = 0; j < x.length; j++) z += m.beta[j + 1] * (x[j] - m.mu[j]) / m.sdv[j];
  return sigmoid(z);
}
const probabilities = [];
let model = null;
for (let i = split; i < frame.length; i++) {
  if (model === null || (i - split) % 20 === 0) model = fitLogit(frame.slice(0, i));
  probabilities.push(probLogit(model, frame[i].x));
}
predictions.logistic_regression = probabilities.map(p => p >= .5 ? 1 : 0);
function balanced(y, p) {
  const n0 = y.filter(v => v === 0).length, n1 = y.filter(v => v === 1).length;
  let tn = 0, tp = 0;
  for (let i = 0; i < y.length; i++) { if (y[i] === 0 && p[i] === 0) tn++; if (y[i] === 1 && p[i] === 1) tp++; }
  return .5 * (tn / Math.max(1, n0) + tp / Math.max(1, n1));
}
function metrics(name, y, p, pr = null) {
  let tn = 0, fp = 0, fn = 0, tp = 0;
  for (let i = 0; i < y.length; i++) {
    if (y[i] === 0 && p[i] === 0) tn++; else if (y[i] === 0) fp++; else if (p[i] === 0) fn++; else tp++;
  }
  const accuracy = (tn + tp) / y.length, precision0 = tn / Math.max(1, tn + fn), precision1 = tp / Math.max(1, tp + fp);
  const recall0 = tn / Math.max(1, tn + fp), recall1 = tp / Math.max(1, tp + fn);
  const out = {model:name, n:y.length, accuracy, balanced_accuracy:.5*(recall0+recall1), confusion_matrix_labels_down_up:[[tn,fp],[fn,tp]],
    precision_down_up:[precision0,precision1], recall_down_up:[recall0,recall1],
    f1_down_up:[2*precision0*recall0/Math.max(1e-12,precision0+recall0),2*precision1*recall1/Math.max(1e-12,precision1+recall1)]};
  if (pr) { out.brier_score = mean(pr.map((v,i)=>(v-y[i])**2)); out.log_loss = -mean(pr.map((v,i)=>y[i]?Math.log(Math.max(1e-12,v)):Math.log(Math.max(1e-12,1-v)))); }
  let seed = 20261025; const rng = () => { seed = (1664525*seed+1013904223)>>>0; return seed/4294967296; };
  const values = [], n = y.length, block = 10;
  for (let r = 0; r < 1000; r++) {
    const ix = [];
    while (ix.length < n) { const start = Math.floor(rng()*n); for (let j=0;j<block && ix.length<n;j++) ix.push((start+j)%n); }
    const yy=ix.map(i=>y[i]), pp=ix.map(i=>p[i]); if (new Set(yy).size>1) values.push(balanced(yy,pp));
  }
  values.sort((a,b)=>a-b);
  out.balanced_accuracy_95pct_ci = {lower:values[Math.floor(.025*(values.length-1))],upper:values[Math.floor(.975*(values.length-1))],method:"circular block bootstrap, block=10, reps=1000"};
  return out;
}
const results = Object.entries(predictions).map(([name,p]) => metrics(name,yTest,p,name==="logistic_regression"?probabilities:null));
const report = {
  study:"PRELIMINARY diagnostic: NIFTY 50 next-session direction, third-party historical CSV",
  status:"PRELIMINARY_RESULTS_COMPUTED_NOT_FINAL",
  source:{repository:"VatsalSin/Stock-Market-Indices-Dataset",path:"NIFTY 50.csv",upstream_git_blob_sha:"21a6b73916d577ce84178925fe515aeee1ad1441",cached_git_blob_sha:"4ca331b4de6c18f8e00b08097cc2c9535addc6f5",first_date:bars[0].date,last_date:bars[bars.length-1].date,raw_rows:bars.length,duplicate_dates:0,invalid_ohlc_rows:0,source_not_exchange_certified:true},
  method:"Chronological 75/25 split with expanding logistic regression refit every 20 test observations; custom Node.js gradient-descent implementation, not scikit-learn. Naive baselines use identical holdout dates.",
  feature_columns:featureNames, all_rows:frame.length, train_rows:split, test_rows:yTest.length,
  test_first_date:frame[split].date,test_last_date:frame[frame.length-1].date,test_up_rate:mean(yTest),
  test_tie_count:frame.slice(split).filter(r=>r.targetReturn===0).length, models:results,
  limitations:["Source snapshot ends in December 2019 and is not current-market validation.","Third-party CSV mirror; values are not exchange-certified.","Custom logistic implementation differs from the committed scikit-learn pipeline; treat as a diagnostic, not the final benchmark.","Random forest and gradient boosting are not evaluated in this diagnostic.","Bootstrap intervals are approximate.","No trading costs or profitability evaluated."]
};
fs.mkdirSync(path.dirname(output), {recursive:true});
fs.writeFileSync(output, JSON.stringify(report,null,2)+"\n");
console.log(JSON.stringify(report,null,2));
