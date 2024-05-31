import socket
import time
import sys

version = "v2"

HOST = "127.0.0.1"
PORT = 65432

LOGS = []

def log(message, severity, server = None):
    _endOfLog = len(LOGS)
    LOGS.append([None, severity, message])
    _currTime = time.localtime()
    LOGS[_endOfLog][0] = str(_currTime[3]) + ":" + str(_currTime[4]) + ":" + str(_currTime[5])

    print(LOGS[_endOfLog][0], " : ", LOGS[_endOfLog][1], " : ", LOGS[_endOfLog][2])

    if server != None:
        sock.sendall(f"SENDLOG---{str(LOGS[_endOfLog])}".encode())
        _ = sock.recv(1024)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

log("Started!", "info")

try:
    log("Connecting to log server...", "info")
    sock.connect((HOST, PORT))
except Exception as e:
    log(e, "FATAL")
    sys.exit(1)

# Conn request
log("Connected to {}:{}!".format(HOST,PORT), "info")

sock.sendall(b"conn request")
data = sock.recv(1024)

if data == b"accepted":
    log("Successful!", "info")
else:
    log("not accepted", "FATAL")
    sys.exit(1)

# handshake
log("Handshake with server".format(HOST,PORT), "info")

sock.sendall(b"version handshake")
data = eval(sock.recv(1024).decode())

if version in data:
    log("Our version is supported with the server", "info")

    sock.sendall(b"handshake accepted")
    _ = sock.recv(1024)
else:
    log("Version mis-match", "FATAL")
    sys.exit(1)

# sync logs
log("Syncing logs with server".format(HOST,PORT), "info")

sock.sendall(f"LOGSYNC---{str(LOGS)}".encode())
data = sock.recv(1024)

log("hello server test", "verbose", sock)
log("hello server test", "verbose", sock)

log("Sending file", "info", sock)

_filething = "log file or something\nqwertyuiop[]\\asdfghjkl;'zxcvbnm,./1234567890-=!@#$%^&*()_+`~QWERTYUIOP{}|ASDFGHJKL:\"ZXCVBNM<>?\nqwertyuiop[]\\asdfghjkl;'zxcvbnm,./1234567890-=!@#$%^&*()_+`~QWERTYUIOP{}|ASDFGHJKL:\"ZXCVBNM<>?\nqwertyuiop[]\\asdfghjkl;'zxcvbnm,./1234567890-=!@#$%^&*()_+`~QWERTYUIOP{}|ASDFGHJKL:\"ZXCVBNM<>?"

sock.sendall(f"send file---cool.txt---{len(_filething)}".encode())
data = sock.recv(1024).decode()

if data == "ok":
    sock.sendall(_filething.encode())
    data = sock.recv(1024).decode()
    if data == "ok":
        log("Server got our file", "info", sock)
    else:
        log("Server did not get our file successfully", "warn", sock)
else:
    log("Server didn't accept our file.....", "warn", sock)



sock.close()