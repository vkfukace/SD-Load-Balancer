import socket

HOST = 'localhost'
PORT = 8080

SERVER_POOL = [('localhost', 60001), ('localhost', 60002), ('localhost', 60003)]
CURRENT_SERVER = 0

# Create a socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a port
sock.bind((HOST, PORT))

# Listen for incoming connections
sock.listen(5)

print(f"Load Balancer listening on {HOST}:{PORT}...")

while True:
    # Accept an incoming connection
    client_sock, client_addr = sock.accept()
    print(f"Received connection from {client_addr}")
    
    # Choose a server to forward the connection to
    serverAddr, serverPort = SERVER_POOL[CURRENT_SERVER]
    CURRENT_SERVER = (CURRENT_SERVER + 1) % len(SERVER_POOL)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.connect((serverAddr, serverPort))

    # Forward the connection
    print(f"Forwarding connection to {serverAddr}:{serverPort}\n")
    server_sock.sendall(client_sock.recv(1024))
    client_sock.sendall(server_sock.recv(1024))

    # Close the connections
    client_sock.close()
    server_sock.close()