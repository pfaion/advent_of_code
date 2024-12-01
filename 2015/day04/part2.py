from hashlib import md5
from itertools import count

data = "iwrupvqb"
target_prefix = "0" * 6

for n in count():
    hashee = f"{data}{n}"
    hashed = md5(hashee.encode()).hexdigest()
    if hashed.startswith(target_prefix):
        print(n)
        break
