#!/usr/bin/env python3
"""Bounded next-session intraday NIFTY option-buying validation.

Licensed raw quotes remain in data/cache/options_rolling and are not published.
Only sanitized per-trade outcomes and aggregate metrics are produced.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
import time
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from build_feature_matrix import build as build_feature_matrix  # noqa: E402

CACHE = ROOT / "data" / "cache"
OPTION_CACHE = CACHE / "options_rolling"
REPORT = ROOT / "reports" / "option_validation"
PLAN_VERSION = "OPT-BUY-1.0"
SEED = 20261014
FEATURE_PREFIX = ("ret_", "mom_", "vol_", "absret_")
BASE_FEATURES = {"log_close", "intraday_return", "range", "gap", "log_volume", "rsi_14"}
HORIZONS = (5, 20)
OFFSETS = tuple(range(-10, 11))
OPTION_TYPES = ("CALL", "PUT")
SLIPPAGE_BPS = (0, 25, 50, 100)
BROKERAGE_CASES = (10, 20)
ENTRY_TIME = "09:20"
EXIT_TIME = "15:25"
SEBI_RATE = 10.0 / 10_000_000.0
STAMP_RATE = 0.00003
EXCHANGE_RATE = 0.0003553
GST_RATE = 0.18
START_STT_RATE = 0.001
APRIL_2026_STT_RATE = 0.0015
BOOTSTRAP_REPS = 2000


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_dirs() -> None:
    REPORT.mkdir(parents=True, exist_ok=True)
    OPTION_CACHE.mkdir(parents=True, exist_ok=True)


def read_daily_and_build_matrix() -> pd.DataFrame:
    source = CACHE / "nifty50_daily.csv"
    if not source.exists():
        raise FileNotFoundError("Validated daily NIFTY cache is missing: data/cache/nifty50_daily.csv")
    daily = pd.read_csv(source)
    needed = {"date", "open", "high", "low", "close", "volume", "source_id"}
    if not needed.issubset(set(daily.columns)):
        raise ValueError("Daily cache schema is missing required fields")
    frame = build_feature_matrix(daily).sort_values("date").reset_index(drop=True)
    frame["date"] = pd.to_datetime(frame["date"], errors="raise")
    frame["origin_i"] = pd.to_numeric(frame["origin_i"], errors="raise").astype(int)
    frame.to_csv(CACHE / "model_matrix_option_validation.csv", index=False)
    return frame


def model_features(frame: pd.DataFrame) -> list[str]:
    cols = [
        c for c in frame.columns
        if c in BASE_FEATURES or c.startswith(FEATURE_PREFIX)
    ]
    cols = [c for c in cols if not c.startswith("ext_")]
    if len(cols) < 5:
        raise ValueError("Technical classifier feature family is incomplete")
    return cols


def predict_positive_probability(model, X: np.ndarray) -> np.ndarray:
    proba = model.predict_proba(X)
    classes = list(model.classes_)
    if 1 not in classes:
        return np.zeros(len(X), dtype=float)
    return np.asarray(proba[:, classes.index(1)], dtype=float)


def build_signals(frame: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Rebuild the technical Logistic classifier with OOF-only alert cutoffs."""
    cols = model_features(frame)
    cut = int(len(frame) * 0.8)
    all_origin_i = frame["origin_i"].to_numpy(int)
    test_rows = frame[(frame.origin_i >= cut) & (frame.origin_i < len(frame) - 1)].copy()
    if len(test_rows) < 30:
        raise ValueError(f"Too few chronological test origins: {len(test_rows)}")
    results = []
    details = {
        "plan_version": PLAN_VERSION,
        "data_rows": int(len(frame)),
        "data_first_date": frame.date.min().strftime("%Y-%m-%d"),
        "data_last_date": frame.date.max().strftime("%Y-%m-%d"),
        "cut_index": cut,
        "cut_date": frame.loc[cut, "date"].strftime("%Y-%m-%d"),
        "features": cols,
        "model": "SimpleImputer(median) + StandardScaler + LogisticRegression(C=0.1,class_weight=balanced,max_iter=1500,seed=20261014)",
        "threshold_rule": "75th percentile of purged development-only 4-fold TimeSeriesSplit out-of-fold probabilities",
        "horizons": {},
    }
    for h in HORIZONS:
        target = f"target_vol_expansion_{h}"
        if target not in frame:
            raise ValueError(f"Expected classifier target missing: {target}")
        usable = frame.loc[frame[target].notna()].copy()
        dev = usable.loc[usable.origin_i < cut - h].copy()
        ydev = pd.to_numeric(dev[target], errors="raise").astype(int).to_numpy()
        if len(dev) < 300 or len(np.unique(ydev)) < 2:
            raise ValueError(f"Development target too small or single class at horizon {h}")
        Xdev = dev[cols].to_numpy(float)
        origins = dev.origin_i.to_numpy(int)
        oof_probability = []
        fold_counts = []
        splitter = TimeSeriesSplit(n_splits=4)
        for train_index, valid_index in splitter.split(Xdev):
            first_valid_origin = int(origins[valid_index[0]])
            purged_train = train_index[origins[train_index] + h <= first_valid_origin]
            if len(purged_train) < 100 or len(np.unique(ydev[purged_train])) < 2:
                continue
            model = make_pipeline(
                SimpleImputer(strategy="median"),
                StandardScaler(),
                LogisticRegression(C=0.1, max_iter=1500, class_weight="balanced", random_state=SEED),
            )
            model.fit(Xdev[purged_train], ydev[purged_train])
            p = predict_positive_probability(model, Xdev[valid_index])
            oof_probability.extend(p.tolist())
            fold_counts.append({"n_train_after_purge": int(len(purged_train)), "n_valid": int(len(valid_index))})
        if len(oof_probability) < 100:
            raise ValueError(f"Insufficient purged OOF probabilities at horizon {h}")
        threshold = float(np.quantile(np.asarray(oof_probability), 0.75))
        final_model = make_pipeline(
            SimpleImputer(strategy="median"),
            StandardScaler(),
            LogisticRegression(C=0.1, max_iter=1500, class_weight="balanced", random_state=SEED),
        )
        final_model.fit(Xdev, ydev)
        Xtest = test_rows[cols].to_numpy(float)
        test_p = predict_positive_probability(final_model, Xtest)
        for (_, row), probability in zip(test_rows.iterrows(), test_p):
            origin_i = int(row.origin_i)
            next_date = frame.loc[origin_i + 1, "date"]
            results.append({
                "origin_date": row.date.strftime("%Y-%m-%d"),
                "trade_date": next_date.strftime("%Y-%m-%d"),
                "horizon": h,
                "probability": float(probability),
                "threshold": threshold,
                "alert": bool(probability >= threshold),
                "origin_i": origin_i,
            })
        details["horizons"][str(h)] = {
            "n_development": int(len(dev)),
            "n_test_origins": int(len(test_rows)),
            "n_oof_probabilities": int(len(oof_probability)),
            "threshold": threshold,
            "oof_alert_fraction": float(np.mean(np.asarray(oof_probability) >= threshold)),
            "test_alert_fraction": float(np.mean(test_p >= threshold)),
            "folds": fold_counts,
        }
    signals = pd.DataFrame(results).sort_values(["trade_date", "horizon"]).reset_index(drop=True)
    signals.to_csv(REPORT / "signals.csv", index=False)
    details["signals_rows"] = int(len(signals))
    details["daily_data_sha256"] = sha256(CACHE / "nifty50_daily.csv")
    (REPORT / "classifier_manifest.json").write_text(json.dumps(details, indent=2), encoding="utf-8")
    return signals, details


