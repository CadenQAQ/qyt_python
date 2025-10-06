from qyt_day8_03 import qytang_ping
from qyt_day9_01 import qytang_ssh
import re
import pprint


def qytang_get_if(ips, username='admin', password='Cisc0123'):
    """
    获取多个设备的接口信息
    参数:
        ips: IP地址列表或单个IP地址字符串
    返回:
        字典格式的设备接口信息 {ip: {interface: ip_address}}
    """
    device_if_dict = {}

    # 如果传入的是单个IP地址字符串，转换为列表
    if isinstance(ips, str):
        ips = [ips]

    for ip in ips:
        # 首先尝试Ping设备
        if qytang_ping(ip):
            print(f"{ip} 通，开始采集接口信息...")

            # SSH登录设备并执行显示接口IP地址的命令
            # 使用'show ip interface brief'命令来获取接口信息
            try:
                cmd_output = qytang_ssh(ip, username, password, cmd='show ip interface brief')

                # 解析命令输出，提取接口和IP地址信息
                interface_dict = {}
                for line in cmd_output.split('\n'):
                    # 使用正则表达式匹配接口和IP地址
                    # 格式示例: GigabitEthernet0/0    192.168.1.1    YES manual up    up
                    re_result = re.match(r'^(\S+)\s+(\d+\.\d+\.\d+\.\d+)\s+', line)
                    if re_result:
                        interface = re_result.groups()[0]
                        ip_address = re_result.groups()[1]
                        # 排除未分配IP地址的接口（显示为unassigned）
                        if ip_address != 'unassigned':
                            interface_dict[interface] = ip_address

                # 将解析结果添加到主字典中
                device_if_dict[ip] = interface_dict
                print(f"{ip} 接口信息采集完成")

            except Exception as e:
                print(f"SSH连接或命令执行失败: {e}")
                device_if_dict[ip] = {}
        else:
            print(f"{ip} 不通，跳过此设备")
            device_if_dict[ip] = {}

    return device_if_dict


if __name__ == '__main__':
    # 测试函数
    ips_to_check = ['192.168.1.1', '192.168.136.1']
    result = qytang_get_if(ips_to_check, username='ubiq', password='Ubiqnetwork@1024')
    pprint.pprint(result, indent=4)