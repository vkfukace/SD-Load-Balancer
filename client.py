import sys
import socket

HOST = 'localhost'
PORT_TCP = 8080
PORT_UDP = 8081

if len(sys.argv) != 2:
    print("Uso: python3 client.py <protocolo>")
    print("Onde <protocol> eh 1 para TCP ou 2 para UDP.")
    exit()

protocol = int(sys.argv[1])

if protocol == 1:
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.connect((HOST, PORT_TCP))

    sock.sendall(b'Enviando uma mensagem TCP')

    response = sock.recv(1024)
    print(f'Response from load balancer: {response.decode()}')

    # Close the socket
    sock.close()
elif protocol == 2:
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(b'Enviando uma mensagem UDP', (HOST, PORT_UDP))

    response, _ = sock.recvfrom(1024)
    print(f'Response from load balancer: {response.decode()}')

    # Close the socket
    sock.close()
else:
    print("Protocolo invalido. Precisa ser 1 para TCP ou 2 para UDP.")
    exit()