def offset_label(offset: int) -> str:
    if offset == 0:
        return "ATM"
    return f"ATM+{offset}" if offset > 0 else f"ATM{offset}"


def safe_filename(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", text)


def request_chunks(start: date, end_exclusive: date):
    current = start
    while current < end_exclusive:
        nxt = min(current + timedelta(days=30), end_exclusive)
        yield current, nxt
        current = nxt


def locate_option_series(payload: dict, option_type: str):
    data = payload.get("data", payload)
    if not isinstance(data, dict):
        raise ValueError("Dhan response data field is not an object")
    key = "ce" if option_type == "CALL" else "pe"
    if key not in data and any(k in data for k in ("timestamp", "open", "close")):
        part = data
    elif key in data:
        part = data.get(key)
    else:
        status = str(payload.get("status", "")).lower()
        if status in {"success", "ok"}:
            return None
        raise ValueError("Dhan response has no expected call/put series")
    if part is None:
        return None
    if not isinstance(part, dict):
        raise ValueError("Dhan option series is not an object")
    return part


def validate_payload(payload: dict, option_type: str) -> str:
    part = locate_option_series(payload, option_type)
    if part is None:
        return "EMPTY"
    if "timestamp" not in part:
        raise ValueError("Dhan option series lacks timestamp array")
    n = len(part["timestamp"])
    if n == 0:
        return "EMPTY"
    for field in ("open", "close", "strike", "spot"):
        if field not in part or len(part[field]) != n:
            raise ValueError(f"Dhan option series has absent or unequal {field} array")
    return "PASS"


def acquire_options(refresh: bool = False) -> dict:
    """Acquire only the four rolling series needed for the prespecified same-day structures."""
    ensure_dirs()
    token = os.getenv("DHAN_ACCESS_TOKEN", "").strip()
    try:
        frame = read_daily_and_build_matrix()
        signals, _ = build_signals(frame)
    except Exception as exc:
        manifest = {
            "plan_version": PLAN_VERSION,
            "created_at_utc": utc_now(),
            "status": "BLOCKED_NO_VALID_DAILY_DATA",
            "error_type": type(exc).__name__,
            "error_summary": str(exc)[:250],
            "requests_planned": 0,
            "requests_successful_or_empty": 0,
            "requests_failed": 0,
        }
        (OPTION_CACHE / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        (REPORT / "acquisition_summary.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        update_managed_documents("ACQUISITION", manifest=manifest)
        return manifest

    dates = pd.to_datetime(signals.trade_date, errors="raise").dt.date
    requested_start = min(dates)
    end_exclusive = max(dates) + timedelta(days=1)
    history_floor = date.today() - timedelta(days=365 * 5)
    request_start = max(requested_start, history_floor)
    chunks = list(request_chunks(request_start, end_exclusive))
    if not chunks:
        return write_blocked("BLOCKED_EMPTY_DATE_RANGE", "No trade dates remain in the supported historical range.")
    # ATM CALL/PUT serve the straddle and define the ATM strike. One adjacent
    # OTM CALL and PUT serve the strangle. Other offsets cannot affect this plan.
    required_requests = ((0, "CALL"), (0, "PUT"), (1, "CALL"), (-1, "PUT"))
    planned = len(chunks) * len(required_requests)
    req_records, failures = [], []
    successes, cached = 0, 0
    stop_all_requests = False
    refresh = refresh or os.getenv("REFRESH_OPTIONS", "").lower() in {"1", "true", "yes"}

    session = requests.Session()
    if token:
        session.headers.update({"Accept": "application/json", "Content-Type": "application/json", "access-token": token})

    for d0, d1 in chunks:
        if stop_all_requests:
            break
        for offset, opt_type in required_requests:
            rel = Path("data/cache/options_rolling") / (
                f"{d0:%Y%m%d}_{d1:%Y%m%d}_{'m' if offset < 0 else 'p'}{abs(offset):02d}_{opt_type}.json"
            )
            if offset == 0:
                rel = Path("data/cache/options_rolling") / f"{d0:%Y%m%d}_{d1:%Y%m%d}_ATM_{opt_type}.json"
            path = ROOT / rel
            if path.exists() and not refresh:
                try:
                    payload = json.loads(path.read_text(encoding="utf-8"))
                    state = validate_payload(payload, opt_type)
                    req_records.append({"from": d0.isoformat(), "to_exclusive": d1.isoformat(),
                                        "offset": offset, "option_type": opt_type,
                                        "status": "CACHED" if state == "PASS" else "EMPTY",
                                        "file": str(rel)})
                    successes += 1
                    cached += 1
                    continue
                except Exception:
                    # Corrupt cache is not trusted. Replace it only when authenticated access exists.
                    if not token:
                        failures.append({"from": d0.isoformat(), "to_exclusive": d1.isoformat(),
                                         "offset": offset, "option_type": opt_type,
                                         "error_type": "InvalidCacheNoCredential",
                                         "error_summary": "Cached response failed schema validation; refresh requires DHAN_ACCESS_TOKEN"})
                        continue
            if not token:
                failures.append({"from": d0.isoformat(), "to_exclusive": d1.isoformat(),
                                 "offset": offset, "option_type": opt_type,
                                 "error_type": "MissingCredential",
                                 "error_summary": "DHAN_ACCESS_TOKEN is not configured and response not cached"})
                continue

            request_body = {
                "exchangeSegment": "NSE_FNO",
                "interval": 5,
                "securityId": 13,
                "instrument": "OPTIDX",
                "expiryFlag": "WEEK",
                "expiryCode": 0,
                "strike": offset_label(offset),
                "drvOptionType": opt_type,
                "requiredData": ["open", "high", "low", "close", "iv", "volume", "strike", "oi", "spot"],
                "fromDate": d0.isoformat(),
                "toDate": d1.isoformat(),
            }
            last_error = "unknown"
            state = "FAIL"
            for attempt in range(3):
                try:
                    response = session.post("https://api.dhan.co/v2/charts/rollingoption",
                                            json=request_body, timeout=45)
                    if response.status_code in (401, 403):
                        last_error = f"AUTH_HTTP_{response.status_code}"
                        stop_all_requests = True
                        break
                    if response.status_code in (400, 404, 422):
                        last_error = f"REQUEST_SCHEMA_HTTP_{response.status_code}"
                        stop_all_requests = True
                        break
                    if response.status_code == 429 or response.status_code >= 500:
                        last_error = f"HTTP_{response.status_code}"
                        if attempt < 2:
                            time.sleep(2 ** attempt)
                            continue
                        break
                    if not response.ok or "json" not in response.headers.get("content-type", "").lower():
                        last_error = f"HTTP_OR_CONTENT_TYPE_{response.status_code}"
                        stop_all_requests = True
                        break
                    payload = response.json()
                    state = validate_payload(payload, opt_type)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    tmp = path.with_suffix(".json.tmp")
                    tmp.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
                    tmp.replace(path)
                    req_records.append({"from": d0.isoformat(), "to_exclusive": d1.isoformat(),
                                        "offset": offset, "option_type": opt_type,
                                        "status": state, "file": str(rel)})
                    successes += 1
                    break
                except Exception as exc:
                    last_error = f"{type(exc).__name__}: {str(exc)[:140]}"
                    if attempt < 2:
                        time.sleep(2 ** attempt)
            if state == "FAIL":
                failures.append({"from": d0.isoformat(), "to_exclusive": d1.isoformat(),
                                 "offset": offset, "option_type": opt_type,
                                 "error_type": "RequestOrSchemaFailure", "error_summary": last_error})
                if stop_all_requests:
                    break
            time.sleep(0.15)

    session.close()
    if stop_all_requests:
        status = "BLOCKED_REQUEST_AUTH_OR_SCHEMA"
    elif failures and successes:
        status = "PARTIAL"
    elif failures and not successes:
        status = "BLOCKED_NO_TOKEN" if not token else "BLOCKED_NO_VALID_OPTION_DATA"
    elif not failures and successes == planned:
        status = "PASS_CACHED" if cached == planned else "PASS"
    else:
        status = "PARTIAL"

    manifest = {
        "plan_version": PLAN_VERSION,
        "created_at_utc": utc_now(),
        "status": status,
        "daily_data_sha256": sha256(CACHE / "nifty50_daily.csv"),
        "requested_date_start": requested_start.isoformat(),
        "request_date_start_after_5y_clip": request_start.isoformat(),
        "request_date_end_exclusive": end_exclusive.isoformat(),
        "history_start_clipped_to_provider_window": bool(request_start > requested_start),
        "request_window_days_max": 30,
        "interval_minutes": 5,
        "expiry_flag": "WEEK",
        "expiry_code": 0,
        "requested_offset_type_pairs": [{"offset": x, "option_type": y} for x, y in required_requests],
        "requests_planned": planned,
        "requests_attempted": len(req_records) + len(failures),
        "requests_successful_or_empty": successes,
        "requests_cached": cached,
        "requests_failed": len(failures),
        "request_stopped_early_for_auth_or_schema": stop_all_requests,
        "failure_summaries": dict(Counter(f"{x.get('error_type')}:{x.get('error_summary', '')}" for x in failures)),
        "requests": req_records,
        "failures": failures,
        "raw_quote_cache_path": "data/cache/options_rolling (not committed or uploaded)",
    }
    (OPTION_CACHE / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    public = {k: v for k, v in manifest.items() if k not in {"requests", "failures"}}
    public["request_status_counts"] = dict(Counter(x.get("status", "UNKNOWN") for x in req_records))
    (REPORT / "acquisition_summary.json").write_text(json.dumps(public, indent=2), encoding="utf-8")
    write_json(REPORT / "acquisition_failures.csv", pd.DataFrame(failures))
    update_managed_documents("ACQUISITION", manifest=manifest)
    print(json.dumps(public, indent=2))
    return manifest

def payload_to_rows(payload: dict, option_type: str) -> list[dict]:
    part = locate_option_series(payload, option_type)
    if part is None or not part.get("timestamp"):
        return []
    timestamps = part.get("timestamp", [])
    n = len(timestamps)
    columns = {}
    for name in ("open", "high", "low", "close", "iv", "volume", "oi", "strike", "spot"):
        values = part.get(name)
        if values is None or len(values) != n:
            values = [None] * n
        columns[name] = values
    rows = []
    for i, ts in enumerate(timestamps):
        try:
            stamp = int(ts)
        except (ValueError, TypeError):
            continue
        rows.append({
            "timestamp": stamp,
            "option_type": option_type,
            **{k: _to_float(v[i]) for k, v in columns.items()},
        })
    return rows


def _to_float(x):
    try:
        if x is None:
            return np.nan
        v = float(x)
        return v if math.isfinite(v) else np.nan
    except (ValueError, TypeError):
        return np.nan


def load_quote_table(manifest: dict) -> tuple[pd.DataFrame, dict]:
    rows = []
    parse_failures = []
    for rec in manifest.get("requests", []):
        if rec.get("status") not in {"PASS", "CACHED", "EMPTY"}:
            continue
        path = ROOT / rec.get("file", "")
        if not path.exists():
            parse_failures.append("cached request file disappeared")
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            rows.extend(payload_to_rows(payload, rec["option_type"]))
        except Exception as exc:
            parse_failures.append(f"{rec.get('file')}: {type(exc).__name__}")
    if not rows:
        return pd.DataFrame(), {"raw_rows": 0, "usable_rows": 0, "duplicate_conflict_groups": 0, "parse_failures": parse_failures}
    quotes = pd.DataFrame(rows)
    unit = "ms" if quotes.timestamp.max() > 10**12 else "s"
    local = pd.to_datetime(quotes.timestamp, unit=unit, utc=True, errors="coerce").dt.tz_convert("Asia/Kolkata")
    quotes["date"] = local.dt.strftime("%Y-%m-%d")
    quotes["time"] = local.dt.strftime("%H:%M")
    quotes = quotes.dropna(subset=["date", "strike", "spot"])
    quotes = quotes[(quotes.strike > 0) & (quotes.spot > 0)]
    raw_rows = int(len(quotes))
    keys = ["date", "time", "option_type", "strike"]
    duplicates = quotes.groupby(keys, dropna=False).agg(
        n=("close", "size"),
        open_spread=("open", lambda x: float(x.max() - x.min()) if x.notna().any() else 0.0),
        close_spread=("close", lambda x: float(x.max() - x.min()) if x.notna().any() else 0.0),
    ).reset_index()
    conflicted = duplicates[(duplicates.n > 1) & ((duplicates.open_spread > 0.01) | (duplicates.close_spread > 0.01))]
    bad_keys = set(tuple(row) for row in conflicted[keys].itertuples(index=False, name=None))
    if bad_keys:
        tuples = list(zip(*(quotes[k] for k in keys)))
        keep = np.asarray([tuple(t) not in bad_keys for t in tuples])
        quotes = quotes.loc[keep]
    quotes = quotes.drop_duplicates(keys, keep="first")
    quotes = quotes.dropna(subset=["open", "close"])
    quotes = quotes[(quotes.open > 0) & (quotes.close > 0)]
    quotes = quotes.sort_values(keys).reset_index(drop=True)
    meta = {
        "raw_rows": raw_rows,
        "usable_rows": int(len(quotes)),
        "duplicate_conflict_groups": int(len(conflicted)),
        "duplicate_groups": int((duplicates.n > 1).sum()),
        "parse_failures": parse_failures[:20],
        "first_quote_date": str(quotes.date.min()) if len(quotes) else None,
        "last_quote_date": str(quotes.date.max()) if len(quotes) else None,
        "entry_time_rows": int((quotes.time == ENTRY_TIME).sum()),
        "exit_time_rows": int((quotes.time == EXIT_TIME).sum()),
    }
    return quotes, meta


def match_exit_price(rows: pd.DataFrame, trade_date: str, option_type: str, strike: float):
    if rows.empty:
        return None
    subset = rows[
        (rows.date.astype(str) == str(trade_date))
        & (rows.time.astype(str) == EXIT_TIME)
        & (rows.option_type.astype(str) == option_type)
        & np.isclose(pd.to_numeric(rows.strike, errors="coerce"), float(strike), atol=1e-6, rtol=0)
    ]
    if subset.empty:
        return None
    vals = pd.to_numeric(subset["close"], errors="coerce").dropna()
    return float(vals.iloc[0]) if len(vals) and vals.iloc[0] > 0 else None


def build_trade_candidate(quotes: pd.DataFrame, trade_date: str, structure: str):
    entry = quotes[(quotes.date == trade_date) & (quotes.time == ENTRY_TIME)].copy()
    exit_rows = quotes[(quotes.date == trade_date) & (quotes.time == EXIT_TIME)].copy()
    if entry.empty:
        return None, "MISSING_ENTRY_BAR"
    if exit_rows.empty:
        return None, "MISSING_EXIT_BAR"
    spot = pd.to_numeric(entry.spot, errors="coerce").dropna()
    if spot.empty:
        return None, "MISSING_ENTRY_SPOT"
    spot_value = float(spot.median())
    calls = entry[entry.option_type == "CALL"].drop_duplicates("strike")
    puts = entry[entry.option_type == "PUT"].drop_duplicates("strike")
    common = np.intersect1d(calls.strike.to_numpy(float), puts.strike.to_numpy(float))
    if not len(common):
        return None, "NO_COMMON_CALL_PUT_STRIKES"
    atm = float(common[np.argmin(np.abs(common - spot_value))])
    if structure == "straddle":
        legs = [("CALL", atm), ("PUT", atm)]
    elif structure == "strangle":
        call_strikes = calls.loc[calls.strike > atm, "strike"].to_numpy(float)
        put_strikes = puts.loc[puts.strike < atm, "strike"].to_numpy(float)
        if not len(call_strikes) or not len(put_strikes):
            return None, "NO_ONE_STEP_OTM_STRIKES"
        legs = [("CALL", float(np.min(call_strikes))), ("PUT", float(np.max(put_strikes)))]
    else:
        raise ValueError(f"Unknown structure {structure}")
    entry_prices = []
    exit_prices = []
    for opt_type, strike in legs:
        erow = entry[
            (entry.option_type == opt_type)
            & np.isclose(entry.strike.astype(float), strike, atol=1e-6, rtol=0)
        ]
        if erow.empty:
            return None, "MISSING_ENTRY_LEG"
        entry_price = float(erow.iloc[0]["open"])
        exit_price = match_exit_price(quotes, trade_date, opt_type, strike)
        if not math.isfinite(entry_price) or entry_price <= 0:
            return None, "INVALID_ENTRY_PREMIUM"
        if exit_price is None:
            return None, "MISSING_SAME_STRIKE_EXIT"
        entry_prices.append(entry_price)
        exit_prices.append(exit_price)
    return {
        "trade_date": trade_date,
        "structure": structure,
        "entry_prices": entry_prices,
        "exit_prices": exit_prices,
        "lot_size": lot_size_proxy(trade_date),
    }, "PASS"


def lot_size_proxy(trade_date: str) -> int:
    # A dated proxy only; the rolling endpoint does not expose stable contract expiry metadata.
    if trade_date < "2024-04-26":
        return 50
    if trade_date < "2024-11-20":
        return 25
    if trade_date < "2025-12-31":
        return 75
    return 65


def calculate_trade(trade: dict, slippage_bps: int, brokerage_per_order: int) -> dict:
    entry_prices = [float(x) for x in trade["entry_prices"]]
    exit_prices = [float(x) for x in trade["exit_prices"]]
    if len(entry_prices) != 2 or len(exit_prices) != 2:
        raise ValueError("Only complete two-leg long structures are permitted")
    if any(not math.isfinite(x) or x <= 0 for x in entry_prices + exit_prices):
        raise ValueError("Option premiums must be finite and positive")
    lot = int(trade["lot_size"])
    if lot <= 0:
        raise ValueError("lot_size must be positive")
    entry_raw = float(sum(entry_prices))
    exit_raw = float(sum(exit_prices))
    slip = float(slippage_bps) / 10000.0
    entry_exec = entry_raw * (1.0 + slip)
    exit_exec = exit_raw * (1.0 - slip)
    buy_turnover = entry_exec * lot
    sell_turnover = exit_exec * lot
    date_txt = str(trade["trade_date"])
    stt_rate = APRIL_2026_STT_RATE if date_txt >= "2026-04-01" else START_STT_RATE
    brokerage = float(brokerage_per_order) * 4.0
    stt = max(sell_turnover, 0.0) * stt_rate
    stamp = buy_turnover * STAMP_RATE
    sebi = (buy_turnover + sell_turnover) * SEBI_RATE
    exchange = (buy_turnover + sell_turnover) * EXCHANGE_RATE
    gst = GST_RATE * (brokerage + sebi + exchange)
    slip_cost = (entry_raw + exit_raw) * slip * lot
    explicit_fees = brokerage + stt + stamp + sebi + exchange + gst
    gross = (exit_raw - entry_raw) * lot
    total_cost = slip_cost + explicit_fees
    net = gross - total_cost
    debit_rupees = entry_exec * lot
    return {
        "gross_pnl_points": exit_raw - entry_raw,
        "gross_pnl_rupees": gross,
        "entry_debit_points": entry_exec,
        "entry_debit_rupees": debit_rupees,
        "sell_turnover_rupees": sell_turnover,
        "slippage_cost_rupees": slip_cost,
        "brokerage_rupees": brokerage,
        "stt_rate": stt_rate,
        "stt_rupees": stt,
        "stamp_duty_rupees": stamp,
        "sebi_fee_rupees": sebi,
        "exchange_fee_rupees": exchange,
        "gst_rupees": gst,
        "other_fees_rupees": explicit_fees,
        "total_cost_rupees": total_cost,
        "net_pnl_rupees": net,
        "net_return_on_debit": net / debit_rupees if debit_rupees > 0 else float("nan"),
        "lot_size_proxy": lot,
    }


def block_bootstrap_mean(values, block_len: int, n_boot: int = BOOTSTRAP_REPS, seed: int = SEED):
    x = np.asarray(list(values), dtype=float)
    x = x[np.isfinite(x)]
    if len(x) < 2:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    n = len(x)
    block_len = max(1, min(int(block_len), n))
    means = np.empty(n_boot, dtype=float)
    n_blocks = int(math.ceil(n / block_len))
    for b in range(n_boot):
        idx = []
        for _ in range(n_blocks):
            start = int(rng.integers(0, n))
            idx.extend((start + j) % n for j in range(block_len))
        means[b] = float(np.mean(x[np.asarray(idx[:n], dtype=int)]))
    return float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))


def block_bootstrap_difference(values, block_len: int, n_boot: int = BOOTSTRAP_REPS, seed: int = SEED):
    x = np.asarray(list(values), dtype=float)
    x = x[np.isfinite(x)]
    if len(x) < 3:
        return (float("nan"), float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    n = len(x)
    block_len = max(1, min(int(block_len), n))
    means = np.empty(n_boot, dtype=float)
    null_means = np.empty(n_boot, dtype=float)
    centered = x - np.mean(x)
    n_blocks = int(math.ceil(n / block_len))
    for b in range(n_boot):
        idx = []
        for _ in range(n_blocks):
            start = int(rng.integers(0, n))
            idx.extend((start + j) % n for j in range(block_len))
        idx = np.asarray(idx[:n], dtype=int)
        means[b] = float(np.mean(x[idx]))
        null_means[b] = float(np.mean(centered[idx]))
    observed = float(np.mean(x))
    p = (1.0 + float(np.sum(np.abs(null_means) >= abs(observed)))) / (n_boot + 1.0)
    lo, hi = float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))
    return lo, hi, p


def holm_adjust(pvalues) -> list[float]:
    p = np.asarray(list(pvalues), dtype=float)
    out = np.full(len(p), np.nan, dtype=float)
    valid = np.flatnonzero(np.isfinite(p))
    if not len(valid):
        return out.tolist()
    order = valid[np.argsort(p[valid])]
    m = len(order)
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, min(1.0, (m - rank) * float(p[idx])))
        out[idx] = running
    return out.tolist()


