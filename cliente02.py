from socket import *

Rementente_Cliente02_Sock = socket(AF_INET, SOCK_DGRAM)
Receptor_Cliente02_Sock = socket(AF_INET, SOCK_DGRAM) # Criacao do socket UDP.
Receptor_Cliente02_Sock.bind(('', 4000)) # Definicao de numero de porta.
print("O cliente 02 ativado!")

destino = ('127.0.0.1', 5000)

def resultadoC(checksum): # Complemento do checksum.
	resultado = ''
	for i in checksum:
		if(i=='0'):
			resultado += '1'
		else:
			resultado += '0'
	return resultado

def somaResChe(p, s): # Fazendo soma entre resultado e checksum.
    somaRC = ''
    transbordo = 0

    for i in range(len(p) - 1, -1, -1):
        primeiroBit = int(p[i])
        segundoBit = int(s[i])

        sum = (primeiroBit ^ segundoBit ^ transbordo) + 48
        somaRC = chr(sum) + somaRC

        transbordo = (primeiroBit & segundoBit) | (segundoBit & transbordo) | (primeiroBit & transbordo)

    if(transbordo == 1):
        somaRC = somaResChe(somaRC, '1')

    return somaRC

ack = None
while(True):
    mensagem_recebida_c, ip_servidor = Receptor_Cliente02_Sock.recvfrom(1024)
    mensagem_recebida = mensagem_recebida_c.decode("utf-8")
    seq = mensagem_recebida[0:1]
    checksum = mensagem_recebida[1:17]
    mensagem = mensagem_recebida[17:]

    # Soma checksum com o resultado, se a soma for sequencia de 16bits-1, sem erro detectado.
    resultado = resultadoC(checksum)
    somaRC = somaResChe(resultado, checksum)
    if(somaRC == "1111111111111111"):
        print("Mensagem recebida sem erro detectado!")
    else:
        print("Erro detectado!")

    if(mensagem == "sair"):
        print("Encerrando comunicacao!")
        break

    if len(mensagem) is not None:
        print("Cliente02 recebeu =",mensagem,", do cliente", ip_servidor) 
        # Devolve um ack correspondente ao numero de sequencia do pacote recebido.
        if seq == "0":
            ack = "0"
        elif seq == "1":
            ack = "1"
        print(f"Enviando Ack {ack}\n")
        # endereco eh o endereco do socket que enviou os dados.
        Rementente_Cliente02_Sock.sendto(ack.encode(), destino)
          
# Fechamento do socket.
Rementente_Cliente02_Sock.close()
Receptor_Cliente02_Sock.close()