#!lastimer-env/bin/python
import requests
import json
from operator import itemgetter

apiKey = '83ba1a28621720c492722eec77006a40'
user = 'lenizense'

def get_musicas():
    result = requests.get('https://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user='+
            user+'&api_key='+apiKey+'&format=json&limit=500')
    resultJ = json.loads(result.text)
    # o + 1 no final o for só roda até a penúltima página
    totalPages = int(resultJ['toptracks']['@attr']['totalPages']) + 1
    for i in range(2, totalPages):
        # apenas para ver o progresso
        print("\r%d de %d" % (i, totalPages-1))
        result = requests.get('http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user='+
                user+'&api_key='+apiKey+'&format=json&limit=500&page='+str(i))
        # única forma que achei para unir os itens
        for item in json.loads(result.text)['toptracks']['track']:
            resultJ['toptracks']['track'].append(item)

    lista_musicas = []
    for item in resultJ['toptracks']['track']:
        musica = {
                'title': item['name'],
                'artist': item['artist']['name'],
                'totalListenTime': int(item['playcount']) * int(item['duration'])
        }
        lista_musicas.append(musica)
    return lista_musicas

def get_artists():
    result = requests.get('http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user='+user+'&api_key='+apiKey+'&format=json&limit=1000')
    resultJ = json.loads(result.text)
    lista_artistas = []
    for item in resultJ['topartists']['artist']:
        artista = {
                'name': item['name'],
                'totalListen': 0
        }
        lista_artistas.append(artista)
    return lista_artistas


musicas = get_musicas()

artistas = get_artists()

for artista in artistas:
    for musica in musicas:
        if (musica['artist'] == artista['name']):
            artista['totalListen'] += musica['totalListenTime']

artistasOrd = sorted(artistas, key=itemgetter('totalListen')) 

for artista in artistasOrd:
    if (artista['totalListen'] is not 0):
        m, s = divmod(artista['totalListen'], 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        print(artista['name'], "%d dias %d:%02d:%02d" % (d, h, m, s))
