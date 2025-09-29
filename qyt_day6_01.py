import re

asa_conn = """TCP Student 192.168.189.167:32806 Teacher 137.78.5.128:65247, idle 0:00:00, bytes 74, flags UIO
TCP Student 192.168.189.167:80 Teacher 137.78.5.128:65233, idle 0:00:03, bytes 334516, flags UIO"""

asa_dict = {}
# 匹配协议 + 源IP:端口 + 目的IP:端口 + bytes + flags
pattern = re.compile(
    r'(?P<proto>\w+)\s+\S+\s+(?P<src_ip>[\d.]+):(?P<src_port>\d+)\s+\S+\s+(?P<dst_ip>[\d.]+):(?P<dst_port>\d+).*?bytes\s+(?P<bytes>\d+),\s+flags\s+(?P<flags>\S+)'
)

for conn in asa_conn.strip().split('\n'):
    re_result = pattern.match(conn.strip())
    if re_result:
        key = (
            re_result["src_ip"],
            re_result["src_port"],
            re_result["dst_ip"],
            re_result["dst_port"],
        )
        asa_dict[key] = {
            "proto": re_result["proto"],
            "bytes": re_result["bytes"],
            "flags": re_result["flags"],
        }

print("打印分析后的字典：\n")
print(asa_dict)

print("\n格式化打印输出\n")
for (src_ip, src_port, dst_ip, dst_port), info in asa_dict.items():
    print(f"{'src':<8}: {src_ip:<15} | {'src_port':<8}: {src_port:<8} | {'dst':<8}: {dst_ip:<15} | {'dst_port':<8}: {dst_port:<8}")
    print(f"{'bytes':<8}: {info['bytes']:<15} | {'flags':<8}: {info['flags']:<8}")
    print("=" * 100)

port_list = ['eth 1/101/1/42',
             'eth 1/101/1/26',
             'eth 1/101/1/23',
             'eth 1/101/1/7',
             'eth 1/101/2/46',
             'eth 1/101/1/34','eth 1/101/1/18','eth 1/101/1/13','eth 1/101/1/32','eth 1/101/1/25','eth 1/101/1/45','eth 1/101/2/8']

sorted_list = sorted(port_list, key=lambda x: list(map(int, x.replace("eth ","").split("/"))))

print(sorted_list)