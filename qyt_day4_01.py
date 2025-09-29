import os
import re
ifconfig_result = os.popen('ifconfig '+'ens160').read()
#print(ifconfig_result)

# 定义正则表达式来提取所需信息
ipv4_regex = r"inet (\d+\.\d+\.\d+\.\d+)"
netmask_regex = r"netmask (\d+\.\d+\.\d+\.\d+)"
broadcast_regex = r"broadcast (\d+\.\d+\.\d+\.\d+)"
mac_addr_regex = r"ether ([0-9a-fA-F:]{17})"

ipv4_add = re.findall(ipv4_regex, ifconfig_result)
netmask = re.findall(netmask_regex, ifconfig_result)
broadcast = re.findall(broadcast_regex, ifconfig_result)
mac_addr = re.findall(mac_addr_regex, ifconfig_result)

# 格式化输出并确保冒号对齐
print(f"{'IPv4 Address':<15}: {ipv4_add[0] if ipv4_add else 'Not Found'}")
print(f"{'Netmask':<15}: {netmask[0] if netmask else 'Not Found'}")
print(f"{'Broadcast':<15}: {broadcast[0] if broadcast else 'Not Found'}")
print(f"{'MAC Address':<15}: {mac_addr[0] if mac_addr else 'Not Found'}")

# 提取网段部分并计算 .2 网关地址
if ipv4_add:
    # 获取IPv4地址的前三个部分（即网段）
    ipv4_parts = ipv4_add[0].split('.')[:-1]  # 获取前三个部分
    ipv4_gw = '.'.join(ipv4_parts) + '.2'  # 拼接 .2，得到网关地址

ping_result=os.popen('ping '+ipv4_gw+' -c 1').read()
#print(ping_result)
re_ping_result = re.search(r'bytes from', ping_result)

print("我们假设网关IP地址最后一位为2,因此网关IP地址为:"+str(ipv4_gw))
# 判断网关是否可达
if re_ping_result:
    print("网关可达")
else:
    print("网关不可达")