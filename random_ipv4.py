import random

def random_ipv4():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

print(random_ipv4())