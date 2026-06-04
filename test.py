import hashlib
import hmac

secret = "my-secret"

body = b"{'message':'hello'}"

signature = hmac.new(
    key=secret.encode(), msg=body, digestmod=hashlib.sha256
).hexdigest()


print("sha256=" + signature)