def no_trade_result(trade_date: str, structure: str, slippage: int, brokerage: int, alert: bool, probability, threshold, horizon, mode) -> dict:
    return {
        "trade_date": trade_date,
        "mode": mode,
        "horizon": horizon,
        "structure": structure,
        "probability": probability,
        "alert_threshold": threshold,
        "alert": bool(alert),
        "did_trade": False,
        "slippage_bps": slippage,
        "brokerage_per_order": brokerage,
        "lot_size_proxy": lot_size_proxy(trade_date),
        "entry_debit_points": 0.0,
        "gross_pnl_points": 0.0,
        "gross_pnl_rupees": 0.0,
        "slippage_cost_rupees": 0.0,
        "brokerage_rupees": 0.0,
        "stt_rupees": 0.0,
        "stamp_duty_rupees": 0.0,
        "sebi_fee_rupees": 0.0,
        "exchange_fee_rupees": 0.0,
        "gst_rupees": 0.0,
        "total_cost_rupees": 0.0,
        "net_pnl_rupees": 0.0,
        "net_return_on_debit": 0.0,
    }


def ledger_row(trade: dict, result: dict, mode: str, horizon, probability, threshold, alert: bool, slippage: int, brokerage: int) -> dict:
    return {
        "trade_date": trade["trade_date"],
        "mode": mode,
        "horizon": horizon,
        "structure": trade["structure"],
        "probability": probability,
        "alert_threshold": threshold,
        "alert": bool(alert),
        "did_trade": True,
        "slippage_bps": slippage,
        "brokerage_per_order": brokerage,
        "lot_size_proxy": result["lot_size_proxy"],
        "entry_debit_points": result["entry_debit_points"],
        "gross_pnl_points": result["gross_pnl_points"],
        "gross_pnl_rupees": result["gross_pnl_rupees"],
        "slippage_cost_rupees": result["slippage_cost_rupees"],
        "brokerage_rupees": result["brokerage_rupees"],
        "stt_rupees": result["stt_rupees"],
        "stamp_duty_rupees": result["stamp_duty_rupees"],
        "sebi_fee_rupees": result["sebi_fee_rupees"],
        "exchange_fee_rupees": result["exchange_fee_rupees"],
        "gst_rupees": result["gst_rupees"],
        "total_cost_rupees": result["total_cost_rupees"],
        "net_pnl_rupees": result["net_pnl_rupees"],
        "net_return_on_debit": result["net_return_on_debit"],
    }


