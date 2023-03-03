# Vinícius Kenzo Fukace - RA115672
# Guilherme Panobianco Ferrari - RA112679

import socket
import select

HOST = 'localhost'
TCP_PORT = 8080
UDP_PORT = 8081

SERVER_POOL = [('localhost', 60001), ('localhost', 60002), ('localhost', 60003)]
CURRENT_SERVER = 0

# Retorna True se o servidor estiver ativo, False caso contrário
def servertest(host, port, protocol):
    if protocol == socket.SOCK_STREAM:
        args = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)
        for family, socktype, proto, canonname, sockaddr in args:
            s = socket.socket(family, socktype, proto)
            try:
                s.connect(sockaddr)
            except:
                print(f'Erro na conexão ao servidor {host}:{port}')
                return False
            else:
                s.close()
                return True
    elif protocol == socket.SOCK_DGRAM:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        try:
            s.sendto(b'', (host, port))
            s.recvfrom(1024)
        except:
            print(f'Erro na conexão ao servidor {host}:{port}')
            return False
        else:
            s.close()
            return True
    else:
        return False


# Retorna o índice do próximo servidor disponível
# Caso não haja servidor disponível, retorna -1
def getNextServer(protocol):
    global SERVER_POOL, CURRENT_SERVER
    nextServer = (CURRENT_SERVER + 1) % len(SERVER_POOL)

    # passa sequencialmente pelos próximos servidores até achar um que funcione
    while nextServer != CURRENT_SERVER:
        nextServerAddr, nextServerPort = SERVER_POOL[nextServer]
        # se o servidor estiver disponível
        if(servertest(nextServerAddr, nextServerPort, protocol)):
            return nextServer
        else:
            nextServer = (nextServer + 1) % len(SERVER_POOL)

    # Neste caso, já passou por todos os servidores e voltou para o primeiro
    # se o primeiro não estiver disponível, nenhum está disponível
    nextServer = (nextServer + 1) % len(SERVER_POOL)
    nextServerAddr, nextServerPort = SERVER_POOL[nextServer]
    if (servertest(nextServerAddr, nextServerPort, socket.SOCK_DGRAM)):
        return CURRENT_SERVER
    else:
        return -1


def main():
    global HOST, TCP_PORT, UDP_PORT, SERVER_POOL, CURRENT_SERVER

    # Cria socket TCP
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcp_sock.bind((HOST, TCP_PORT))
    tcp_sock.listen(5)

    # Cria socket UDP
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_sock.bind((HOST, UDP_PORT))

    # Seleciona os dois sockets para receber respostas de ambos
    input_sockets = [tcp_sock, udp_sock]

    print(f"Load Balancer listening on {HOST}:{TCP_PORT} (TCP) and {HOST}:{UDP_PORT} (UDP)")

    while True:
        readable, _, _ = select.select(input_sockets, [], [])

        for sock in readable:
            # Socket TCP
            if sock == tcp_sock:
                client_sock, client_addr = sock.accept()
                print(f"Received TCP connection from {client_addr}")

                # Choose a server to forward the connection to
                nextServer = getNextServer(socket.SOCK_STREAM)
                if nextServer == -1:
                    print('Sem servidores TCP disponiveis\n')
                    client_sock.sendall(b'Sem servidores TCP disponiveis')
                    client_sock.close()
                    continue
                CURRENT_SERVER = nextServer
                serverAddr, serverPort = SERVER_POOL[CURRENT_SERVER]

                # Forward the connection
                print(f"Forwarding TCP connection to {serverAddr}:{serverPort}\n")
                server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_sock.connect((serverAddr, serverPort))
                server_sock.sendall(client_sock.recv(1024))
                client_sock.sendall(server_sock.recv(1024))

                # Close the connections
                client_sock.close()
                server_sock.close()

            # Socket UDP
            elif sock == udp_sock:
                data, addr = udp_sock.recvfrom(1024)
                print(f"Received UDP message from {addr}")

                # Choose a server to forward the message to
                nextServer = getNextServer(socket.SOCK_DGRAM)
                if nextServer == -1:
                    print('Sem servidores UDP disponiveis\n')
                    udp_sock.sendto(b'Sem servidores UDP disponiveis', addr)
                    continue
                CURRENT_SERVER = nextServer
                serverAddr, serverPort = SERVER_POOL[CURRENT_SERVER]

                # Forward the connection
                print(f"Forwarding UDP connection to {serverAddr}:{serverPort}\n")
                server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                server_sock.sendto(data, (serverAddr, serverPort))
                udp_sock.sendto(server_sock.recv(1024), addr)

                # Close the connection
                server_sock.close()


if __name__ == '__main__':
    main()
