from socket import *
import time
import random

def corrupt(pkt):
    index = random.randint(0, len(pkt) - 1)
    var = str(chr(random.randint(0, 95)))
    if(var == '0' or var == '1'):
        var = '#'
    pkt = pkt[:index] + var.encode() + pkt[index + 1:]
    return pkt


def manipulador(opt, mensagem, servidor_UDP, cliente_destino, ip_cliente):
    if opt == 1:
        print("Pacote perdido!")
        time.sleep(3)
        return
    elif opt == 2:
        # opção para corromper o pacote e causar erro de checksum ou ack corrompido
        mensagem = corrupt(mensagem)
        servidor_UDP.sendto(mensagem, cliente_destino)
        return

    print("Servidor recebeu =", mensagem.decode("utf-8"), ", do cliente", ip_cliente)
    print("Servidor enviou =", mensagem.decode("utf-8"), ", para o cliente", cliente_destino)
    servidor_UDP.sendto(mensagem, cliente_destino)


servidor_UDP = socket(AF_INET, SOCK_DGRAM)
print("O servidor esta disponivel!")

receptor_cliente01 = ('127.0.0.1', 3000)
destino_cliente01 = ('127.0.0.1', 2000)
receptor_cliente02 = ('127.0.0.1', 5000)
destino_cliente02 = ('127.0.0.1', 4000)

Receptor_Cliente01_Sock = socket(AF_INET, SOCK_DGRAM)
Receptor_Cliente01_Sock.bind(receptor_cliente01)
Receptor_Cliente01_Sock.setblocking(False)
Receptor_Cliente02_Sock = socket(AF_INET, SOCK_DGRAM)
Receptor_Cliente02_Sock.bind(receptor_cliente02)
Receptor_Cliente02_Sock.setblocking(False)

while True:
    try:
        mensagem_recebida_c, ip_cliente = Receptor_Cliente01_Sock.recvfrom(1024)

        rand = random.randint(1, 20)
        if 1 <= rand <= 5:
            opt = 0
        elif 6 <= rand <= 15:
            opt = 1
        elif 16 <= rand <= 20:
            opt = 2

        print("\nOPÇÃO CLIENTE 1 -> 2: ", opt)
        manipulador(opt, mensagem_recebida_c, servidor_UDP, destino_cliente02, ip_cliente)

    except error:
        pass

    try:
        mensagem_recebida_c, ip_cliente = Receptor_Cliente02_Sock.recvfrom(1024)

        rand = random.randint(1, 20)
        if 1 <= rand <= 15:
            opt = 0
        elif 16 <= rand <= 20:
            opt = 2

        print("\nOPÇÃO CLIENTE 2 -> 1: ", opt)
        manipulador(opt, mensagem_recebida_c, servidor_UDP, destino_cliente01, ip_cliente)
    except error:
        pass

servidor_UDP.close()  # Fechamento do socket.
