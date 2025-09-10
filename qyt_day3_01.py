import re

str_line = '166 54a2.74f7.0326 DYNAMIC Gi1/0/11'

# 使用正则表达式匹配各个部分
pattern = r'(\d+)\s+([0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4})\s+(\w+)\s+(\S+)'
match = re.search(pattern, str_line)

if match:
    vlan_id = match.group(1)
    mac_addr = match.group(2)
    mac_type = match.group(3)
    interface = match.group(4)

    # 创建字典
    output = {
        "VLAN ID": vlan_id,
        "MAC": mac_addr,
        "Type": mac_type,
        "Interface": interface
    }

    # 输出字典的键值对
    for key, value in output.items():
        print(f"{key}: {value}")
else:
    print("未找到匹配的内容")