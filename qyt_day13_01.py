import subprocess
import platform
import re


class QYTPING:
    def __init__(self, dstip, srcip=None, length=100):
        self.dstip = dstip
        self.srcip = srcip
        self.length = length

    def __str__(self):
        if self.srcip:
            return f"<QYTPING => srcip: {self.srcip}, dstip: {self.dstip}, size: {self.length}>"
        else:
            return f"<QYTPING => dstip: {self.dstip}, size: {self.length}>"

    def one(self):
        """Ping一个包判断可达性"""
        try:
            # 根据不同操作系统选择ping命令
            if platform.system().lower() == "windows":
                cmd = ['ping', '-n', '1', '-l', str(self.length), self.dstip]
                if self.srcip:
                    cmd.insert(1, '-S')
                    cmd.insert(2, self.srcip)
            else:
                cmd = ['ping', '-c', '1', '-s', str(self.length), self.dstip]
                if self.srcip:
                    cmd.insert(1, '-I')
                    cmd.insert(2, self.srcip)

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                print(f"{self.dstip} 可达!")
                return True
            else:
                print(f"{self.dstip} 不可达!")
                return False

        except subprocess.TimeoutExpired:
            print(f"{self.dstip} 超时!")
            return False
        except Exception as e:
            print(f"ping执行错误: {e}")
            return False

    def ping(self, count=5):
        """模拟正常ping程序ping指定数量的包"""
        results = []

        for i in range(count):
            try:
                # 根据不同操作系统选择ping命令
                if platform.system().lower() == "windows":
                    cmd = ['ping', '-n', '1', '-l', str(self.length), self.dstip]
                    if self.srcip:
                        cmd.insert(1, '-S')
                        cmd.insert(2, self.srcip)
                else:
                    cmd = ['ping', '-c', '1', '-s', str(self.length), self.dstip]
                    if self.srcip:
                        cmd.insert(1, '-I')
                        cmd.insert(2, self.srcip)

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

                if result.returncode == 0:
                    results.append('!')  # 通
                else:
                    results.append('.')  # 不通

            except subprocess.TimeoutExpired:
                results.append('.')  # 超时也算不通
            except Exception:
                results.append('.')  # 其他错误也算不通

        # 打印结果
        print(''.join(results))
        return results


class NewPing(QYTPING):
    def __str__(self):
        if self.srcip:
            return f"<NewPing => srcip: {self.srcip}, dstip: {self.dstip}, size: {self.length}>"
        else:
            return f"<NewPing => dstip: {self.dstip}, size: {self.length}>"

    def ping(self, count=5):
        """重写ping方法，使用不同的符号"""
        results = []

        for i in range(count):
            try:
                # 根据不同操作系统选择ping命令
                if platform.system().lower() == "windows":
                    cmd = ['ping', '-n', '1', '-l', str(self.length), self.dstip]
                    if self.srcip:
                        cmd.insert(1, '-S')
                        cmd.insert(2, self.srcip)
                else:
                    cmd = ['ping', '-c', '1', '-s', str(self.length), self.dstip]
                    if self.srcip:
                        cmd.insert(1, '-I')
                        cmd.insert(2, self.srcip)

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)

                if result.returncode == 0:
                    results.append('+')  # 通，使用+
                else:
                    results.append('?')  # 不通，使用?

            except subprocess.TimeoutExpired:
                results.append('?')  # 超时也算不通
            except Exception:
                results.append('?')  # 其他错误也算不通

        # 打印结果
        print(''.join(results))
        return results


def print_new(word, s='-'):
    """打印分隔行"""
    total_len = 70
    left_len = int((total_len - len(word)) / 2)
    right_len = total_len - len(word) - left_len
    print(f"{s * left_len}{word}{s * right_len}")


if __name__ == '__main__':
    # 注意：实际使用时请将IP地址改为可ping通的目标
    ping = QYTPING('8.8.8.8')  # 使用类QYTPING,产生实例

    print_new('print class')
    print(ping)  # 打印类

    print_new('ping one for sure reachable')
    ping.one()  # Ping一个包判断可达性

    print_new('ping five')
    ping.ping()  # 模拟正常ping程序ping五个包，'!'表示通，'.'表示不通

    print_new('set payload length')
    ping.length = 200  # 设置负载长度
    print(ping)  # 打印类
    ping.ping()  # 使用修改长度的包进行ping测试

    print_new('set ping src ip address')
    ping.srcip = '192.168.1.1'  # 修改源IP地址
    print(ping)  # 打印类
    ping.ping()  # 使用修改长度又修改源的包进行ping测试

    print_new('new class NewPing')
    newping = NewPing('8.8.8.8')  # 使用新的类NewPing(通过继承QYTPING类产生)产生实例
    newping.length = 300
    print(newping)  # 打印类
    newping.ping()  # NewPing类自定义过ping()这个方法， '+'表示通，'?'表示不通