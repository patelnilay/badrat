import socket

s = socket.socket()
host = "172.26.240.105"
port = 1424

s.bind((host, port))
s.listen(5)
c, addr = s.accept()

while True:
   cmd = input("Enter your command\n")

   if cmd == "exit":
        c.send(cmd.encode())
        c.close()
        break

   c.send(cmd.encode())
