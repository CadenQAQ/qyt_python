from netmiko import ConnectHandler
import time


def qytang_ssh_netmiko(ip, username, password, cmd='show ip route'):
    """使用netmiko连接网络设备"""
    try:
        # 定义设备参数
        device = {
            'device_type': 'cisco_ios',  # 根据你的设备类型选择
            'ip': ip,
            'username': username,
            'password': password,
            'port': 22,
            'timeout': 30,
            'session_timeout': 30
        }

        print(f"连接到 {ip}...")

        # 建立连接
        connection = ConnectHandler(**device)

        # 进入enable模式
        connection.enable()

        # 禁用分页
        connection.send_command('terminal length 0')

        # 执行命令
        output = connection.send_command(cmd)

        # 断开连接
        connection.disconnect()

        print("✓ 命令执行成功")
        return output

    except Exception as e:
        print(f"Netmiko错误: {e}")
        return None


if __name__ == '__main__':
    result = qytang_ssh_netmiko("192.168.136.1", "ubiq", "Ubiqnetwork@1024")
    if result:
        print(result)