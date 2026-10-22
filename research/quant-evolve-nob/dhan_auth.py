#!/usr/bin/env python3
"""Generate and validate a fresh Dhan 24-hour token using the account's TOTP seed.

Secrets are read only from environment variables and the token is written only to
GITHUB_ENV after /profile validates it. No credential or token is printed.
"""
from __future__ import annotations
import base64, hashlib, hmac, json, os, struct, sys, time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

AUTH_URL = "https://auth.dhan.co/app/generateAccessToken"
PROFILE_URL = "https://api.dhan.co/v2/profile"

def totp(secret: str, now: float | None = None) -> str:
    normalized = "".join(secret.strip().replace(" ", "").upper().split())
    key = base64.b32decode(normalized + "=" * ((8 - len(normalized) % 8) % 8), casefold=True)
    counter = int((time.time() if now is None else now) // 30)
    digest = hmac.new(key, struct.pack(">Q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    number = (struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7fffffff) % 1_000_000
    return f"{number:06d}"

def request_json(url: str, headers: dict[str, str] | None = None) -> dict:
    req = Request(url, headers=headers or {}, method="GET")
    try:
        with urlopen(req, timeout=20) as response:
            raw = response.read()
            if response.status != 200:
                raise RuntimeError(f"HTTP {response.status}")
            value = json.loads(raw)
            if not isinstance(value, dict):
                raise RuntimeError("Unexpected response format")
            return value
    except HTTPError as exc:
        # Never include response body: authentication endpoints may echo sensitive data.
        raise RuntimeError(f"Dhan authentication request failed with HTTP {exc.code}") from None
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Dhan authentication request failed ({type(exc).__name__})") from None

def main() -> int:
    client_id = os.getenv("DHAN_CLIENT_ID", "").strip()
    pin = os.getenv("DHAN_PIN", "").strip()
    seed = os.getenv("DHAN_TOTP_SECRET", "").strip()
    envfile = os.getenv("GITHUB_ENV", "")
    if not all((client_id, pin, seed, envfile)):
        print("ERROR: configure DHAN_CLIENT_ID, DHAN_PIN and DHAN_TOTP_SECRET repository Actions secrets.", file=sys.stderr)
        return 2
    try:
        otp = totp(seed)
        payload = request_json(AUTH_URL + "?" + urlencode({"dhanClientId": client_id, "pin": pin, "totp": otp}))
        token = payload.get("accessToken")
        returned_id = str(payload.get("dhanClientId", ""))
        if not isinstance(token, str) or not token.strip():
            print("ERROR: Dhan token-generation response did not contain accessToken.", file=sys.stderr)
            return 3
        if returned_id and returned_id != client_id:
            print("ERROR: Dhan returned a client ID that does not match DHAN_CLIENT_ID.", file=sys.stderr)
            return 4
        profile = request_json(PROFILE_URL, {"access-token": token})
        if str(profile.get("dhanClientId", "")) != client_id:
            print("ERROR: fresh token profile validation failed or client ID mismatched.", file=sys.stderr)
            return 5
        # GitHub Actions environment files are line-oriented; JWTs must be a single line.
        if any(ch in token for ch in "\r\n"):
            print("ERROR: malformed token response.", file=sys.stderr)
            return 6
        with open(envfile, "a", encoding="utf-8") as out:
            out.write("DHAN_ACCESS_TOKEN=" + token + "\n")
        expiry = payload.get("expiryTime", "not provided")
        print(f"Dhan token generated and /profile validated for client {client_id}; expiryTime={expiry}. Token value suppressed.")
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
