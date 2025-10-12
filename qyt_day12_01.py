from qyt_day11_01 import qytang_ssh_c8k
import pexpect
import time


def qytang_multicmd(ip, username, password, cmd_list, enable='', wait_time=2, verbose=True):
    """
    执行多条路由器配置命令

    参数:
    ip: 设备IP地址
    username: 用户名
    password: 密码
    cmd_list: 命令列表，如 ['show version', 'show running-config']
    enable: enable密码，如果没有则为空字符串
    wait_time: 等待设备返回的时间
    verbose: 是否打印设备返回信息
    """
    try:
        # 建立SSH连接
        if verbose:
            print(f"正在连接设备 {ip}...")

        child = pexpect.spawn(f'ssh -o StrictHostKeyChecking=no {username}@{ip}', timeout=30, encoding='utf-8',
                              codec_errors='ignore')

        # 处理登录过程
        login_result = child.expect(['password:', 'Password:', pexpect.TIMEOUT, pexpect.EOF])
        if login_result == 0 or login_result == 1:
            child.sendline(password)
        else:
            raise Exception(f"SSH连接失败: 未收到密码提示")

        # 等待登录成功，检查是否需要enable
        login_check = child.expect(['#', '>', pexpect.TIMEOUT], timeout=10)

        # 如果需要enable密码且提供了enable密码
        if login_check == 1 and enable:
            if verbose:
                print("检测到需要enable权限，正在进入特权模式...")
            child.sendline('enable')
            child.expect(['Password:', 'password:'])
            child.sendline(enable)
            child.expect('#', timeout=10)
        elif login_check == 1 and not enable:
            raise Exception("设备需要enable密码，但未提供enable参数")

        # 禁用分页（对所有命令都执行，避免分页影响）
        child.sendline('terminal length 0')
        child.expect(['#', '>'], timeout=5)

        all_output = []  # 存储所有命令的输出

        # 逐条执行命令
        for i, cmd in enumerate(cmd_list):
            if verbose:
                print(f"\n执行命令 {i + 1}/{len(cmd_list)}: {cmd}")

            child.sendline(cmd)

            # 等待命令执行完成
            child.expect(['#', '>', pexpect.TIMEOUT], timeout=wait_time)

            # 获取命令输出
            cmd_output = child.before.strip()

            # 移除命令回显本身
            lines = cmd_output.split('\n')
            if lines and cmd in lines[0]:
                cmd_output = '\n'.join(lines[1:]).strip()

            all_output.append({
                'command': cmd,
                'output': cmd_output
            })

            if verbose:
                print(f"命令输出:\n{cmd_output}")
                print("-" * 50)

            # 命令间短暂停顿
            time.sleep(0.5)

        # 退出设备
        child.sendline('exit')
        child.expect(pexpect.EOF)
        child.close()

        if verbose:
            print(f"\n所有命令执行完成！")

        return all_output

    except pexpect.TIMEOUT:
        if 'child' in locals():
            child.close()
        raise Exception("连接或命令执行超时")
    except pexpect.EOF:
        if 'child' in locals():
            child.close()
        raise Exception("连接意外中断")
    except Exception as e:
        if 'child' in locals():
            child.close()
        raise Exception(f"执行过程中出错: {str(e)}")


if __name__ == "__main__":
    # 测试要求：一次执行show version(必须完整内容)和配置ospf process 1并宣告一个网络

    # 测试命令列表
    cmd_list = [
        'show version',  # 必须完整内容
        'configure terminal',
        'router ospf 1',
        'network 192.168.1.0 0.0.0.255 area 0',
        'end',
        'show ip protocols'  # 验证OSPF配置
    ]

    print("=" * 60)
    print("测试 qytang_multicmd 函数")
    print("执行命令: show version 和 配置OSPF process 1")
    print("=" * 60)

    try:
        # 使用qytang_multicmd函数执行命令
        results = qytang_multicmd(
            ip='192.168.136.1',
            username='ubiq',
            password='admin123',
            cmd_list=cmd_list,
            enable='',  # 根据实际情况填写enable密码
            wait_time=3,
            verbose=True
        )

        print("\n" + "=" * 60)
        print("执行结果汇总")
        print("=" * 60)

        # 显示每个命令的执行结果摘要
        for i, result in enumerate(results):
            print(f"\n命令 {i + 1}: {result['command']}")
            print(f"输出长度: {len(result['output'])} 字符")

            # 特别验证show version的完整性
            if result['command'] == 'show version':
                required_keywords = ['Version', 'image', 'uptime', 'processor']
                missing = [kw for kw in required_keywords if kw.lower() not in result['output'].lower()]
                if not missing:
                    print("✅ show version 输出完整")
                else:
                    print(f"❌ show version 可能不完整，缺少: {missing}")

            # 验证OSPF配置
            elif result['command'] == 'show ip protocols':
                if 'ospf 1' in result['output'].lower():
                    print("✅ OSPF进程1配置成功")
                    if '192.168.1.0' in result['output']:
                        print("✅ 网络192.168.1.0/24宣告成功")
                else:
                    print("❌ OSPF配置可能未生效")

            # 显示输出预览
            preview = result['output'][:150] + "..." if len(result['output']) > 150 else result['output']
            print(f"输出预览: {preview}")
            print("-" * 40)

    except Exception as e:
        print(f"执行过程中出错: {e}")