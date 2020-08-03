# hash
import hashlib

obj = hashlib.md5('salt'.encode())

obj.update('hello'.encode())

print(obj.hexdigest())
