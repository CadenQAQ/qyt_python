import os
import re
import time
while True:
    port_result = os.popen("netstat -tulnp").read()  # 执行并返回命令的结果
    if not re.search(r'^tcp\s+\d+\s+\d+\s+0\.0\.0\.0:80\s', port_result, re.M):
        print("等待一秒重新开始监控！")
        time.sleep(1)

    else:
        print("HTTP(TCP/80)服务器已经被打开")
        break;