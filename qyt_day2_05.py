import re

# 定义字符串
str1 = 'Port-channel1.189    192.168.189.254 YES   CONFIG  up'

# 使用正则表达式匹配模式
# 匹配接口名（非空白字符开头，可能包含点号和数字）
# 匹配IP地址（四组数字，每组1-3位，用点号分隔）
# 匹配状态（up或down）
pattern = r'^(\S+)\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+\w+\s+\w+\s+(up|down)'

# 进行匹配
match = re.search(pattern, str1)

if match:
    # 提取匹配的组
    interface = match.group(1)
    ip_address = match.group(2)
    status = match.group(3)

    # 格式化打印结果
    print("接口    :", interface)
    print("IP地址  :", ip_address)
    print("状态    :", status)
else:
    print("未找到匹配的信息")