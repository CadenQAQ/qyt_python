import re

str_line = 'TCP server 172.16.1.101:443 localserver 172.16.66.1:53710, idle 0:01:09, bytes 27575949, flags UIO'

# 使用正则表达式匹配各个部分
pattern = r'TCP server (\d+\.\d+\.\d+\.\d+:\d+) localserver (\d+\.\d+\.\d+\.\d+:\d+), idle ([\d:]+), bytes (\d+), flags (\w+)'
match = re.search(pattern, str_line)

if match:
    server_addr = match.group(1)
    local_addr = match.group(2)
    idle_time = match.group(3)
    bytes_count = match.group(4)
    flags = match.group(5)

    # 将 idle 时间格式转换为 "0 小时 01分钟 09秒" 格式
    idle_parts = idle_time.split(':')
    if len(idle_parts) == 3:
        hours, minutes, seconds = idle_parts
        idle_formatted = f"{hours} 小时 {minutes}分钟 {seconds}秒"
    else:
        idle_formatted = idle_time

    # 创建字典
    output = {
        "Protocol": "TCP",
        "server": server_addr,
        "localserver": local_addr,
        "idle": idle_formatted,
        "bytes": bytes_count,
        "flags": flags
    }

    # 按照指定格式输出
    for key, value in output.items():
        print(f"{key.ljust(12)}: {value}")
else:
    print("未找到匹配的内容")