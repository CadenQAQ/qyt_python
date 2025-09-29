import os
route_n_result = os.popen("route -n").read() # 执行并返回命令的结果
ipv4_gw = None
for line in route_n_result.splitlines():
    parts = line.split()
    # 跳过表头，找到默认路由行
    if len(parts) >= 2 and parts[0] == "0.0.0.0":
        ipv4_gw = parts[1]
        break
print("网关为："+ ipv4_gw)

l1=[4,5,7,1,3,9,0]
#l2是l1的排序
l2=sorted(l1)

for i in range (len(l1)):
    print(l1[i],l2[i])