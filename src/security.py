import hashlib
import hmac
import os


def verify_meta_signature(raw_body: bytes, signature_header: str | None) -> bool:
    app_secret = os.getenv("META_APP_SECRET")

    if not app_secret or not signature_header:
        return False

    expected_signature = hmac.new(
        key=app_secret.encode("utf-8"),
        msg=raw_body,
        digestmod=hashlib.sha256,
    ).hexdigest()

    expected_header = f"sha256={expected_signature}"

    return hmac.compare_digest(expected_header, signature_header)
