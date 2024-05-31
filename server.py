import socket

HOST = "0.0.0.0"
PORT = 65432

versions = ["v1", "v1.1", "v2"]

ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ss.bind((HOST, PORT))
ss.listen()

Running = True

def recvall(sock, n): # https://stackoverflow.com/a/17668009
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


while Running:
    conn, addr = ss.accept()
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            # v1
            if data == b"conn request":
                conn.sendall(b"accepted")
                print(f"{addr[0]}:{addr[1]} - accepted request")
            elif data == b"handshake request":
                conn.sendall(b"v1")
                print(f"{addr[0]}:{addr[1]} - sent handshake data")
            elif data == b"handshake accepted":
                conn.sendall(b"ok")
                print(f"{addr[0]}:{addr[1]} - sent handshake accepted")
            elif data.decode().split("---")[0] == "LOGSYNC":
                print(f"{addr[0]}:{addr[1]} - sent logs")
                _LOGS = eval(data.decode().split("---")[1])
                for i in range(len(_LOGS)):
                    print(f"{addr[0]}:{addr[1]} - {_LOGS[i][0]} : {_LOGS[i][1]} : {_LOGS[i][2]}")
                conn.sendall(b"ok")
            elif data.decode().split("---")[0] == "SENDLOG":
                _LOGS = eval(data.decode().split("---")[1])
                print(f"{addr[0]}:{addr[1]} - {_LOGS[0]} : {_LOGS[1]} : {_LOGS[2]}")
                conn.sendall(b"ok")
            
            # v1.1
            elif data == b"version handshake":
                conn.sendall(f"{versions}".encode())
                print(f"{addr[0]}:{addr[1]} - sent version handshake data")

            # v2
            elif data.decode().split("---")[0] == "send file":
                data = data.decode().split("---")
                conn.sendall(b"ok")
                print(f"{addr[0]}:{addr[1]} - accepted send file - name {data[1]} size {data[2]}b")
                try:
                    with open(data[1], "w") as f:
                        f.write(recvall(conn, int(data[2])).decode())
                        conn.sendall(b"ok")
                except Exception as e:
                    conn.sendall(b"not ok")
                    print(f"! {e} line {e.__traceback__.tb_lineno}")

    print(f"{addr[0]}:{addr[1]} - disconnected")