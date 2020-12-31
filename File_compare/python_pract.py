first = 0
"""while(first<10):
    print("outside", first)
    first += 1
    while(first<5):
        first += 1
        print("inside",first)

"""
import uuid, secrets

print(uuid.uuid4())
key = secrets.token_hex(5)
print(key)

