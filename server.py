import socket

def parseJsonToString(json, con):
    for item in json:
        #Esvazia todos os campos utilizados para evitar erros/utilização de dados errados
        location = ''
        forecast = ''
        string = ''
        obj = ''
        #Seleciona objeto do JSON com informações da localização
        location = item['location']
        obj += obj + 'Previsão para ' + location['city'] + ', ' + location['region'] + ' - ' + location['country'] + '\n \n'
        forecast = item['item']['forecast']
        for weather in forecast:
            string = weather['date'] + "\n Temperatura Máxima: " + weather['high'] + "ºC \n Temperatura mínima: " + weather['low'] + "ºC \n"
            obj = obj + "\n" + string
        #String com informações de temperatura são enviados ao client
        con.send(obj.encode('utf-8'))


import requests
import json
def getWeather(city, state, con):
    #URL do serviço do Yahoo Weather
    url = "https://query.yahooapis.com/v1/public/yql"
    print('URL definida')

    #A busca se dá por uma query própria do Yahoo
    #Aqui definimos essa query e qual cidade e estado ela irá buscar
    query = "select * from weather.forecast where woeid in (SELECT woeid FROM geo.places WHERE text='({}, {})') and u = 'c'"
    print('query definida')

    #Define os parametros que serão passados para a URL
    params = {}
    params['q'] = query.format(city, state)
    params['format'] = 'json'

    #Realiza chamada ao serviço
    result = requests.get(url, params = params)

    data = result.json()
    #Busca no JSON retornado o campo com as previsões para os próximos dias
    jsonReceived = data['query']['results']['channel']

    #Trata os dados retornados para serem mostrados ao usuário
    parseJsonToString(jsonReceived, con)

def main():
    HOST = '127.0.0.1'              # Endereco IP do Servidor
    PORT = 9999            # Porta que o Servidor esta
    print('Porta e Hosts definidos')
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('socket definido')
    #Cria objeto com endereço e porta
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(2)
    while True:
        #Aceita conexão do Cliente
        con, cliente = tcp.accept()
        print ('Conectado por', cliente)
        while True:
            #Recebe mensagem enviada pelo cliente
            #Pela mensagem ser encoded em UTF-8, ela vem com algumas 'sujeiras', por isso é preciso
            #decodifica-la para passar ao método
            city = con.recv(2048).decode('utf-8')
            state = con.recv(2048).decode('utf-8')

            getWeather(city, state, con)
            
        print ('Finalizando conexao do cliente', cliente)
        con.close()


main()