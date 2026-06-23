import random

from app.core.security import create_access_token, decode_access_token

code = str(random.randint(100000, 999999))
print(code)
