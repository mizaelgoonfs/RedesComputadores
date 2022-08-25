import socket

IP_Servidor = '127.0.0.1' 
# Endereco IP do Servidor
             
PORTA_Servidor = 5000                  
# Porta em que o servidor estara ouvindo

MEU_IP = ''                                
# Endereco IP '' = significa que ouvira em todas as interfaces

MINHA_PORTA = 7000
# Porta que o cliente1 vai ouvir

cliente1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#  socket.SOCK_DGRAM=usaremos UDP

cliente1_serv = (MEU_IP, MINHA_PORTA) 
cliente1.bind(cliente1_serv)
# faz o bind do ip e a porta para que possa comecar a ouvir
print("O cliente1 está ligado!")

DESTINO = (IP_Servidor, PORTA_Servidor) 
#destino(IP + porta) do Servidor

while(True):
    Mensagem = input("Digite a mensagem: ")   
    # Mensagem recebera dados do teclado           

    cliente1.sendto (Mensagem.encode(), DESTINO)
    # enviar a mensgem para o destino(IP + porta)
    #bytes(Mensagem,"utf8") = converte tipo  str para byte
    
    if(Mensagem == "quit"):
        print("Encerrando comunicação...")
        break

    Mensagem_Recebida, END_cliente = cliente1.recvfrom(1024)
    if len(Mensagem_Recebida) is not None:
        print ("Recebi =", Mensagem_Recebida.decode("utf-8"),", do cliente", END_cliente, "\n")
        # endereco eh o endereco do socket que enviou os dados.      

cliente1.close()
# fim socket