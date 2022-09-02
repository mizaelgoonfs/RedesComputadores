from socket import *
import time

def descarta_ack(msg, n):
    if n < 6 and len(msg) == 1:
        return True
    else:
        return True

def manipulador(opt, mensagem, servidor_UDP, cliente_destino, ip_cliente):
    if opt == 1:
        print("Pacote perdido!")
        time.sleep(3)
        return
    elif opt == 2:
        #opção para corromper o pacote e causar erro de checksum
        corromper = "Função para corromper"
    
    print ("Servidor recebeu =",mensagem.decode("utf-8"),", do cliente", ip_cliente)
    print("Servidor enviou =",mensagem.decode("utf-8"),", para o cliente", cliente_destino)
    servidor_UDP.sendto(mensagem, cliente_destino)


servidor_UDP = socket(AF_INET, SOCK_DGRAM)
print("O servidor esta disponivel!")

receptor_cliente01 = ('127.0.0.1', 3000)
destino_cliente01 = ('127.0.0.1', 2000)
receptor_cliente02 = ('127.0.0.1', 5000)
destino_cliente02 = ('127.0.0.1', 4000)

Receptor_Cliente01_Sock = socket(AF_INET, SOCK_DGRAM)
Receptor_Cliente01_Sock.bind(receptor_cliente01)
Receptor_Cliente01_Sock.setblocking(0)
Receptor_Cliente02_Sock = socket(AF_INET, SOCK_DGRAM)
Receptor_Cliente02_Sock.bind(receptor_cliente02)
Receptor_Cliente02_Sock.setblocking(0)

#numero_de_acks = 0
alterador_opcao_cliente01 = True
while(True):
    try:
        mensagem_recebida_c, ip_cliente = Receptor_Cliente01_Sock.recvfrom(1024)
        mensagem_recebida = mensagem_recebida_c.decode("utf-8")
        mensagem = mensagem_recebida[17:]

        if(alterador_opcao_cliente01):
            opt = 0
            alterador_opcao_cliente01 = False
        else:
            opt = 1
            alterador_opcao_cliente01 = True
        manipulador(opt, mensagem_recebida_c, servidor_UDP, destino_cliente02, ip_cliente)
    except error:
        pass

    try:
        mensagem_recebida_c, ip_cliente = Receptor_Cliente02_Sock.recvfrom(1024)
        mensagem_recebida = mensagem_recebida_c.decode("utf-8")
        mensagem = mensagem_recebida[17:]

        opt = 0
        manipulador(opt, mensagem_recebida_c, servidor_UDP, destino_cliente01, ip_cliente)
    except error:
        pass

servidor_UDP.close() # Fechamento do socket.