from socket import socket, AF_INET, SOCK_DGRAM, timeout

Rementente_Cliente01_Sock = socket(AF_INET, SOCK_DGRAM)
Receptor_Cliente01_Sock = socket(AF_INET, SOCK_DGRAM)  # Criacao do socket UDP.
Receptor_Cliente01_Sock.bind(('', 2000))  # Definicao de numero de porta.
Receptor_Cliente01_Sock.settimeout(3)  # Definindo limite do temporizador
print("O cliente 01 ativado!")

destino = ('127.0.0.1', 3000)  # IP e porta do servidor.


def igualCompr(p, s):  # Para que haja igualdade de comprimento entre as somas.
    tamanho01 = len(p)
    tamanho02 = len(s)
    if (tamanho01 < tamanho02):
        p = (tamanho02 - tamanho01) * '0' + p
        tamanho01 = len(p)
    else:
        if (tamanho02 < tamanho01):
            s = (tamanho01 - tamanho02) * '0' + s
            tamanho02 = len(s)
    return tamanho01, p, s


def adicionaBit(p, s):  # Fazendo soma entre os bits.
    somaBits = ''
    total, p, s = igualCompr(p, s)
    transbordo = 0

    for i in range(total - 1, -1, -1):
        primeiroBit = int(p[i])
        segundoBit = int(s[i])

        sum = (primeiroBit ^ segundoBit ^ transbordo) + 48
        somaBits = chr(sum) + somaBits

        transbordo = (primeiroBit & segundoBit) | (segundoBit & transbordo) | (primeiroBit & transbordo)

    if (transbordo == 1):
        somaBits = adicionaBit(somaBits, '1')

    return somaBits


def complemento(somaBits):  # Complemento do checksum.
    checksum = ''
    for i in somaBits:
        if i == '0':
            checksum += '1'
        else:
            checksum += '0'
    return checksum

def enviar_mensagem(Mensagem, DESTINO):
    Rementente_Cliente01_Sock.sendto(Mensagem, DESTINO)

seq = 0

while True:
    mensagem = input("Digite a mensagem: ")  # Mensagem recebera dados do teclado.
    listaBits = list(format(c, 'b') for c in bytearray(mensagem, "utf-8"))  # Transformando a mensagem em bits.

    for i in range(len(listaBits)):  # Percorrendo lista de bits.
        if i == 0:
            somaBits = adicionaBit(listaBits[i], '0')
        else:
            somaBits = adicionaBit(somaBits, listaBits[i])

    somaBits = (16 - len(somaBits)) * '0' + somaBits  # Caso a soma, seja, menor que 16bits e completado com zeros.
    checksum = complemento(somaBits)  # Complemento do checksum.

    enviar_mensagem(str(seq).encode() + str(checksum).encode() + mensagem.encode(), destino)  # Envio de bytes codificados para servidor.

    if mensagem == "sair":
        print("Comunicacao encerrada!")
        enviar_mensagem(str(seq).encode() + str(checksum).encode() + mensagem.encode(), destino)
        break

    ack_recebido = False
    # Recebe um Ack, se ele for o ack esperado libera para o envio da prox msg, se nao é ignorado
    while not ack_recebido:

        try:
            mensagem_recebida, ip_servidor = Receptor_Cliente01_Sock.recvfrom(1024)
            mensagem_ack = mensagem_recebida.decode("utf-8")

        except timeout:
            print("Timeout!\nREENVIANDO MENSAGEM...")
            enviar_mensagem(str(seq).encode() + str(checksum).encode() + mensagem.encode(), destino)  # Envio de bytes codificados para servidor.
        else:
            if mensagem_ack == str(seq):
                print("Cliente02 recebeu =", mensagem, ", do cliente", ip_servidor)
                print("Ack", mensagem_ack, "recebido, pronto para enviar a proxima mensagem\n")
                ack_recebido = True
            else:
                print("Erro de Ack ou Ack corrompido detectado!")
                print("Reenviando arquivo...")
                enviar_mensagem(str(seq).encode() + str(checksum).encode() + mensagem.encode(), destino)
    seq = 1 - seq

# Fechamento do socket.
Rementente_Cliente01_Sock.close()
Receptor_Cliente01_Sock.close()
