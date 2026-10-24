#!/usr/bin/env python3
"""Reproducible bounded NWCP-1.0 data, target, features, baseline and exploratory search runner."""
from __future__ import annotations
import argparse, hashlib, json, os, sys, time, traceback
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / "data" / "cache" / "nifty_weekly_candle_prediction_v1"
REPORTS = ROOT / "reports" / "nifty_weekly_candle_prediction_v1"
PUBLIC_REPO = "https://raw.githubusercontent.com/technovusin/nifty50-historical-data/main"
NSE_EXPIRY_URL = "https://www.nseindia.com/api/historicalOR/meta/foCPV/expireDts"
IST = "Asia/Kolkata"
TODAY = date.today()
START_DATE = date(2019, 2, 14)  # First NIFTY weekly expiry era
SWITCH_DATE = date(2025, 9, 2)  # First Tuesday weekly expiry under revised NSE schedule

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def json_write(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, default=str, sort_keys=True) + "\n", encoding="utf-8")

def log(message: str) -> None:
    print("[NWCP] " + message, flush=True)

def download_url(url: str, dest: Path, session: requests.Session, timeout: int = 45) -> dict:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 100:
        return {"status": "CACHE_HIT", "path": str(dest.relative_to(ROOT)), "bytes": dest.stat().st_size, "sha256": sha256_file(dest)}
    last_error = None
    for attempt in range(1, 4):
        try:
            response = session.get(url, timeout=timeout)
            if response.status_code == 404:
                return {"status": "NOT_FOUND", "url": url, "http_status": 404}
            response.raise_for_status()
            if not response.content or len(response.content) < 100:
                raise ValueError("response too small to be a data file")
            tmp = dest.with_suffix(dest.suffix + ".tmp")
            tmp.write_bytes(response.content)
            tmp.replace(dest)
            return {"status": "DOWNLOADED", "path": str(dest.relative_to(ROOT)), "bytes": dest.stat().st_size, "sha256": sha256_file(dest)}
        except Exception as exc:
            last_error = type(exc).__name__ + ": " + str(exc)[:180]
            time.sleep(attempt)
    return {"status": "FAILED", "url": url, "error": last_error}

def public_urls():
    for year in range(2017, TODAY.year + 1):
        if year < 2026:
            yield year, None, f"{PUBLIC_REPO}/1min/{year}/NIFTY50_1min_{year}.csv"
        else:
            for month in range(1, min(12, TODAY.month) + 1):
                yield year, month, f"{PUBLIC_REPO}/1min/2026/NIFTY50_1min_2026-{month:02d}.csv"

def acquire_public(force: bool = False) -> tuple[list[Path], list[dict]]:
    session = requests.Session()
    session.headers.update({"User-Agent": "NWCP-1.0 reproducible research; non-commercial audit", "Accept": "text/csv,*/*"})
    files, manifest = [], []
    for year, month, url in public_urls():
        suffix = f"{year}" if month is None else f"{year}-{month:02d}"
        path = CACHE / "public" / "1min" / f"NIFTY50_1min_{suffix}.csv"
        if force and path.exists():
            path.unlink()
        result = download_url(url, path, session)
        result.update({"source": "technovusin/nifty50-historical-data", "year": year, "month": month})
        manifest.append(result)
        if result["status"] in {"CACHE_HIT", "DOWNLOADED"}:
            files.append(path)
        log(f"public {suffix}: {result['status']}")
    return files, manifest

def find_column(columns, candidates):
    low = {str(c).strip().lower(): c for c in columns}
    for candidate in candidates:
        if candidate in low:
            return low[candidate]
    for c in columns:
        lc = str(c).strip().lower()
        if any(candidate in lc for candidate in candidates):
            return c
    return None

def fetch_dhan_security_id(session: requests.Session) -> str:
    urls = [
        "https://images.dhan.co/api-data/api-scrip-master.csv",
        "https://images.dhan.co/api-data/api-scrip-master-detailed.csv",
    ]
    for url in urls:
        try:
            response = session.get(url, timeout=50)
            response.raise_for_status()
            from io import BytesIO
            df = pd.read_csv(BytesIO(response.content), dtype=str, low_memory=False)
            id_col = find_column(df.columns, ["sem_smst_security_id", "security_id", "sem_security_id"])
            if id_col is None:
                continue
            # Use a conjunction over the row fields; do not hard-code a potentially stale ID.
            text = df.fillna("").astype(str).agg(" ".join, axis=1).str.upper()
            mask = text.str.contains("NIFTY 50|NIFTY50", regex=True)
            if "sem_segment" in [str(c).lower() for c in df.columns]:
                c = next(c for c in df.columns if str(c).lower() == "sem_segment")
                mask &= df[c].fillna("").astype(str).str.upper().str.contains("IDX_I|INDEX", regex=True)
            matches = df.loc[mask].copy()
            if len(matches) == 0:
                continue
            # Avoid silently selecting a derivative contract.
            if "sem_exm_exch_id" in [str(c).lower() for c in matches.columns]:
                c = next(c for c in matches.columns if str(c).lower() == "sem_exm_exch_id")
                matches = matches[matches[c].fillna("").astype(str).str.upper().eq("NSE")]
            if "sem_segment" in [str(c).lower() for c in matches.columns]:
                c = next(c for c in matches.columns if str(c).lower() == "sem_segment")
                matches = matches[matches[c].fillna("").astype(str).str.upper().eq("IDX_I")]
            if len(matches) == 1:
                value = str(matches.iloc[0][id_col]).strip()
                if value and value.lower() != "nan":
                    return value
        except Exception:
            continue
    raise RuntimeError("could not resolve a unique NIFTY 50 IDX_I security ID from Dhan scrip master")

def normalize_ohlc(df: pd.DataFrame, timestamp_col: str, timestamp_is_start: bool = True) -> pd.DataFrame:
    out = pd.DataFrame()
    ts = df[timestamp_col]
    if pd.api.types.is_numeric_dtype(ts):
        parsed = pd.to_datetime(pd.to_numeric(ts, errors="coerce"), unit="s", utc=True).dt.tz_convert(IST)
    else:
        parsed = pd.to_datetime(ts, errors="coerce")
        if getattr(parsed.dt, "tz", None) is None:
            parsed = parsed.dt.tz_localize(IST, ambiguous="NaT", nonexistent="NaT")
        else:
            parsed = parsed.dt.tz_convert(IST)
    out["bar_start"] = parsed
    if not timestamp_is_start:
        out["bar_start"] = out["bar_start"] - pd.Timedelta(minutes=1)
    for col in ["open", "high", "low", "close"]:
        source_col = find_column(df.columns, [col])
        if source_col is None:
            raise ValueError("missing OHLC column " + col)
        out[col] = pd.to_numeric(df[source_col], errors="coerce")
    out["source"] = "public"
    out = out.dropna(subset=["bar_start", "open", "high", "low", "close"])
    out = out[(out["bar_start"].dt.strftime("%H:%M") >= "09:15") & (out["bar_start"].dt.strftime("%H:%M") <= "15:29")]
    out = out.sort_values("bar_start")
    return out