def metrics_from_daily(rows: list[dict], block_len: int) -> dict:
    if not rows:
        return {}
    returns = np.asarray([r["net_return_on_debit"] for r in rows], dtype=float)
    returns = returns[np.isfinite(returns)]
    trades = [r for r in rows if r.get("did_trade")]
    pnls = np.asarray([r["net_pnl_rupees"] for r in trades], dtype=float)
    wins = pnls[pnls > 0]
    losses = pnls[pnls < 0]
    gross_profit = float(wins.sum()) if len(wins) else 0.0
    gross_loss = float(-losses.sum()) if len(losses) else 0.0
    cum = np.cumsum([r["net_pnl_rupees"] if r.get("did_trade") else 0.0 for r in rows])
    peaks = np.maximum.accumulate(np.concatenate([[0.0], cum]))[1:] if len(cum) else np.array([])
    dd = peaks - cum if len(cum) else np.array([])
    lo, hi = block_bootstrap_mean(returns, block_len=block_len, seed=SEED + block_len)
    return {
        "eligible_dates": int(len(rows)),
        "trade_count": int(len(trades)),
        "trade_rate": float(len(trades) / len(rows)) if rows else 0.0,
        "win_rate": float(np.mean(pnls > 0)) if len(pnls) else float("nan"),
        "mean_net_return_per_trade": float(np.mean([r["net_return_on_debit"] for r in trades])) if trades else float("nan"),
        "median_net_return_per_trade": float(np.median([r["net_return_on_debit"] for r in trades])) if trades else float("nan"),
        "mean_net_return_daily": float(np.mean(returns)) if len(returns) else float("nan"),
        "ci95_daily_return_low": lo,
        "ci95_daily_return_high": hi,
        "mean_net_pnl_rupees_per_trade": float(np.mean(pnls)) if len(pnls) else float("nan"),
        "median_net_pnl_rupees_per_trade": float(np.median(pnls)) if len(pnls) else float("nan"),
        "total_net_pnl_rupees": float(pnls.sum()) if len(pnls) else 0.0,
        "profit_factor": gross_profit / gross_loss if gross_loss > 0 else (float("inf") if gross_profit > 0 else float("nan")),
        "max_drawdown_rupees": float(np.max(dd)) if len(dd) else 0.0,
        "mean_premium_debit_points": float(np.mean([r["entry_debit_points"] for r in trades])) if trades else float("nan"),
        "mean_all_in_cost_rupees": float(np.mean([r["total_cost_rupees"] for r in trades])) if trades else float("nan"),
    }


