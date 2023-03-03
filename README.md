# SD-Load-Balancer

CC UEM 2023 - Sistemas Digitais

Vinícius Kenzo Fukace - RA115672
Guilherme Panobianco Ferrari - RA112679

Desenvolva um Balanceador de Carga que receba conexões e seja capaz de enviar o tráfego para três diferentes servidores (S1, S2 e S3). Dois algoritmos devem ser implementados:

1. Round Robin padrão
2. Encaminhamento baseado no tipo de conexão (TCP ou UDP). Nesse algoritmo, S1 deve receber as conexões TCP, S2 e S3 devem receber as conexões UDP. A distribuição entre S2 e S3 deve usar o algoritmo Round Robin.

Para a execução do Balanceador de carga, deve ser passado um parâmetro numérico para a escolha do algoritmo.

Pode ser feito em duplas.

## Implementação

O cliente escolhe qual tipo de conexão utilizar com base no argumento de execução.

O Load Balancer se conecta a 3 servidores, que podem utilizar TCP ou UDP.
É possível ter 3 servidores TCP e 0 UDP, ou 1 TCP e 2 UDP, por exemplo.

O Load Balancer sempre vai tentar fazer o Round Robin com base no tipo de conexão utilizada.
Se não tiver nenhum servidor disponível, retorna uma mensagem para o cliente.

## Execução

-   python3 server1.py 1 : Inicia servidor 1 como TCP
-   python3 server2.py 2 : Inicia servidor 2 como UDP
-   python3 server3.py 2 : Inicia servidor 3 como UDP
-   python3 loadBalancer.py : Inicia o Load Balancer
-   python3 client.py 1 : Envia uma mensagem TCP para o Load Balancer
-   python3 client.py 2 : Envia uma mensagem UDP para o Load Balancer
