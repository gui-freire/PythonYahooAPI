import socket

HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 9999            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Cria objeto com endereço e porta
dest = (HOST, PORT)
tcp.connect(dest)
print ('Para sair use CTRL+X\n')
msg = ''
while msg != '\x18':
    print('Digite a cidade que deseja saber a previsão do tempo(Ex.: São Paulo): ')
    msg = input()
    #Encoda a mensagem em UTF-8 para que possa ser enviada
    tcp.send (msg.encode('utf-8'))

    print('Agora, digite o estado que essa cidade pertence(Ex.: SP): ')
    msg = input()
    tcp.send (msg.encode('utf-8'))

    #Recebe mensagem do servidor
    msgReceived = tcp.recv(2048).decode('utf-8')
    while msgReceived != '':
        print(msgReceived)
        msgReceived = tcp.recv(2048).decode('utf-8')
tcp.close()