def analyze_options() -> dict:
    ensure_dirs()
    daily = CACHE / "nifty50_daily.csv"
    raw_manifest_path = OPTION_CACHE / "manifest.json"
    if not daily.exists():
        return write_blocked("BLOCKED_NO_VALID_DAILY_DATA", "NIFTY daily cache unavailable; no option result computed.")
    if not raw_manifest_path.exists():
        return write_blocked("BLOCKED_NO_OPTIONS_MANIFEST", "No Dhan option acquisition manifest exists; no option result computed.")
    raw_manifest = json.loads(raw_manifest_path.read_text(encoding="utf-8"))
    if raw_manifest.get("status") in {"BLOCKED_NO_TOKEN", "BLOCKED_NO_VALID_DAILY_DATA", "BLOCKED_NO_VALID_OPTION_DATA", "BLOCKED_REQUEST_AUTH_OR_SCHEMA"}:
        return write_blocked(raw_manifest.get("status"), "Dhan historical option acquisition was blocked; no option P&L is claimed.", raw_manifest)
    frame = read_daily_and_build_matrix()
    signals, classifier_meta = build_signals(frame)
    quotes, quote_meta = load_quote_table(raw_manifest)
    if quotes.empty:
        return write_blocked("BLOCKED_NO_VALID_OPTION_QUOTES", "The acquisition attempt yielded no valid option quotes at the prespecified times.", raw_manifest, quote_meta)
    # Candidate dates must be derived from model holdout origins, not from quote availability.
    signal_by_horizon_date = {}
    for _, s in signals.iterrows():
        signal_by_horizon_date[(str(s.trade_date), int(s.horizon))] = {
            "origin_date": str(s.origin_date),
            "probability": float(s.probability),
            "threshold": float(s.threshold),
            "alert": bool(s.alert),
        }
    all_trade_dates = sorted(signals.trade_date.astype(str).unique())
    structure_cache = {}
    skip_counts = Counter()
    for trade_date in all_trade_dates:
        for structure in ("straddle", "strangle"):
            trade, reason = build_trade_candidate(quotes, trade_date, structure)
            structure_cache[(trade_date, structure)] = trade
            if trade is None:
                skip_counts[reason] += 1
    eligible_dates_by_structure = {
        structure: [d for d in all_trade_dates if structure_cache[(d, structure)] is not None]
        for structure in ("straddle", "strangle")
    }
    total_dates = len(all_trade_dates)
    coverage = {
        s: (len(eligible_dates_by_structure[s]) / total_dates if total_dates else 0.0)
        for s in ("straddle", "strangle")
    }
    rows_metrics = []
    ledger = []
    primary_rows = []
    for h in HORIZONS:
        for structure in ("straddle", "strangle"):
            dates = eligible_dates_by_structure[structure]
            block_len = h
            primary_candidate_daily = []
            primary_benchmark_daily = []
            first_half = []
            second_half = []
            for slip in SLIPPAGE_BPS:
                for broker in BROKERAGE_CASES:
                    base_rows = []
                    candidate_rows = []
                    for td in dates:
                        trade = structure_cache[(td, structure)]
                        sig = signal_by_horizon_date.get((td, h), {})
                        alert = bool(sig.get("alert", False))
                        probability = sig.get("probability", float("nan"))
                        threshold = sig.get("threshold", float("nan"))
                        base_result = calculate_trade(trade, slip, broker)
                        brow = ledger_row(trade, base_result, "always_buy", h, probability, threshold, alert, slip, broker)
                        brow["origin_date"] = sig.get("origin_date")
                        base_rows.append(brow)
                        ledger.append(brow)
                        if alert:
                            cand_result = calculate_trade(trade, slip, broker)
                            crow = ledger_row(trade, cand_result, "model_filtered", h, probability, threshold, alert, slip, broker)
                        else:
                            crow = no_trade_result(td, structure, slip, broker, alert, probability, threshold, h, "model_filtered")
                            crow["origin_date"] = sig.get("origin_date")
                        crow["origin_date"] = sig.get("origin_date")
                        candidate_rows.append(crow)
                        ledger.append(crow)
                    base_stats = metrics_from_daily(base_rows, block_len)
                    candidate_stats = metrics_from_daily(candidate_rows, block_len)
                    for mode, stats in (("always_buy", base_stats), ("model_filtered", candidate_stats)):
                        rec = {
                            "horizon": h,
                            "structure": structure,
                            "mode": mode,
                            "slippage_bps_per_side": slip,
                            "brokerage_per_order_rupees": broker,
                            **stats,
                        }
                        rows_metrics.append(rec)
                    if slip == 50 and broker == 10:
                        diff = np.asarray([c["net_return_on_debit"] for c in candidate_rows]) - np.asarray([b["net_return_on_debit"] for b in base_rows])
                        ci_low, ci_high, pval = block_bootstrap_difference(diff, block_len=block_len, n_boot=BOOTSTRAP_REPS, seed=SEED + h)
                        mid = len(candidate_rows) // 2
                        for ix, arr in ((0, candidate_rows[:mid]), (1, candidate_rows[mid:])):
                            half_stats = metrics_from_daily(arr, block_len)
                            if ix == 0:
                                first_half = arr
                                first_half_mean = half_stats.get("mean_net_return_daily", float("nan"))
                                first_half_trades = half_stats.get("trade_count", 0)
                            else:
                                second_half = arr
                                second_half_mean = half_stats.get("mean_net_return_daily", float("nan"))
                                second_half_trades = half_stats.get("trade_count", 0)
                        primary = {
                            "horizon": h,
                            "structure": structure,
                            "n_eligible_dates": len(dates),
                            "n_alert_trades": candidate_stats.get("trade_count", 0),
                            "candidate_mean_net_daily_return": candidate_stats.get("mean_net_return_daily", float("nan")),
                            "candidate_ci95_low": candidate_stats.get("ci95_daily_return_low", float("nan")),
                            "candidate_ci95_high": candidate_stats.get("ci95_daily_return_high", float("nan")),
                            "benchmark_mean_net_daily_return": base_stats.get("mean_net_return_daily", float("nan")),
                            "paired_mean_difference": float(np.mean(diff)) if len(diff) else float("nan"),
                            "paired_ci95_low": ci_low,
                            "paired_ci95_high": ci_high,
                            "paired_p_value": pval,
                            "p_holm": float("nan"),
                            "half1_mean_net_daily_return": first_half_mean,
                            "half1_trades": first_half_trades,
                            "half2_mean_net_daily_return": second_half_mean,
                            "half2_trades": second_half_trades,
                            "positive_at_100bps": None,
                            "trade_count_gate": bool(candidate_stats.get("trade_count", 0) >= 100),
                            "positive_primary_ci_gate": bool(
                                math.isfinite(candidate_stats.get("ci95_daily_return_low", float("nan")))
                                and candidate_stats["ci95_daily_return_low"] > 0
                                and candidate_stats.get("mean_net_return_daily", float("nan")) > 0
                            ),
                        }
                        primary_rows.append(primary)
            # Compare candidates at 100 bps / ₹10 and in both halves.
    if primary_rows:
        adjusted = holm_adjust([r["paired_p_value"] for r in primary_rows])
        for r, adj in zip(primary_rows, adjusted):
            r["p_holm"] = adj
            sens = next((x for x in rows_metrics if x.get("horizon") == r["horizon"] and x.get("structure") == r["structure"] and x.get("mode") == "model_filtered" and x.get("slippage_bps_per_side") == 100 and x.get("brokerage_per_order_rupees") == 10), {})
            r["positive_at_100bps"] = bool(sens.get("mean_net_return_daily", float("nan")) > 0)
            r["both_halves_positive"] = bool(r.get("half1_mean_net_daily_return", -1) > 0 and r.get("half2_mean_net_daily_return", -1) > 0)
            r["holm_outperformance_gate"] = bool(adj < 0.05 and r.get("paired_mean_difference", 0) > 0 and r.get("paired_ci95_low", 0) > 0)
            r["positive_candidate_gate"] = bool(
                r["trade_count_gate"]
                and r["positive_primary_ci_gate"]
                and r["positive_at_100bps"]
                and r["both_halves_positive"]
                and r["holm_outperformance_gate"]
            )
    metrics_df = pd.DataFrame(rows_metrics)
    primary_df = pd.DataFrame(primary_rows)
    ledger_df = pd.DataFrame(ledger)
    metrics_df.to_csv(REPORT / "performance.csv", index=False)
    primary_df.to_csv(REPORT / "primary_comparisons.csv", index=False)
    ledger_df.to_csv(REPORT / "trade_ledger.csv", index=False)
    quote_meta.update({
        "candidate_dates": int(total_dates),
        "eligible_date_coverage_by_structure": coverage,
        "skip_reason_counts": dict(skip_counts),
    })
    acquisition_status = raw_manifest.get("status", "UNKNOWN")
    complete_coverage = min(coverage.values()) if coverage else 0.0
    data_gate = acquisition_status in {"PASS", "PASS_CACHED"} and int(raw_manifest.get("requests_failed", 0)) == 0 and complete_coverage >= 0.80 and quote_meta.get("duplicate_conflict_groups", 0) == 0
    candidate_pass = bool(primary_rows) and any(bool(r.get("positive_candidate_gate")) for r in primary_rows)
    if not data_gate:
        overall = "INCONCLUSIVE_PARTIAL_OR_INCOMPLETE_DATA"
    elif candidate_pass:
        overall = "PAPER_CANDIDATE_GATE_PASS_PENDING_INDEPENDENT_REVIEW"
    else:
        overall = "NO_VALIDATED_EDGE"
    summary = {
        "plan_version": PLAN_VERSION,
        "created_at_utc": utc_now(),
        "overall_status": overall,
        "acquisition_status": acquisition_status,
        "options_manifest_status": raw_manifest.get("status"),
        "requests_planned": raw_manifest.get("requests_planned"),
        "requests_successful_or_empty": raw_manifest.get("requests_successful_or_empty"),
        "requests_failed": raw_manifest.get("requests_failed"),
        "classifier": classifier_meta,
        "quotes": quote_meta,
        "data_gate_pass": data_gate,
        "primary_candidates": primary_rows,
        "cost_settings": {
            "brokerage_per_order_rupees": list(BROKERAGE_CASES),
            "slippage_bps_each_premium_side": list(SLIPPAGE_BPS),
            "sell_STT_rate_before_2026_04_01": START_STT_RATE,
            "sell_STT_rate_from_2026_04_01": APRIL_2026_STT_RATE,
            "stamp_duty_buy_rate": STAMP_RATE,
            "SEBI_turnover_rate": SEBI_RATE,
            "NSE_transaction_fee_rate_assumed": EXCHANGE_RATE,
            "GST_rate_on_brokerage_exchange_SEBI": GST_RATE,
        },
        "warnings": [
            "Rolling option data contain no historical bid/ask; slippage is a sensitivity proxy.",
            "NIFTY lot sizes use a date-based proxy because stable expiry/contract identifiers were not provided by this endpoint.",
            "Same-session intraday results do not validate multi-day option holdings.",
            "The option P&L evaluation is a new outcome on the original model holdout, but is still one historical sample; a successful gate would only support prospective paper validation, not live deployment.",
        ],
    }
    (REPORT / "results_summary.json").write_text(json.dumps(summary, indent=2, allow_nan=True), encoding="utf-8")
    (REPORT / "quote_quality.json").write_text(json.dumps(quote_meta, indent=2, allow_nan=True), encoding="utf-8")
    make_results_markdown(summary, primary_df, metrics_df)
    update_managed_documents("ANALYSIS", summary=summary, manifest=raw_manifest)
    print(json.dumps({k: summary[k] for k in ("overall_status", "acquisition_status", "requests_failed", "data_gate_pass", "primary_candidates")}, indent=2, allow_nan=True))
    return summary


