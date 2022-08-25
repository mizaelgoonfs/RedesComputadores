import socket
#importa a bib socket

MEU_IP = ''                                
# Endereco IP do Servidor, '' = significa que ouvira em todas as interfaces

MINHA_PORTA = 5000
# Porta que o Servidor vai ouvir

cliente1 = ("127.0.0.1", 7000)
cliente2 = ("127.0.0.1", 12000)                           

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#socket.SOCK_DGRAM=usaremos UDP

MEU_SERVIDOR = (MEU_IP, MINHA_PORTA) 
udp.bind(MEU_SERVIDOR)
# faz o bind do ip e a porta para que possa comecar a ouvir
print("O servidor está ligado!")

while(True):
    Mensagem_Recebida, END_cliente = udp.recvfrom(1024)
    # socket.recvfrom(bufsize[, flags])  deve ser uma potencia de 2
    #Recebe dados do soquete = um par (string, endereco) onde string eh uma string representando os dados recebidos
    
    if(END_cliente[1] == 7000):
        print ("Recebi =", Mensagem_Recebida.decode("utf-8"),", do cliente", END_cliente)
        # endereco eh o endereco do socket que enviou os dados.

        udp.sendto (Mensagem_Recebida, cliente2)
        print ("Enviei =", Mensagem_Recebida.decode("utf-8"),", para o cliente", cliente2)
    else:
        print ("Recebi =", Mensagem_Recebida.decode("utf-8"),", do cliente", END_cliente)
        # endereco eh o endereco do socket que enviou os dados.

        udp.sendto (Mensagem_Recebida, cliente1)
        print ("Enviei =", Mensagem_Recebida.decode("utf-8"),", para o cliente", cliente1)
    
    if(Mensagem_Recebida.decode("utf-8") == "quit"):
        print("Encerrando comunicação...")
        break

udp.close()
#fim do socket