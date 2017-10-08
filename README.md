# badrat
i'd like to call this a (bad) remote access tool instead of trojan


## Tutorial

### What's all this noise about?
We're going to be writing a simple client and server. Simply put the server will send the client a message
and based on this message the client will run some sort of shell command. You could compare this to a (hugely) dumbed down RAT or
some other remote access utility.


#### The client

##### Sockets
We're going to need to use the sockets module so that we can establish a TCP connection with our server client 
which we will write later in this tutorial.

##### Subprocess
We also need the subprocess module so we can execute shell commands through our Python program.

```python
import socket
import subprocess
```
First we're going to create a socket through calling socket.socket

Next we're going to need to specify our host and port we want to connect on, you're going to want this to correspond to the
servers details which we will set later on. 

**Note: You can get the IPv4 of a machine through ipconfig on Windows or ifconfig on Linux using the CLI, 
this is what goes in the host field. I won't go in depth here though as it is a Google search away should you need it.**

Finally the code takes our two variables host and port and attempts a connection
```python
s = socket.socket()
host = "172.26.240.105"
port = 1424

s.connect((host, port))
```

Now the following may look like a big chunk of code but it is relatively simple.

Our program endlessly loops waiting for messages from the server or for you to enter 'exit' to end our client program

You also notice 3 if statements, these are how we define the behavior for how our program should respond should we receive
a certain message from the server we recognise.

You also may have noticed we make use of subprocess.call a few times, this is what allows us to execute shell commands,
note how the amount of parameters may vary based on the command you try to execute, this could be OS, or desktop environment
dependent if you're a Linux user.
```python
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
```

#### The server

We're going to start off by including the sockets module again, the server needs to be able to accept TCP connections.
```python
import socket
```

The next bit looks familiar again, pop the servers IPv4 in and select a port that matches the clients one and we can move
swiftly on
```python
s = socket.socket()
host = "172.26.240.105"
port = 1424
```

Oh look this is different! This time we're binding to a port instead of connecting because we're the server now
and waiting for connections

We then listen for a maximum of 5 queued connection through the s.listen method and accept any incoming connection, in this case
we are accepting one and haven't put it inside our loop which is to come, this is not very ideal as you will need to restart the 
server after each connection
```python
s.bind((host, port))
s.listen(5)
c, addr = s.accept()
```
Loopy loop for input and send it to the client encoded as utf-8 to prevent some errors you may get sending it unencoded.
If the input is exit then we send the client the exit command which tells them to quit and then proceeds to close the socket

```python
while True:
   cmd = input("Enter your command\n")

   if cmd == "exit":
        c.send(cmd.encode("utf-8"))
        c.close()
        break

c.send(cmd.encode())
```

## Final words
You can improve this! (A lot!) You should now simple ideas down of how you might talk to clients through a sockets,
going forward I would recommend you try and write some of your own commands using the existing ones as a guideline and then
re-writing the entire thing to be concurrent and not have our nasty restart requirement


