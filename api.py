#!flask/bin/python
from flask import Flask
from flask import request
from service import Recomendacao
import simplejson as json

app = Flask(__name__)

@app.route('/recomendacoes/capturas', methods=['PUT'])
def capturaDados():
	if request.is_json:
		content = request.get_json()
		print(content)
		recomendacao = Recomendacao()
		return recomendacao.capturarAcessoUsuario(content)
    
@app.route('/recomendacoes/<idUsuario>')
def recomendarParaUsuario(idUsuario):
	recomendacao = Recomendacao()	
	return recomendacao.getRecomendacoes(idUsuario)
	
@app.route('/recomendacoes/usuarios/<idUsuario>')
def obterUsuariosSimilares(idUsuario):
	recomendacao = Recomendacao()
	return recomendacao.getSimilaresPorUsuario(idUsuario)

@app.route('/recomendacoes', methods=['post'])
def recomendar():
	return null


app.run(host='0.0.0.0', port=5000)