def read_public(files: list[Path]) -> tuple[pd.DataFrame, list[dict]]:
    parts, audits = [], []
    for path in files:
        try:
            df = pd.read_csv(path, low_memory=False)
            tcol = find_column(df.columns, ["timestamp", "datetime", "ts", "epoch"])
            if tcol is None:
                raise ValueError("no timestamp field")
            part = normalize_ohlc(df, tcol, timestamp_is_start=True)
            part["source"] = "public"
            parts.append(part)
            audits.append({"file": str(path.relative_to(ROOT)), "rows_read": int(len(df)), "valid_bars": int(len(part)), "sha256": sha256_file(path), "status": "OK"})
        except Exception as exc:
            audits.append({"file": str(path.relative_to(ROOT)), "status": "FAILED", "error": type(exc).__name__ + ": " + str(exc)[:160]})
    if not parts:
        return pd.DataFrame(), audits
    bars = pd.concat(parts, ignore_index=True).sort_values("bar_start")
    duplicate_count = int(bars.duplicated("bar_start", keep=False).sum())
    bars = bars.drop_duplicates("bar_start", keep="last").sort_values("bar_start").reset_index(drop=True)
    bars["bar_end"] = bars["bar_start"] + pd.Timedelta(minutes=1)
    bars["session_date"] = bars["bar_start"].dt.date
    audits.append({"source": "public_aggregate", "valid_bars": int(len(bars)), "duplicate_rows_removed_or_collapsed": duplicate_count, "start": str(bars.bar_start.min()), "end": str(bars.bar_start.max())})
    return bars, audits

def acquire_dhan(force: bool = False) -> tuple[pd.DataFrame, dict]:
    token = os.environ.get("DHAN_ACCESS_TOKEN", "").strip()
    if not token:
        return pd.DataFrame(), {"status": "SKIPPED_NO_SECRET", "note": "DHAN_ACCESS_TOKEN unavailable; public-data audit continues"}
    session = requests.Session()
    session.headers.update({"Accept": "application/json", "Content-Type": "application/json", "access-token": token})
    try:
        security_id = fetch_dhan_security_id(session)
    except Exception as exc:
        # Do not show headers or token in logs.
        return pd.DataFrame(), {"status": "FAILED_SECURITY_MASTER", "error": type(exc).__name__ + ": " + str(exc)[:180]}
    start = max(date(2021, 1, 1), TODAY - timedelta(days=1095))
    end = TODAY
    # In this public repository, keep licensed Dhan rows in an ephemeral runner cache unless redistribution/cache rights are established.
    dest_dir = Path(os.environ.get("NWCP_DHAN_CACHE_DIR", str(CACHE / "dhan"))) / "intraday"
    dest_dir.mkdir(parents=True, exist_ok=True)
    chunks, failures = [], []
    cursor = start
    while cursor <= end:
        chunk_end = min(end, cursor + timedelta(days=89))
        cache_file = dest_dir / f"{cursor.isoformat()}_{chunk_end.isoformat()}.json"
        if cache_file.exists() and cache_file.stat().st_size > 100 and not force:
            payload = json.loads(cache_file.read_text(encoding="utf-8"))
            status = "CACHE_HIT"
        else:
            body = {
                "securityId": security_id, "exchangeSegment": "IDX_I", "instrument": "INDEX",
                "interval": "1", "oi": False,
                "fromDate": cursor.strftime("%Y-%m-%d 00:00:00"),
                "toDate": chunk_end.strftime("%Y-%m-%d 23:59:00"),
            }
            payload = None
            status = "FAILED"
            error_text = None
            for attempt in range(1, 4):
                try:
                    response = session.post("https://api.dhan.co/v2/charts/intraday", json=body, timeout=55)
                    if response.status_code >= 400:
                        raise RuntimeError("HTTP " + str(response.status_code) + " from Dhan historical endpoint")
                    payload = response.json()
                    if not isinstance(payload, dict) or not payload.get("timestamp"):
                        raise ValueError("Dhan response missing timestamp array")
                    cache_file.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
                    status = "DOWNLOADED"
                    break
                except Exception as exc:
                    error_text = type(exc).__name__ + ": " + str(exc)[:160]
                    time.sleep(attempt * 2)
            if status == "FAILED":
                failures.append({"start": str(cursor), "end": str(chunk_end), "error": error_text})
        if payload and isinstance(payload, dict) and payload.get("timestamp"):
            try:
                chunk = pd.DataFrame({
                    "timestamp": payload["timestamp"], "open": payload["open"], "high": payload["high"],
                    "low": payload["low"], "close": payload["close"],
                })
                chunk = normalize_ohlc(chunk, "timestamp", timestamp_is_start=True)
                chunk["source"] = "dhan"
                chunks.append(chunk)
            except Exception as exc:
                failures.append({"start": str(cursor), "end": str(chunk_end), "error": "parse " + type(exc).__name__ + ": " + str(exc)[:120]})
        log(f"Dhan chunk {cursor} to {chunk_end}: {status}")
        cursor = chunk_end + timedelta(days=1)
    if not chunks:
        return pd.DataFrame(), {"status": "FAILED_NO_BARS", "chunks": len(failures), "failures": failures[:15]}
    bars = pd.concat(chunks, ignore_index=True).drop_duplicates("bar_start", keep="last").sort_values("bar_start").reset_index(drop=True)
    bars["bar_end"] = bars["bar_start"] + pd.Timedelta(minutes=1)
    bars["session_date"] = bars["bar_start"].dt.date
    return bars, {"status": "PARTIAL" if failures else "OK", "security_id_resolved": True, "valid_bars": int(len(bars)), "start": str(bars.bar_start.min()), "end": str(bars.bar_start.max()), "failed_chunks": len(failures), "failures": failures[:15]}

def nse_expiries_by_year(year: int, session: requests.Session) -> list[date]:
    url = f"{NSE_EXPIRY_URL}?instrument=OPTIDX&symbol=NIFTY&year={year}"
    response = session.get(url, timeout=25)
    response.raise_for_status()
    payload = response.json()
    values = payload.get("expiresDts", [])
    expiries = []
    for value in values:
        try:
            expiries.append(datetime.strptime(str(value), "%d-%b-%Y").date())
        except ValueError:
            try:
                expiries.append(pd.Timestamp(value).date())
            except Exception:
                pass
    return sorted(set(expiries))

