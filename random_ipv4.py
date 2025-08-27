import random

def random_ipv4():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

# 生成 10 个随机 IPv4 地址
for _ in range(10):
    print(random_ipv4())