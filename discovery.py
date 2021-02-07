import json
import requests

def simular():
    participantes = requests.get('https://data.directory.openbankingbrasil.org.br/participants')
    participantes_json = participantes.json()

    lista_discovery = []
    instituicao = ''
    for participante in participantes_json:
        for nome in participante['AuthorisationServers']:
            instituicao = nome['CustomerFriendlyName'] + ' [' + participante['RegisteredName'] + ']'
            for api in nome['ApiResources']:
                if (api['ApiFamilyType'] == 'discovery'):
                    for endp in api['ApiDiscoveryEndpoints']:
                        if (endp['ApiEndpoint'][-6:]=='status' or endp['ApiEndpoint'][-7:]=='outages'):
                            lista_discovery.append([instituicao, endp['ApiEndpoint']])
                        elif (endp['ApiEndpoint'][-1:]=='/'):
                            lista_discovery.append([instituicao, endp['ApiEndpoint'] + 'status'])
                        else:
                            lista_discovery.append([instituicao, endp['ApiEndpoint'] + '/status'])

    return lista_discovery

if __name__ == '__main__':

    lista_discovery = simular()
    for l in lista_discovery:
        retorno = ''
        data = ''
        try:
            retorno = requests.get(l[1])
            print(str(retorno.status_code) + ' - ' + l[0] + ' - ' + l[1])
        except:
            print('.e.' + ' - ' + l[0] + ' - ' + l[1])
        