def write_blocked(status: str, reason: str, manifest: dict | None = None, quote_meta: dict | None = None) -> dict:
    ensure_dirs()
    summary = {
        "plan_version": PLAN_VERSION,
        "created_at_utc": utc_now(),
        "overall_status": status,
        "reason": reason,
        "acquisition_status": (manifest or {}).get("status", status),
        "requests_planned": (manifest or {}).get("requests_planned", 0),
        "requests_successful_or_empty": (manifest or {}).get("requests_successful_or_empty", 0),
        "requests_failed": (manifest or {}).get("requests_failed", 0),
        "quotes": quote_meta or {},
        "primary_candidates": [],
        "data_gate_pass": False,
        "strategy_approved": False,
    }
    (REPORT / "results_summary.json").write_text(json.dumps(summary, indent=2, allow_nan=True), encoding="utf-8")
    (REPORT / "primary_comparisons.csv").write_text("horizon,structure,n_alert_trades,paired_mean_difference,paired_p_value,p_holm\n", encoding="utf-8")
    (REPORT / "performance.csv").write_text("horizon,structure,mode,slippage_bps_per_side,brokerage_per_order_rupees,eligible_dates,trade_count,mean_net_return_daily\n", encoding="utf-8")
    (REPORT / "trade_ledger.csv").write_text("trade_date,mode,horizon,structure,did_trade,net_pnl_rupees\n", encoding="utf-8")
    make_results_markdown(summary, pd.DataFrame(), pd.DataFrame())
    update_managed_documents("BLOCKED", summary=summary, manifest=manifest or {})
    print(json.dumps(summary, indent=2, allow_nan=True))
    return summary


