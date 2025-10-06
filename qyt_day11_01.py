import hashlib
import time
import pexpect


def qytang_ssh_c8k(ip, username, password, cmd='show running-config'):
    """SSH连接函数，支持参数传递"""
    try:
        child = pexpect.spawn(f'ssh -o StrictHostKeyChecking=no {username}@{ip}', timeout=30)

        # 登录
        child.expect(['password:', 'Password:'])
        child.sendline(password)
        child.expect(['#', '>'])

        # 如果是show命令，先禁用分页
        if cmd.startswith('show'):
            child.sendline('terminal length 0')
            child.expect(['#', '>'])

        # 执行命令
        child.sendline(cmd)
        child.expect(['#', '>'], timeout=20)

        output = child.before.decode('utf-8', errors='ignore')

        # 退出
        child.sendline('exit')
        child.expect(pexpect.EOF)
        child.close()

        return output

    except Exception as e:
        print(f"SSH执行错误: {e}")
        return None


def extract_running_config(full_output):
    """从完整输出中提取 running-config 部分"""
    if not full_output:
        return None

    # 查找 hostname 开始位置
    hostname_start = full_output.find('hostname')
    if hostname_start == -1:
        print("未找到配置起始位置")
        return None

    # 查找 end 结束位置
    end_pos = full_output.find('end', hostname_start)
    if end_pos == -1:
        print("未找到配置结束位置")
        return None

    # 提取配置部分 (包含 'end')
    config = full_output[hostname_start:end_pos + 3]  # +3 包含 'end'
    return config.strip()


def calculate_config_hash(config):
    """计算配置的哈希值"""
    if not config:
        return None
    return hashlib.md5(config.encode('utf-8')).hexdigest()


def qytang_check_diff(ip, username, password):
    """检查配置变化的函数 - 检测到变化就退出"""
    print(f"开始监控设备 {ip} 的配置变化...")
    print("按 Ctrl+C 停止监控\n")

    # 获取初始配置和哈希值
    initial_output = qytang_ssh_c8k(ip, username, password)
    initial_config = extract_running_config(initial_output)

    if not initial_config:
        print("无法获取初始配置，退出监控")
        return

    initial_hash = calculate_config_hash(initial_config)
    print(f"初始配置哈希值: {initial_hash}")
    print("配置监控中...\n")

    check_count = 0

    while True:
        try:
            time.sleep(5)
            check_count += 1
            # 获取当前配置
            current_output = qytang_ssh_c8k(ip, username, password)
            current_config = extract_running_config(current_output)

            if not current_config:
                print(f"第 {check_count} 次检查: 无法获取配置")
                continue

            current_hash = calculate_config_hash(current_config)

            if current_hash != initial_hash:
                print(f"MD5 value changed")
                print(f"新的MD5值: {current_hash}")
                print("🚨 配置发生变化，退出监控")
                return current_hash
            else:
                print(f"第 {check_count} 次检查 - MD5值: {current_hash}")

        except KeyboardInterrupt:
            print("\n\n监控已停止")
            break
        except Exception as e:
            print(f"第 {check_count} 次检查时发生错误: {e}")
            continue


def get_single_config(ip, username, password):
    """获取单次配置并显示哈希值"""
    print(f"获取设备 {ip} 的配置...")
    output = qytang_ssh_c8k(ip, username, password)
    config = extract_running_config(output)

    if config:
        config_hash = calculate_config_hash(config)
        print("配置获取成功!")
        print(f"配置MD5值: {config_hash}")
        return config, config_hash
    else:
        print("配置获取失败")
        return None, None


if __name__ == '__main__':
    ip = '192.168.136.1'
    username = 'admin'
    password = 'cisco123'

    # 测试单次获取配置
    print("测试单次配置获取:")
    config, hash_value = get_single_config(ip, username, password)

    if config:
        print("\n开始持续监控配置变化...")
        new_hash = qytang_check_diff(ip, username, password)
        if new_hash:
            print(f"最终检测到的新配置MD5值: {new_hash}")
    else:
        print("无法获取配置，无法启动监控")