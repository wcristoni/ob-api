import requests
from flask   import Flask, request
from flask_cors import CORS
from discovery import simular

app = Flask(__name__)
CORS(app)

@app.route("/disponibilidade", methods=["GET"])
def disponibilidade():
    
    data = []
    lista_discovery = simular()

    for l in lista_discovery:
        ctrl = 'OK'
        try:
            retorno = requests.get(l[1])
            if (retorno.status_code != 200):
                ctrl = 'NOK'
            item = {
                'status': ctrl,
                'statusCode' : retorno.status_code,
                'instituicao': l[0],
                'servico': l[1]
            }
            data.append(item)
        except:
            item = {
                'status': 'NOK',
                'statusCode' : '.e.',
                'instituicao': l[0],
                'servico': l[1]
            }
            data.append(item)

    return geraResponse(200, "Processamento concluído", data)

def geraResponse(status, mensagem, dados):
    response = {}
    response["status"] = status
    response["mensagem"] = mensagem
    response["dados"] = dados

    return response

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)