def fmt_percent(value):
    try:
        return f"{100 * float(value):.3f}%"
    except (ValueError, TypeError):
        return "NA"


def fmt_number(value, digits=4):
    try:
        value = float(value)
        return "NA" if not math.isfinite(value) else f"{value:.{digits}f}"
    except (ValueError, TypeError):
        return "NA"


def make_results_markdown(summary: dict, primary: pd.DataFrame, metrics: pd.DataFrame) -> None:
    status = summary.get("overall_status", "UNKNOWN")
    lines = [
        "# Option-buying validation results — OPT-BUY-1.0",
        "",
        f"**Last updated UTC:** {summary.get('created_at_utc', utc_now())}",
        f"**Decision status:** {status}",
        f"**Acquisition status:** {summary.get('acquisition_status', 'UNKNOWN')}",
        "",
        "This report never treats volatility-classification accuracy as option profitability. The original NIFTY-PRED-1.0 study remains closed and unchanged. Raw Dhan option quote files are not published.",
        "",
    ]
    if not summary.get("primary_candidates"):
        lines.extend([
            "## Empirical result",
            "",
            f"**{status}** — {summary.get('reason', 'No complete option P&L result was produced.')}",
            "",
            f"Option requests planned: {summary.get('requests_planned', 0)}; successful/empty: {summary.get('requests_successful_or_empty', 0)}; failed: {summary.get('requests_failed', 0)}.",
            "",
            "No option profit/loss result is claimed. The next decision is a data-quality/credential gate, not selection of a trading structure.",
        ])
    else:
        lines.extend([
            "## Primary comparisons",
            "",
            "Primary costs are ₹10/order and 50 bps adverse slippage per premium side. Returns are mean daily net premium return (non-alert dates are 0); P&L is calculated using a date-based lot-size proxy.",
            "",
            "| Alert horizon | Structure | Alert trades | Mean daily net return | 95% block CI | Always-buy mean | Paired diff | Paired 95% CI | Raw p | Holm p | 100 bps positive? | Half 1 / half 2 positive? | Gate |",
            "|---:|---|---:|---:|---|---:|---:|---|---:|---:|---|---|---|",
        ])
        for r in summary.get("primary_candidates", []):
            ci = f"{fmt_percent(r.get('candidate_ci95_low'))} to {fmt_percent(r.get('candidate_ci95_high'))}"
            diffci = f"{fmt_percent(r.get('paired_ci95_low'))} to {fmt_percent(r.get('paired_ci95_high'))}"
            halves = f"{fmt_percent(r.get('half1_mean_net_daily_return'))} / {fmt_percent(r.get('half2_mean_net_daily_return'))}"
            lines.append("| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
                r.get("horizon"), r.get("structure"), r.get("n_alert_trades"),
                fmt_percent(r.get("candidate_mean_net_daily_return")), ci,
                fmt_percent(r.get("benchmark_mean_net_daily_return")),
                fmt_percent(r.get("paired_mean_difference")), diffci,
                fmt_number(r.get("paired_p_value"), 4), fmt_number(r.get("p_holm"), 4),
                bool(r.get("positive_at_100bps")), halves,
                "PASS" if r.get("positive_candidate_gate") else "NO",
            ))
        lines.extend([
            "",
            "## Cost and execution notes",
            "",
            "- Four executed orders per completed 2-leg intraday trade; brokerage sensitivity is ₹10/₹20 per order.",
            "- Option sale STT: 0.10% through 2026-03-31, 0.15% from 2026-04-01. Buyer stamp duty 0.003%, SEBI turnover fee, current exchange transaction-fee approximation and GST are included.",
            "- Slippage is charged by increasing each entry premium and reducing each exit premium by 0/25/50/100 bps per side. This is a stress proxy because historical bid/ask is absent from the rolling endpoint.",
            "- Currency P&L uses a date-based lot-size proxy; premium-point returns and costs are more reliable than treating proxy lot-sized P&L as exact contracts.",
            "",
            "## Data quality and limitations",
            "",
            f"- Options acquisition status: {summary.get('acquisition_status')}; requests failed: {summary.get('requests_failed')}.",
            f"- Quote coverage: {summary.get('quotes', {}).get('eligible_date_coverage_by_structure', {})}.",
            f"- Skip counts: {summary.get('quotes', {}).get('skip_reason_counts', {})}.",
            f"- Conflicting duplicate quote groups: {summary.get('quotes', {}).get('duplicate_conflict_groups', 'unknown')}.",
            "- This only tests intraday positions. It does not prove multi-day straddles/strangles, because rolling relative strikes are not stable contract identifiers.",
            "- One chronological historical sample cannot establish live profitability. Even a passing gate supports only a prospective paper-trading validation, not live deployment.",
        ])
    lines.extend([
        "",
        "## Files and reproducibility",
        "",
        "- Sanitized acquisition summary: reports/option_validation/acquisition_summary.json",
        "- Classifier metadata and fixed OOF thresholds: reports/option_validation/classifier_manifest.json",
        "- Quote coverage: reports/option_validation/quote_quality.json",
        "- Primary comparisons: reports/option_validation/primary_comparisons.csv",
        "- Cost sensitivity matrix: reports/option_validation/performance.csv",
        "- Sanitized trade-outcome ledger: reports/option_validation/trade_ledger.csv",
        "- Raw option responses remain only in Actions cache at data/cache/options_rolling and are not uploaded.",
        "",
        "Developer handoff: independently inspect data/strike/time matching, cost formulae, date cutoff and results ledger before recommending even paper-trading validation.",
    ])
    (ROOT / "research" / "option-validation" / "RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_managed_documents(stage: str, summary: dict | None = None, manifest: dict | None = None) -> None:
    summary = summary or {}
    manifest = manifest or {}
    run_id = os.getenv("GITHUB_RUN_ID", "local")
    sha = os.getenv("GITHUB_SHA", "not supplied")
    server = os.getenv("GITHUB_SERVER_URL", "https://github.com")
    repo = os.getenv("GITHUB_REPOSITORY", "vishnuvcr/Naked-Options-v2")
    run_link = f"{server}/{repo}/actions/runs/{run_id}" if run_id != "local" else "local execution"
    status = summary.get("overall_status", manifest.get("status", "INITIALIZED"))
    err_summary = manifest.get("failure_summaries", {})
    if not err_summary and manifest.get("error_summary"):
        err_summary = {manifest.get("error_type", "ERROR"): manifest.get("error_summary")}
    section_readme = (
        "## Follow-on study: option-buying validation — OPT-BUY-1.0\n\n"
        "The original nine-phase NIFTY-PRED-1.0 prediction-only study remains closed and unchanged. This separate user-approved validation tests next-session intraday ATM straddles and one-step OTM strangles filtered by development-only 5/20-session technical Logistic volatility-expansion probabilities. It is not a live-trading workflow.\n\n"
        f"**Latest status:** {status}. **Git SHA:** {sha}. **Workflow:** {run_link}.\n\n"
        "- [Validation plan](research/OPTION_BUYING_VALIDATION_PLAN.md)\n"
        "- [Option validation results](research/option-validation/RESULTS.md)\n"
        "- [Primary comparisons CSV](reports/option_validation/primary_comparisons.csv)\n"
        "- [Option validation workflow](.github/workflows/option-buying-validation.yml)\n\n"
        "Raw option quotes are kept out of the public repository/artifacts. Do not call a strategy validated unless the cost, statistical, robustness and independent-review gates pass."
    )
    section_phase = (
        "## Separate follow-on study — option-buying validation (does not reopen NIFTY-PRED-1.0)\n\n"
        "| Track | Branch | Status | Evidence / gate |\n|---|---|---|---|\n"
        f"| Intraday option-buying validation | research/option-buying-validation | {status} | Workflow: {run_link}; commit: {sha}; acquisition: {manifest.get('status', summary.get('acquisition_status', 'not run'))}; requests failed: {manifest.get('requests_failed', summary.get('requests_failed', 'NA'))}. Independent post-result developer/tester gate required. |\n\n"
        "No live strategy is approved. The first experiment is intraday-only because rolling strike-relative option series do not establish stable multi-day contract identity."
    )
    section_experiment = (
        "## Follow-on option-buying validation — OPT-BUY-1.0\n\n"
        f"- Last stage: {stage}; decision: {status}; workflow: {run_link}; commit: {sha}.\n"
        f"- Options requests planned: {manifest.get('requests_planned', summary.get('requests_planned', 'NA'))}; completed/empty: {manifest.get('requests_successful_or_empty', summary.get('requests_successful_or_empty', 'NA'))}; failed: {manifest.get('requests_failed', summary.get('requests_failed', 'NA'))}.\n"
        f"- Primary comparisons written: {len(summary.get('primary_candidates', []))}; result file: research/option-validation/RESULTS.md.\n"
        "- Raw data were not committed or uploaded. Missing/failed requests remain visible in the sanitized acquisition summary/error log."
    )
    section_interaction = (
        "## 2026-10-14 — option-buying validation workflow stage\n\n"
        f"- Stage: {stage}; status: {status}; run: {run_link}; commit SHA: {sha}.\n"
        f"- Dhan option data requests planned/successful-or-empty/failed: {manifest.get('requests_planned', summary.get('requests_planned', 'NA'))}/{manifest.get('requests_successful_or_empty', summary.get('requests_successful_or_empty', 'NA'))}/{manifest.get('requests_failed', summary.get('requests_failed', 'NA'))}.\n"
        f"- Result file: research/option-validation/RESULTS.md; sanitized summary: reports/option_validation/results_summary.json.\n"
        "- Raw option prices remain in Actions cache only; no credentials or raw quote file is intentionally staged."
    )
    if err_summary:
        details = "\n".join(f"- {key}: {value}" for key, value in err_summary.items())
    else:
        details = "- No acquisition request failures recorded in this run."
    section_errors = (
        "## Option-validation acquisition error log — OPT-BUY-1.0\n\n"
        f"Stage: {stage}; workflow: {run_link}; commit: {sha}.\n\n"
        f"Request failure summaries (individual redacted request windows are preserved in the Actions cache manifest):\n{details}\n\n"
        "Credentials/authorization headers are not logged. See reports/option_validation/acquisition_summary.json for the sanitized status summary."
    )
    managed = [
        ("README.md", "OPTION_VALIDATION_README_START", "OPTION_VALIDATION_README_END", section_readme),
        ("research/PHASE_STATUS.md", "OPTION_VALIDATION_PHASE_START", "OPTION_VALIDATION_PHASE_END", section_phase),
        ("research/EXPERIMENT_LOG.md", "OPTION_VALIDATION_EXPERIMENT_START", "OPTION_VALIDATION_EXPERIMENT_END", section_experiment),
        ("research/INTERACTION_LOG.md", "OPTION_VALIDATION_INTERACTION_START", "OPTION_VALIDATION_INTERACTION_END", section_interaction),
        ("research/ERROR_LOG.md", "OPTION_VALIDATION_ERRORS_START", "OPTION_VALIDATION_ERRORS_END", section_errors),
    ]
    for rel, start_marker, end_marker, body in managed:
        path = ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        start = f"<!-- {start_marker} -->"
        end = f"<!-- {end_marker} -->"
        if start in text and end in text:
            a = text.index(start)
            b = text.index(end, a) + len(end)
            text = text[:a] + start + "\n" + body + "\n" + end + text[b:]
        else:
            text = text.rstrip() + "\n\n" + start + "\n" + body + "\n" + end + "\n"
        path.write_text(text, encoding="utf-8")


def write_json(path: Path, frame: pd.DataFrame) -> None:
    frame.to_csv(path, index=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--acquire-options", action="store_true", help="Retrieve missing rolling options quote windows from Dhan")
    parser.add_argument("--analyze", action="store_true", help="Run the prespecified classifier/option P&L evaluation")
    parser.add_argument("--refresh-options", action="store_true", help="Redownload cached Dhan rolling-options request windows")
    args = parser.parse_args()
    ensure_dirs()
    if args.acquire_options:
        result = acquire_options(refresh=args.refresh_options)
        if result.get("status") in {"PASS", "PASS_CACHED", "PARTIAL"}:
            raise SystemExit(0)
        if result.get("status") == "BLOCKED_NO_TOKEN":
            raise SystemExit(0)
        raise SystemExit(0)
    if args.analyze:
        analyze_options()
        raise SystemExit(0)
    parser.print_help()


if __name__ == "__main__":
    main()