def get_expiry_calendar(session_dates: set[date]) -> tuple[list[date], dict]:
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 NWCP research; contact not provided", "Accept": "application/json,text/plain,*/*", "Referer": "https://www.nseindia.com/"})
    try:
        # Establish a session for exchange endpoints.
        session.get("https://www.nseindia.com/", timeout=20)
    except Exception:
        pass
    official, year_status = [], {}
    for year in range(2019, TODAY.year + 1):
        try:
            values = [d for d in nse_expiries_by_year(year, session) if START_DATE <= d <= TODAY]
            if values:
                official.extend(values)
                year_status[str(year)] = {"status": "OK", "expiry_count": len(values)}
            else:
                year_status[str(year)] = {"status": "EMPTY"}
        except Exception as exc:
            year_status[str(year)] = {"status": "FAILED", "error": type(exc).__name__ + ": " + str(exc)[:120]}
    official = sorted(set(official))
    # A second source of session dates helps resolve shifted expiry candidates when NSE expiry API is blocked.
    fallback = []
    calendar_status = "NOT_TRIED"
    try:
        import pandas_market_calendars as mcal
        cal = mcal.get_calendar("NSE")
        schedule = cal.schedule(start_date="2019-01-01", end_date=TODAY.isoformat())
        valid_sessions = set(pd.DatetimeIndex(schedule.index).date)
        calendar_status = "pandas_market_calendars:NSE"
        candidates = []
        d = date(2019, 2, 14)
        while d <= min(date(2025, 8, 28), TODAY):
            if d.weekday() == 3:  # Thursday through previous expiry regime
                candidates.append(d)
            d += timedelta(days=1)
        d = SWITCH_DATE
        while d <= TODAY:
            if d.weekday() == 1:  # Tuesday under the revised expiry regime
                candidates.append(d)
            d += timedelta(days=1)
        for nominal in candidates:
            actual = nominal
            if actual not in valid_sessions:
                prior = [s for s in valid_sessions if s < nominal and (nominal - s).days <= 4]
                if not prior:
                    continue
                actual = max(prior)
            fallback.append(actual)
        fallback = sorted(set(fallback))
    except Exception as exc:
        calendar_status = "calendar_failed:" + type(exc).__name__
        # Last-resort observed-session fallback; explicitly not an authoritative expiry catalogue.
        d = date(2019, 2, 14)
        while d <= TODAY:
            if d.weekday() == (3 if d < SWITCH_DATE else 1):
                actual = d
                if actual not in session_dates:
                    prior = [s for s in session_dates if s < d and (d - s).days <= 4]
                    if prior:
                        actual = max(prior)
                if actual in session_dates:
                    fallback.append(actual)
            d += timedelta(days=1)
        fallback = sorted(set(fallback))
    # Prefer complete official data when it has meaningful coverage; fill unavailable years from calendar fallback.
    counts_by_year = {year: sum(1 for d in official if d.year == year) for year in range(2019, TODAY.year + 1)}
    # The API must return roughly a full weekly sequence before its year is trusted.
    trusted_official_years = {year for year, count in counts_by_year.items() if count >= (30 if year in {2019, TODAY.year} else 40)}
    chosen, provenance = set(), {}
    for d in fallback:
        if d.year not in trusted_official_years:
            chosen.add(d)
            provenance[d.isoformat()] = "calendar_fallback"
    for d in official:
        if d.year in trusted_official_years:
            chosen.add(d)
            provenance[d.isoformat()] = "nse_expiry_api"
    dates = sorted(d for d in chosen if START_DATE <= d <= TODAY)
    audit = {
        "source": "mixed_official_and_fallback" if official else "calendar_fallback_only",
        "official_expiry_count": len(official),
        "fallback_expiry_count": len(fallback),
        "selected_expiry_count": len(dates),
        "official_year_status": year_status,
        "calendar_status": calendar_status,
        "first": str(dates[0]) if dates else None,
        "last": str(dates[-1]) if dates else None,
        "fallback_dates": sum(1 for d in dates if provenance.get(d.isoformat()) != "nse_expiry_api"),
        "provenance": provenance,
    }
    return dates, audit

def make_target_rows(bars: pd.DataFrame, expiries: list[date], expiry_audit: dict) -> tuple[pd.DataFrame, dict]:
    if bars.empty:
        return pd.DataFrame(), {"status": "BLOCKED_NO_BARS"}
    data = bars.sort_values("bar_start").copy()
    data["session_date"] = data["bar_start"].dt.date
    observed_sessions = sorted(set(data["session_date"]))
    session_set = set(observed_sessions)
    # Use the package calendar to identify actual trading sessions; the price source must also have the target bars.
    try:
        import pandas_market_calendars as mcal
        cal = mcal.get_calendar("NSE")
        start = max(date(2019, 1, 1), min(observed_sessions))
        schedule = cal.schedule(start_date=start.isoformat(), end_date=max(observed_sessions).isoformat())
        official_sessions = sorted(set(pd.DatetimeIndex(schedule.index).date))
        calendar_source = "pandas_market_calendars:NSE"
    except Exception:
        official_sessions = observed_sessions
        calendar_source = "observed_price_source_dates_only"
    # Include exchange-observed special sessions; weekly expiry logic still comes from official expiry dates when available.
    sessions = sorted(set(official_sessions) | set(observed_sessions))
    by_start = {ts: row for ts, row in data.set_index("bar_start").iterrows()}
    session_rows = {}
    for session_date, group in data.groupby("session_date", sort=True):
        group = group.sort_values("bar_start")
        session_rows[session_date] = group
    daily_complete = {}
    for session_date, group in session_rows.items():
        regular = group[(group.bar_start.dt.strftime("%H:%M") >= "09:15") & (group.bar_start.dt.strftime("%H:%M") <= "15:29")]
        if len(regular):
            daily_complete[session_date] = {
                "open": float(regular.iloc[0].open), "high": float(regular.high.max()),
                "low": float(regular.low.min()), "close": float(regular.iloc[-1].close),
                "rows": int(len(regular))
            }
    output, excluded = [], []
    provenance = expiry_audit.get("provenance", {})
    for i in range(1, len(expiries)):
        prev_expiry, expiry = expiries[i - 1], expiries[i]
        prior_sessions = [d for d in sessions if d > prev_expiry]
        if not prior_sessions or prior_sessions[0] > expiry:
            excluded.append({"previous_expiry": str(prev_expiry), "expiry": str(expiry), "reason": "no_anchor_session"})
            continue
        anchor_date = prior_sessions[0]
        anchor_start = pd.Timestamp(datetime.combine(anchor_date, datetime.min.time()), tz=IST) + pd.Timedelta(hours=9, minutes=15)
        anchor_ts = pd.Timestamp(datetime.combine(anchor_date, datetime.min.time()), tz=IST) + pd.Timedelta(hours=9, minutes=59)
        expiry_ts = pd.Timestamp(datetime.combine(expiry, datetime.min.time()), tz=IST) + pd.Timedelta(hours=15, minutes=29)
        anchor_match = data[data.bar_start.eq(anchor_ts)]
        expiry_match = data[data.bar_start.eq(expiry_ts)]
        if len(anchor_match) != 1:
            excluded.append({"previous_expiry": str(prev_expiry), "expiry": str(expiry), "anchor_date": str(anchor_date), "reason": "missing_or_duplicate_0959_bar"})
            continue
        if len(expiry_match) != 1:
            excluded.append({"previous_expiry": str(prev_expiry), "expiry": str(expiry), "anchor_date": str(anchor_date), "reason": "missing_or_duplicate_1529_bar"})
            continue
        p0, p1 = float(anchor_match.iloc[0].close), float(expiry_match.iloc[0].close)
        label = "UP" if p1 > p0 else ("DOWN" if p1 < p0 else "TIE")
        output.append({
            "previous_expiry": str(prev_expiry), "anchor_date": str(anchor_date),
            "anchor_time_ist": anchor_ts.isoformat(), "current_expiry": str(expiry),
            "expiry_close_time_ist": (expiry_ts + pd.Timedelta(minutes=1)).isoformat(),
            "p0": p0, "p1": p1, "change_points": p1 - p0, "change_pct": p1 / p0 - 1.0,
            "label": label, "expiry_source": provenance.get(str(expiry), "calendar_fallback"),
            "anchor_source": str(anchor_match.iloc[0].source), "expiry_close_source": str(expiry_match.iloc[0].source),
        })
    frame = pd.DataFrame(output)
    audit = {
        "status": "OK" if len(frame) else "BLOCKED_NO_VALID_LABELS",
        "calendar_source": calendar_source,
        "expiry_count": len(expiries), "candidate_intervals": max(0, len(expiries) - 1),
        "valid_labels": len(frame), "excluded_intervals": len(excluded), "excluded_examples": excluded[:25],
        "ties": int((frame.label == "TIE").sum()) if len(frame) else 0,
        "up": int((frame.label == "UP").sum()) if len(frame) else 0,
        "down": int((frame.label == "DOWN").sum()) if len(frame) else 0,
        "first_anchor": str(frame.anchor_date.min()) if len(frame) else None,
        "last_expiry": str(frame.current_expiry.max()) if len(frame) else None,
        "anchor_price_source_counts": frame.anchor_source.value_counts().to_dict() if len(frame) else {},
        "expiry_close_source_counts": frame.expiry_close_source.value_counts().to_dict() if len(frame) else {},
        "expiry_source_counts": frame.expiry_source.value_counts().to_dict() if len(frame) else {},
        "rows_not_uploaded": True,
    }
    return frame, audit

def safe_div(a, b):
    return float(a / b) if b and np.isfinite(b) else np.nan

def rsi(values, n=14):
    x = pd.Series(values, dtype=float).dropna()
    if len(x) < n + 1:
        return np.nan
    delta = x.diff()
    up = delta.clip(lower=0).tail(n).mean()
    down = (-delta.clip(upper=0)).tail(n).mean()
    if down == 0:
        return 100.0 if up > 0 else 50.0
    return float(100 - 100 / (1 + up / down))

def engineer_features(bars: pd.DataFrame, labels: pd.DataFrame) -> pd.DataFrame:
    data = bars.sort_values("bar_start").copy()
    data["session_date"] = data.bar_start.dt.date
    daily = data.groupby("session_date").agg(open=("open", "first"), high=("high", "max"), low=("low", "min"), close=("close", "last"), bars=("close", "size"))
    daily["ret1"] = daily.close.pct_change()
    daily["tr"] = np.maximum(daily.high - daily.low, np.maximum((daily.high - daily.close.shift()).abs(), (daily.low - daily.close.shift()).abs()))
    features = []
    for _, label_row in labels.iterrows():
        day = pd.Timestamp(label_row.anchor_date).date()
        current = data[(data.session_date == day) & (data.bar_start.dt.strftime("%H:%M") <= "09:59")].sort_values("bar_start")
        if current.empty or current.iloc[-1].bar_start.strftime("%H:%M") != "09:59":
            continue
        p0 = float(current.iloc[-1].close)
        prev = daily[daily.index < day]
        if len(prev) < 25:
            continue
        closes = list(prev.close.astype(float)) + [p0]
        highs = list(prev.high.astype(float)) + [float(current.high.max())]
        lows = list(prev.low.astype(float)) + [float(current.low.min())]
        returns = pd.Series(closes, dtype=float).pct_change().dropna()
        tr_hist = list(prev.tr.dropna().astype(float)) + [float(current.high.max() - current.low.min())]
        atr14 = float(np.mean(tr_hist[-14:])) if len(tr_hist) >= 14 else np.nan
        close_arr = np.array(closes, dtype=float)
        current_open = float(current.iloc[0].open)
        abs_path = abs(float(current.iloc[0].close) - current_open)
        cs = current.close.astype(float).to_numpy()
        if len(cs) > 1:
            abs_path = abs(float(cs[0]) - current_open) + float(np.abs(np.diff(cs)).sum())
        prior_expiry_close = daily.loc[pd.Timestamp(label_row.previous_expiry).date(), "close"] if pd.Timestamp(label_row.previous_expiry).date() in daily.index else np.nan
        mean20 = float(np.mean(close_arr[-20:]))
        std20 = float(np.std(close_arr[-20:], ddof=1)) if len(close_arr) >= 20 else np.nan
        high20, low20 = float(max(highs[-20:])), float(min(lows[-20:]))
        feat = {
            "previous_expiry_return": p0 / float(prior_expiry_close) - 1 if pd.notna(prior_expiry_close) and prior_expiry_close > 0 else np.nan,
            "opening_window_return": p0 / current_open - 1 if current_open > 0 else np.nan,
            "opening_window_path_efficiency": abs(p0 - current_open) / abs_path if abs_path > 0 else 0.0,
            "opening_window_range_atr": safe_div(float(current.high.max() - current.low.min()), atr14),
            "anchor_gap_prev_close": p0 / float(prev.close.iloc[-1]) - 1,
            "atr14_pct": safe_div(atr14, p0),
            "rsi14": rsi(closes, 14),
            "ema5_gap": p0 / float(pd.Series(closes).ewm(span=5, adjust=False).mean().iloc[-1]) - 1,
            "ema10_gap": p0 / float(pd.Series(closes).ewm(span=10, adjust=False).mean().iloc[-1]) - 1,
            "ema20_gap": p0 / float(pd.Series(closes).ewm(span=20, adjust=False).mean().iloc[-1]) - 1,
            "macd12_26_pct": safe_div(float(pd.Series(closes).ewm(span=12, adjust=False).mean().iloc[-1] - pd.Series(closes).ewm(span=26, adjust=False).mean().iloc[-1]), p0),
            "bollinger_position20": safe_div(p0 - mean20, 2 * std20),
            "range_position20": safe_div(p0 - low20, high20 - low20),
            "aia_anchor_impulse_atr": safe_div((p0 / float(prior_expiry_close) - 1) if pd.notna(prior_expiry_close) and prior_expiry_close > 0 else np.nan, safe_div(atr14, p0)),
            "vsrp_volatility_scaled_range_position": safe_div(p0 - low20, high20 - low20),
            "tcd_trend_chop_divergence": safe_div(float(close_arr[-1] / close_arr[-11] - 1), float(np.abs(returns.tail(10)).sum())) if len(close_arr) >= 11 else np.nan,
            "weekdays_to_expiry": (pd.Timestamp(label_row.current_expiry).date() - day).days,
            "expiry_shift_regime_tuesday": int(pd.Timestamp(label_row.current_expiry).weekday() == 1),
        }
        for horizon in (1, 2, 3, 5, 10, 20):
            feat[f"return_{horizon}s"] = safe_div(close_arr[-1], close_arr[-1-horizon]) - 1 if len(close_arr) > horizon else np.nan
        for horizon in (5, 10, 20):
            feat[f"realized_vol_{horizon}s"] = float(returns.tail(horizon).std(ddof=1)) if len(returns) >= horizon else np.nan
        # MHDA: agreement among lagged multi-horizon returns, deterministic and point-in-time.
        signs = [np.sign(feat[f"return_{horizon}s"]) for horizon in (1, 3, 5, 10) if pd.notna(feat[f"return_{horizon}s"])]
        feat["mhda_directional_agreement"] = float(np.mean(signs)) if signs else np.nan
        feat["label"] = label_row.label
        feat["anchor_date"] = label_row.anchor_date
        feat["previous_expiry"] = label_row.previous_expiry
        feat["current_expiry"] = label_row.current_expiry
        features.append(feat)
    return pd.DataFrame(features)

def _balanced_accuracy(y_true, y_pred):
    from sklearn.metrics import balanced_accuracy_score
    if len(np.unique(y_true)) < 2:
        return np.nan
    return float(balanced_accuracy_score(y_true, y_pred))

def _rule_prediction(x_scaled, candidate):
    def condition(column, op, threshold):
        return x_scaled[:, int(column)] > float(threshold) if op == "gt" else x_scaled[:, int(column)] < float(threshold)
    first = condition(candidate["f1"], candidate["op1"], candidate["t1"])
    if candidate["mode"] == "single":
        signal = first
    else:
        second = condition(candidate["f2"], candidate["op2"], candidate["t2"])
        signal = np.logical_and(first, second) if candidate["mode"] == "and" else np.logical_or(first, second)
    pred = signal.astype(int)
    if candidate["invert"]:
        pred = 1 - pred
    return pred

def _candidate_key(candidate):
    return json.dumps(candidate, sort_keys=True, separators=(",", ":"))

def _mutate_candidate(candidate, rng, n_features, thresholds):
    child = dict(candidate)
    field = rng.choice(["f1", "op1", "t1", "mode", "invert", "f2", "op2", "t2"])
    if field in {"f1", "f2"}:
        child[field] = int(rng.integers(0, n_features))
    elif field in {"op1", "op2"}:
        child[field] = str(rng.choice(["gt", "lt"]))
    elif field in {"t1", "t2"}:
        child[field] = float(rng.choice(thresholds))
    elif field == "mode":
        child[field] = str(rng.choice(["single", "and", "or"]))
    else:
        child[field] = not bool(child[field])
    if child["mode"] == "single":
        child["f2"], child["op2"], child["t2"] = -1, "gt", 0.0
    elif child["f2"] < 0 or child["f2"] == child["f1"]:
        child["f2"] = int((child["f1"] + 1) % n_features)
    return child

def _new_candidate(rng, n_features, thresholds):
    mode = str(rng.choice(["single", "single", "and", "or"]))
    f1 = int(rng.integers(0, n_features))
    f2 = -1 if mode == "single" else int(rng.integers(0, n_features))
    if mode != "single" and f2 == f1:
        f2 = (f1 + 1) % n_features
    return {
        "f1": f1, "op1": str(rng.choice(["gt", "lt"])), "t1": float(rng.choice(thresholds)),
        "mode": mode, "f2": f2, "op2": str(rng.choice(["gt", "lt"])),
        "t2": float(rng.choice(thresholds)), "invert": bool(rng.integers(0, 2)),
    }

def _evolve_rule(x_train, y_train, x_valid, y_valid, feature_names, seed=1729, max_candidates=500, max_generations=20):
    rng = np.random.default_rng(seed)
    thresholds = [-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5]
    population_size = 32
    seen, archive, population = set(), [], []
    best_valid = -np.inf
    patience = 0
    generations_run = 0
    while generations_run < max_generations and len(seen) < max_candidates:
        generations_run += 1
        proposed = []
        if not population:
            proposed = [_new_candidate(rng, x_train.shape[1], thresholds) for _ in range(population_size)]
        else:
            elites = sorted(population, key=lambda row: row["train_fitness"], reverse=True)[:12]
            proposed = elites[:4]
            while len(proposed) < population_size:
                roll = rng.random()
                if roll < 0.50:
                    parent = elites[int(rng.integers(0, len(elites)))]["candidate"]
                    child = _mutate_candidate(parent, rng, x_train.shape[1], thresholds)
                elif roll < 0.80 and len(elites) >= 2:
                    a = elites[int(rng.integers(0, len(elites)))]["candidate"]
                    b = elites[int(rng.integers(0, len(elites)))]["candidate"]
                    child = dict(a)
                    for field in list(child):
                        if rng.random() < 0.5:
                            child[field] = b[field]
                    if child["mode"] == "single":
                        child["f2"], child["op2"], child["t2"] = -1, "gt", 0.0
                    elif child["f2"] < 0 or child["f2"] == child["f1"]:
                        child["f2"] = (child["f1"] + 1) % x_train.shape[1]
                else:
                    child = _new_candidate(rng, x_train.shape[1], thresholds)
                proposed.append(child)
        generation_best = -np.inf
        next_population = []
        for candidate in proposed:
            key = _candidate_key(candidate)
            if key in seen or len(seen) >= max_candidates:
                continue
            seen.add(key)
            train_pred = _rule_prediction(x_train, candidate)
            valid_pred = _rule_prediction(x_valid, candidate)
            train_ba = _balanced_accuracy(y_train, train_pred)
            valid_ba = _balanced_accuracy(y_valid, valid_pred)
            complexity = 1.0 if candidate["mode"] == "single" else 2.0
            train_fitness = (train_ba if np.isfinite(train_ba) else 0.0) - 0.001 * complexity
            record = {
                "candidate": candidate, "candidate_id": hashlib.sha1(key.encode()).hexdigest()[:12],
                "train_balanced_accuracy": float(train_ba) if np.isfinite(train_ba) else None,
                "validation_balanced_accuracy": float(valid_ba) if np.isfinite(valid_ba) else None,
                "train_fitness": float(train_fitness), "complexity": complexity,
                "feature_1": feature_names[int(candidate["f1"])],
                "feature_2": feature_names[int(candidate["f2"])] if candidate["mode"] != "single" else None,
                "generation": generations_run,
            }
            archive.append(record)
            next_population.append(record)
            if np.isfinite(valid_ba):
                generation_best = max(generation_best, float(valid_ba))
        population = sorted(next_population, key=lambda row: row["train_fitness"], reverse=True)[:population_size]
        if generation_best > best_valid + 1e-12:
            best_valid = generation_best
            patience = 0
        else:
            patience += 1
        if patience >= 3 or not population:
            break
    archive = sorted(archive, key=lambda row: (
        -((row["validation_balanced_accuracy"]) if row["validation_balanced_accuracy"] is not None else -1),
        row["complexity"], -row["train_fitness"]))
    winner = archive[0] if archive else None
    return {
        "status": "OK" if winner else "FAILED_NO_CANDIDATES",
        "method": "bounded typed-rule evolutionary search inspired by QuantEvolve quality-diversity; not the paper's multi-agent implementation",
        "seed": seed, "unique_candidates_evaluated": len(seen), "generations_run": generations_run,
        "population_size": population_size, "max_candidates": max_candidates, "max_generations": max_generations,
        "early_stop_patience_generations": patience, "selected_by_validation_only": winner,
        "top_candidates": archive[:25],
        "family_diversity": pd.Series([row["feature_1"].split("_")[0] for row in archive]).value_counts().to_dict() if archive else {},
        "_archive_internal": archive,
    }

def _block_bootstrap_diff(y_true, pred, baseline_pred, block_len=4, reps=1500, seed=1729):
    rng = np.random.default_rng(seed)
    n = len(y_true)
    if n < max(12, block_len * 2) or len(np.unique(y_true)) < 2:
        return {"status": "INSUFFICIENT_OOS", "block_length": block_len, "replicates_requested": reps}
    values = []
    for _ in range(reps):
        selected = []
        while len(selected) < n:
            start = int(rng.integers(0, n))
            selected.extend([(start + j) % n for j in range(block_len)])
        ix = np.asarray(selected[:n], dtype=int)
        if len(np.unique(y_true[ix])) < 2:
            continue
        candidate_ba = _balanced_accuracy(y_true[ix], pred[ix])
        baseline_ba = _balanced_accuracy(y_true[ix], baseline_pred[ix])
        if np.isfinite(candidate_ba) and np.isfinite(baseline_ba):
            values.append(candidate_ba - baseline_ba)
    if len(values) < max(100, reps // 3):
        return {"status": "INSUFFICIENT_VALID_RESAMPLES", "valid_replicates": len(values), "block_length": block_len}
    values = np.asarray(values)
    observed = _balanced_accuracy(y_true, pred) - _balanced_accuracy(y_true, baseline_pred)
    return {
        "status": "OK", "block_length": block_len, "valid_replicates": int(len(values)),
        "observed_balanced_accuracy_difference": float(observed),
        "difference_ci95": [float(np.quantile(values, .025)), float(np.quantile(values, .975))],
        "one_sided_p_improvement": float((1 + np.sum(values <= 0)) / (len(values) + 1)),
    }

def _holm_adjust(p_values):
    keys = list(p_values)
    valid = [(k, p) for k, p in p_values.items() if p is not None and np.isfinite(p)]
    ordered = sorted(valid, key=lambda item: item[1])
    adjusted = {}
    running = 0.0
    m = len(ordered)
    for rank, (key, p) in enumerate(ordered):
        value = min(1.0, (m - rank) * float(p))
        running = max(running, value)
        adjusted[key] = running
    for key in keys:
        adjusted.setdefault(key, None)
    return adjusted

def baseline_evaluation(feature_frame: pd.DataFrame) -> dict:
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
    from sklearn.dummy import DummyClassifier
    from sklearn.metrics import accuracy_score, balanced_accuracy_score, matthews_corrcoef, precision_recall_fscore_support, confusion_matrix, roc_auc_score, log_loss, brier_score_loss
    frame = feature_frame[feature_frame.label.isin(["UP", "DOWN"])].sort_values("anchor_date").reset_index(drop=True)
    if len(frame) < 120:
        return {"status": "DATA_LIMITED", "reason": "fewer than 120 usable binary labels after feature warm-up", "usable_labels": int(len(frame))}
    y = frame.label.map({"DOWN": 0, "UP": 1}).to_numpy()
    excluded = {"label", "anchor_date", "previous_expiry", "current_expiry"}
    feature_names = [c for c in frame.columns if c not in excluded]
    X = frame[feature_names].replace([np.inf, -np.inf], np.nan)
    n = len(frame)
    train_end, valid_end = int(n * 0.50), int(n * 0.70)  # reserve last 30% for a single chronological holdout
    X_train, y_train = X.iloc[:train_end], y[:train_end]
    X_valid, y_valid = X.iloc[train_end:valid_end], y[train_end:valid_end]
    X_test, y_test = X.iloc[valid_end:], y[valid_end:]
    imputer = SimpleImputer(strategy="median", keep_empty_features=True)
    scaler = StandardScaler()
    x_train = scaler.fit_transform(imputer.fit_transform(X_train))
    x_valid = scaler.transform(imputer.transform(X_valid))
    x_test = scaler.transform(imputer.transform(X_test))
    evolution = _evolve_rule(x_train, y_train, x_valid, y_valid, feature_names, seed=1729)
    models = {
        "majority": DummyClassifier(strategy="most_frequent"),
        "logistic": Pipeline([("imputer", SimpleImputer(strategy="median", keep_empty_features=True, add_indicator=True)), ("scale", StandardScaler()), ("model", LogisticRegression(C=0.1, max_iter=3000, class_weight=None, random_state=1729))]),
        "extra_trees": Pipeline([("imputer", SimpleImputer(strategy="median", keep_empty_features=True, add_indicator=True)), ("model", ExtraTreesClassifier(n_estimators=300, min_samples_leaf=5, max_features=0.8, class_weight="balanced", random_state=1729, n_jobs=2))]),
        "random_forest": Pipeline([("imputer", SimpleImputer(strategy="median", keep_empty_features=True, add_indicator=True)), ("model", RandomForestClassifier(n_estimators=300, min_samples_leaf=5, max_features=0.8, class_weight="balanced", random_state=1729, n_jobs=2))]),
    }
    validation, fitted = {}, {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        pred = model.predict(X_valid)
        validation[name] = {
            "balanced_accuracy": float(balanced_accuracy_score(y_valid, pred)),
            "accuracy": float(accuracy_score(y_valid, pred)),
            "mcc": float(matthews_corrcoef(y_valid, pred)),
        }
        fitted[name] = model
    if evolution.get("selected_by_validation_only"):
        candidate = evolution["selected_by_validation_only"]["candidate"]
        ev_pred = _rule_prediction(x_valid, candidate)
        validation["evolved_rule"] = {
            "balanced_accuracy": float(balanced_accuracy_score(y_valid, ev_pred)),
            "accuracy": float(accuracy_score(y_valid, ev_pred)),
            "mcc": float(matthews_corrcoef(y_valid, ev_pred)),
        }
    candidates = [name for name in validation if name != "majority"]
    chosen = max(candidates, key=lambda name: (validation[name]["balanced_accuracy"], validation[name]["mcc"]))
    # Fit each predeclared model family once on train+validation. This allows corrected secondary comparisons
    # while the primary model is chosen only using validation metrics. The test block is not used to tune.
    models["majority"].fit(X.iloc[:valid_end], y[:valid_end])
    test_predictions, test_probabilities, test_metrics, raw_p = {}, {}, {}, {}
    majority_pred = models["majority"].predict(X_test)
    for name, model in models.items():
        if name != "majority":
            model.fit(X.iloc[:valid_end], y[:valid_end])
            pred = model.predict(X_test)
            proba = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None
        else:
            pred, proba = majority_pred, None
        test_predictions[name] = pred
        if proba is not None:
            test_probabilities[name] = proba
        p, r, f1, _ = precision_recall_fscore_support(y_test, pred, labels=[0,1], zero_division=0)
        valid_ba = _balanced_accuracy(y_test, pred)
        test_metrics[name] = {
            "balanced_accuracy": float(valid_ba) if np.isfinite(valid_ba) else None,
            "accuracy": float(accuracy_score(y_test, pred)),
            "mcc": float(matthews_corrcoef(y_test, pred)),
            "precision_down_up": p.tolist(), "recall_down_up": r.tolist(), "f1_down_up": f1.tolist(),
            "confusion_matrix_down_up": confusion_matrix(y_test, pred, labels=[0,1]).tolist(),
            "roc_auc": float(roc_auc_score(y_test, proba)) if proba is not None and len(np.unique(y_test)) == 2 else None,
            "log_loss": float(log_loss(y_test, np.clip(proba, 1e-6, 1-1e-6), labels=[0,1])) if proba is not None and len(np.unique(y_test)) == 2 else None,
            "brier_score": float(brier_score_loss(y_test, proba)) if proba is not None and len(np.unique(y_test)) == 2 else None,
        }
        if name != "majority":
            raw_p[name] = _block_bootstrap_diff(y_test, pred, majority_pred, block_len=4, reps=1500, seed=1729 + len(raw_p)).get("one_sided_p_improvement")
    evolved_candidate = evolution.get("selected_by_validation_only")
    if evolved_candidate:
        ev_test_pred = _rule_prediction(x_test, evolved_candidate["candidate"])
        test_predictions["evolved_rule"] = ev_test_pred
        p, r, f1, _ = precision_recall_fscore_support(y_test, ev_test_pred, labels=[0,1], zero_division=0)
        ev_ba = _balanced_accuracy(y_test, ev_test_pred)
        test_metrics["evolved_rule"] = {
            "balanced_accuracy": float(ev_ba) if np.isfinite(ev_ba) else None,
            "accuracy": float(accuracy_score(y_test, ev_test_pred)),
            "mcc": float(matthews_corrcoef(y_test, ev_test_pred)),
            "precision_down_up": p.tolist(), "recall_down_up": r.tolist(), "f1_down_up": f1.tolist(),
            "confusion_matrix_down_up": confusion_matrix(y_test, ev_test_pred, labels=[0,1]).tolist(),
            "roc_auc": None, "log_loss": None, "brier_score": None,
            "probability_metrics_note": "not applicable; evolved rule returns a hard class only",
        }
        raw_p["evolved_rule"] = _block_bootstrap_diff(y_test, ev_test_pred, majority_pred, block_len=4, reps=1500, seed=1733).get("one_sided_p_improvement")
    adjusted = _holm_adjust(raw_p)
    comparison = {}
    for name, p_value in raw_p.items():
        comparison[name] = {
            "one_sided_p_improvement": p_value,
            "holm_adjusted_p": adjusted.get(name),
            "block_bootstrap_vs_majority": _block_bootstrap_diff(
                y_test, test_predictions[name], majority_pred, block_len=4, reps=1500, seed=1777 + len(comparison)
            ),
        }
    test_class_counts = pd.Series(y_test).map({0:"DOWN", 1:"UP"}).value_counts().to_dict()
    chosen_bootstrap = comparison.get(chosen, {}).get("block_bootstrap_vs_majority", {})
    selected_metrics = test_metrics.get(chosen, {})
    enough_test_classes = min(test_class_counts.get("DOWN", 0), test_class_counts.get("UP", 0)) >= 5
    gate = (
        len(y_test) >= 100
        and enough_test_classes
        and selected_metrics.get("balanced_accuracy") is not None
        and selected_metrics.get("balanced_accuracy", 0) > 0.5
        and selected_metrics.get("mcc", 0) > 0
        and chosen_bootstrap.get("difference_ci95", [0,0])[0] > 0
        and (adjusted.get(chosen) is not None and adjusted.get(chosen) < 0.05)
    )
    archive = evolution.pop("_archive_internal", [])
    return {
        "status": "EXPLORATORY_OOS_GATE_PASS" if gate else "OOS_GATE_NOT_PASSED_OR_INSUFFICIENT",
        "note": "The final chronological quarter is reserved from training. This is a first automated research run; independent verification and source integrity gates remain mandatory.",
        "total_binary_labels": int(n), "train_labels": int(train_end), "validation_labels": int(valid_end-train_end),
        "sealed_test_labels": int(n-valid_end), "test_class_counts": test_class_counts,
        "test_period_start": str(frame.anchor_date.iloc[valid_end]), "test_period_end": str(frame.anchor_date.iloc[-1]),
        "selected_model_by_validation_only": chosen, "validation_metrics": validation,
        "test_metrics_by_model": test_metrics, "multiple_comparison_adjusted_tests_vs_majority": comparison,
        "selected_model_test_metrics": selected_metrics, "selected_model_bootstrap_vs_majority": chosen_bootstrap,
        "exploratory_gate_pass": bool(gate), "features": feature_names, "feature_count": int(X.shape[1]),
        "evolution_summary": {k:v for k,v in evolution.items() if k != "_archive_internal"},
        "evolution_archive_count": len(archive), "evolution_candidate_archive": archive[:500],
        "limitations": [
            "This is preliminary research evidence, not a final decision until source/candle/expiry audits and independent tester gate pass.",
            "Block bootstrap is a circular moving-block approximation; block lengths 2 and 8 and seed sensitivity remain to be run.",
            "Historical exchange/public data provenance and official expiry coverage must be checked before accepting any metric.",
            "Hard prediction accuracy is not a trading strategy or profitability estimate."
        ],
    }

def run(args):
    REPORTS.mkdir(parents=True, exist_ok=True)
    CACHE.mkdir(parents=True, exist_ok=True)
    force = bool(args.refresh_data)
    pub_files, pub_manifest = acquire_public(force=force)
    public_bars, public_audit = read_public(pub_files)
    if public_bars.empty:
        raise RuntimeError("no usable public NIFTY 50 intraday bars acquired")
    dhan_bars, dhan_audit = acquire_dhan(force=force)
    source_comparison = {"status": "NOT_AVAILABLE"}
    if not dhan_bars.empty:
        left = public_bars[["bar_start","close"]].rename(columns={"close":"public_close"})
        right = dhan_bars[["bar_start","close"]].rename(columns={"close":"dhan_close"})
        overlap = left.merge(right, on="bar_start", how="inner")
        if len(overlap):
            diff = (overlap.public_close - overlap.dhan_close).abs()
            source_comparison = {
                "status": "OVERLAP_AUDITED", "overlap_bars": int(len(overlap)),
                "median_abs_price_difference": float(diff.median()), "p95_abs_price_difference": float(diff.quantile(.95)),
                "within_1_point_fraction": float((diff <= 1.0).mean()), "within_5_points_fraction": float((diff <= 5.0).mean()),
                "public_source": "technovusin/nifty50-historical-data", "secondary_source": "Dhan Historical Intraday",
            }
            # Prefer Dhan only where overlap matches well; otherwise keep public canonical and quarantine discrepancies.
            if source_comparison["within_1_point_fraction"] >= 0.995:
                public_bars = public_bars[~public_bars.bar_start.isin(set(overlap.bar_start))]
                bars = pd.concat([public_bars, dhan_bars], ignore_index=True).drop_duplicates("bar_start", keep="last").sort_values("bar_start").reset_index(drop=True)
                source_comparison["merge_policy"] = "Dhan preferred for overlapped timestamps after >=99.5% within one index point; public source outside overlap"
            else:
                bars = public_bars
                source_comparison["merge_policy"] = "overlap failed the predeclared agreement gate; public bars kept, Dhan mismatch quarantined"
        else:
            bars = public_bars
            source_comparison["status"] = "NO_OVERLAP"
    else:
        bars = public_bars
        source_comparison["merge_policy"] = "public source only; Dhan data unavailable"
    bars = bars.drop_duplicates("bar_start", keep="last").sort_values("bar_start").reset_index(drop=True)
    bars["session_date"] = bars.bar_start.dt.date
    expiries, expiry_audit = get_expiry_calendar(set(bars.session_date))
    labels, label_audit = make_target_rows(bars, expiries, expiry_audit)
    features = engineer_features(bars, labels) if len(labels) else pd.DataFrame()
    # Never upload raw source bars or per-week price labels into public artifacts.
    reports = {
        "research_id": "NWCP-1.0", "run_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "source_summary": {
            "public_files_available": len(pub_files), "public_file_manifest": pub_manifest,
            "public_bars_audit": public_audit, "dhan_audit": dhan_audit, "source_comparison": source_comparison,
            "canonical_bars": int(len(bars)), "first_bar": str(bars.bar_start.min()), "last_bar": str(bars.bar_start.max()),
            "session_count": int(bars.session_date.nunique()), "cache_namespace": str(CACHE.relative_to(ROOT)),
        },
        "expiry_audit": expiry_audit, "label_audit": label_audit,
        "feature_audit": {
            "status": "OK" if len(features) else "BLOCKED_NO_FEATURES",
            "feature_rows": int(len(features)), "feature_columns": [c for c in features.columns if c not in {"label","anchor_date","previous_expiry","current_expiry"}],
            "features_missing_over_50pct": features.drop(columns=["label","anchor_date","previous_expiry","current_expiry"], errors="ignore").isna().mean()[lambda s: s > .5].to_dict() if len(features) else {},
        },
    }
    if len(features) >= 120:
        reports["baseline_results"] = baseline_evaluation(features)
    else:
        reports["baseline_results"] = {"status": "BLOCKED_DATA_LIMITED", "usable_feature_rows": int(len(features)), "required_rows": 120}
    json_write(REPORTS / "source_manifest.json", {"public": pub_manifest, "dhan": dhan_audit, "source_comparison": source_comparison})
    json_write(REPORTS / "data_quality_audit.json", reports)
    summary = [
        "# NWCP-1.0 Automated Data and Baseline Audit", "",
        "This report contains sanitized aggregate statistics only. Raw intraday prices and per-expiry target rows are deliberately not uploaded.", "",
        f"- Run: {reports['run_utc']}",
        f"- Canonical 1-minute bars: {len(bars):,}",
        f"- Sessions: {bars.session_date.nunique():,}",
        f"- Valid labels: {label_audit.get('valid_labels', 0):,}; excluded intervals: {label_audit.get('excluded_intervals', 0):,}",
        f"- Expiry source status: {expiry_audit.get('source')}; official expiries: {expiry_audit.get('official_expiry_count', 0)}; fallback expiries: {expiry_audit.get('fallback_expiry_count', 0)}",
        f"- Feature rows after warm-up: {len(features):,}",
        f"- Dhan: {dhan_audit.get('status')}; source overlap: {source_comparison.get('status')}",
        f"- Baseline run status: {reports['baseline_results'].get('status')}",
        "", "## Important limitation", "",
        "This first workflow is a data-quality and exploratory model run. A positive test score is not a scientific conclusion until blocked-bootstrap confidence intervals, multiple-comparison controls, regime robustness, no-leakage checks, and the separate independent tester gate are completed.", "",
    ]
    (REPORTS / "RESULTS.md").write_text("\n".join(summary), encoding="utf-8")
    log(f"valid labels={label_audit.get('valid_labels', 0)}, features={len(features)}, decision status={reports['baseline_results'].get('status')}")
    if not len(labels):
        raise RuntimeError("target construction produced zero usable weekly labels; downstream claims must remain blocked")
    return reports

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["all", "data"], default="all")
    parser.add_argument("--refresh-data", action="store_true")
    args = parser.parse_args()
    try:
        run(args)
    except Exception as exc:
        REPORTS.mkdir(parents=True, exist_ok=True)
        json_write(REPORTS / "runtime_error.json", {
            "research_id": "NWCP-1.0", "status": "FAILED",
            "error_type": type(exc).__name__, "error": str(exc)[:400],
            "traceback_tail": traceback.format_exc()[-2500:], "timestamp_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        })
        raise

if __name__ == "__main__":
    main()
