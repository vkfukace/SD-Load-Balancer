import sys
import socket

HOST = "localhost"
PORT = 60002  # Port to listen on (non-privileged ports are > 1023)

if len(sys.argv) != 2:
    print("Uso: python3 server2.py <protocolo>")
    print("Onde <protocol> eh 1 para TCP ou 2 para UDP.")
    exit()

protocol = int(sys.argv[1])

if protocol == 1:
    # TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen()
    print(f'TCP Server 2 listening on {HOST}:{PORT}...')
elif protocol == 2:
    # UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    print(f'UDP Server 2 listening on {HOST}:{PORT}...')
else:
    print("Protocolo invalido. Precisa ser 1 para TCP ou 2 para UDP.")
    exit()

while True:
    if protocol == 1:
        conn, addr = sock.accept()
        print(f"Connected by {addr}")

        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Message received: {data}")
            conn.sendall(data)

        conn.close()

    if protocol == 2:
        data, addr = sock.recvfrom(1024)
        if (len(data) > 0):
            print(f"Message received from {addr}: {data}")

        sock.sendto(data, addr)
