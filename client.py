
import socket
import subprocess

s = socket.socket()
host = "172.26.240.105"
port = 1424

s.connect((host, port))

while True:
    cmd = s.recv(1024).decode("utf-8")

    if cmd == "logout":
        subprocess.call(["xfce4-session-logout", "--logout"])

    if cmd == "exit":
        s.close
        break

    cmd = cmd.split(",")

    if cmd[0] == "message" and len(cmd) == 2:
        subprocess.call(["notify-send", cmd[1]])
