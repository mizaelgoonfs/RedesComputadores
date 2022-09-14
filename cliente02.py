from socket import *

Rementente_Cliente02_Sock = socket(AF_INET, SOCK_DGRAM)
Receptor_Cliente02_Sock = socket(AF_INET, SOCK_DGRAM)  # Criacao do socket UDP.
Receptor_Cliente02_Sock.bind(('', 4000))  # Definicao de numero de porta.
print("O cliente 02 ativado!")

destino = ('127.0.0.1', 5000)


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

        transbordo = (primeiroBit & segundoBit) | (segundoBit & transbordo) | (
                primeiroBit & transbordo)

    if (transbordo == 1):
        somaBits = adicionaBit(somaBits, '1')

    return somaBits


ack = None
while True:
    mensagem_recebida_c, ip_servidor = Receptor_Cliente02_Sock.recvfrom(1024)
    mensagem_recebida = mensagem_recebida_c.decode("utf-8")
    seq = mensagem_recebida[0:1]
    checksum = mensagem_recebida[1:17]
    mensagem = mensagem_recebida[17:]
    
    if (not seq.isnumeric()):
        print("seq = ", seq)
        print("numero de sequencia corrompido")
    else:
        print("seq = ", int(seq))

    print("mensagem_recebida = ", mensagem_recebida)

    listaBits = list(format(c, 'b') for c in bytearray(mensagem, "utf-8"))  # Transformando a mensagem em bits.
    for i in range(len(listaBits)):  # Percorrendo lista de bits.
        if i == 0:
            somaBits = adicionaBit(listaBits[i], '0')
        else:
            somaBits = adicionaBit(somaBits, listaBits[i])

    somaBits = (16 - len(somaBits)) * '0' + somaBits  # Caso a soma, seja, menor que 16bits e completado com zeros.
    # Soma checksum com a mensagem que chegou, se a soma for sequencia de 16bits-1, sem erro detectado.
    print("somaBits = ", somaBits)
    print("checksum = ", checksum)
    print("ack = ", ack)

    if (not seq.isnumeric()):  # verifica se o numero de sequencia é composto apenas de numeros, caso retorne falso,
        # retorna pro inicio while, estourando o temporizador
        continue

    if str(ack) == seq and ack != None:  # verifica pacote repetido
        print("pacote repetido detectado")
        Rementente_Cliente02_Sock.sendto(str(ack).encode(), destino)
        continue

    try:  # tratamento de excessão para deixar passar caractere especial do checksum
        somaRC = adicionaBit(somaBits, checksum)
        if somaRC == "1111111111111111":  # verificar mensagem corrompida
            if ack != int(seq) or ack is None:
                print("Cliente02 recebeu =", mensagem, ", do cliente", ip_servidor)
                # Devolve um ack correspondente ao numero de sequencia do pacote recebido.
                ack = seq
                print(f"Enviando Ack {ack}\n")
                # endereco eh o endereco do socket que enviou os dados.
                Rementente_Cliente02_Sock.sendto(str(ack).encode(), destino)
        else:
            raise
    except:
        print("Checksum corrompido")
        ack = 1 - int(seq)
        print(f"Enviando Ack {ack}\n")
        Rementente_Cliente02_Sock.sendto(str(ack).encode(), destino)
        continue

    if (mensagem == "sair"):
        print("Encerrando comunicacao!")
        break

# Fechamento do socket.
Rementente_Cliente02_Sock.close()
Receptor_Cliente02_Sock.close()
