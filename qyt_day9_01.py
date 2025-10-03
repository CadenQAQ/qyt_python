import paramiko
import os

def qytang_ssh(ip,username,password,port=22,cmd='ls'):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password, timeout=5, compress=True)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    x = stdout.read().decode()
    ssh.close()
    return x

def ssh_get_route(ip,username,password,cmd='ls'):
    route_n_result = qytang_ssh(ip,username,password,port=22,cmd="/sbin/route -n")
    ipv4_gw = None
    for line in route_n_result.splitlines():
        parts = line.split()

        if len(parts) >= 2 and parts[0] == "0.0.0.0":
            ipv4_gw = parts[1]
            break
    print("网关为:\n")
    return ipv4_gw

if __name__ == "__main__":
    #print(qytang_ssh("1.1.1.1","admin","password@123"))
    #print(qytang_ssh(ip="1.1.1.1", username="admin", password="password@123", cmd="pwd"))
    print(ssh_get_route("1.1.1.1", "admin", "password@123"))