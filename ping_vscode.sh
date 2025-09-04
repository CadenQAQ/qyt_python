#!/bin/bash
while true; do
    ping -c 5 update.code.visualstudio.com >> /var/log/ping_vscode.log

    # 保留最后 1000 行，避免日志无限增长
    tail -n 1000 /var/log/ping_vscode.log > /var/log/ping_vscode.log.tmp
    mv /var/log/ping_vscode.log.tmp /var/log/ping_vscode.log

    sleep 30
done

#nohup ./ping_vscode.sh >/dev/null 2>&1 &
#tail -f /var/log/ping_vscode.log
