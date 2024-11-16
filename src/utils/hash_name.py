import hashlib

def hash_name(name):
  hashed_name = hashlib.sha256(name.encode()).hexdigest()
  return hashed_name