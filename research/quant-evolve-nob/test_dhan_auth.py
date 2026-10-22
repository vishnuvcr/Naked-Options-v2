import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("dhan_auth.py")
spec = importlib.util.spec_from_file_location("dhan_auth", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def test_totp_rfc6238_sha1_vectors():
    # RFC 6238 SHA-1 test secret encoded as base32: GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ
    secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"
    assert module.totp(secret, now=59) == "287082"
    assert module.totp(secret, now=1111111109) == "081804"

def test_totp_is_six_digits_and_changes_with_time():
    secret = "GEZDGNBVGY3TQOJQGEZDGNBVGY3TQOJQ"
    assert len(module.totp(secret, now=30)) == 6
    assert module.totp(secret, now=30) != module.totp(secret, now=60)
