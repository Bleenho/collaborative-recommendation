from math import sqrt
import threading
import simplejson as json
import os
import platform

class Recomendacao:
	
	def getRecomendacoes(self, usuario):
		with open(os.getcwd() + self.fatchSystemBar() + 'base_recomendacao.json', 'r', encoding="utf-8") as json_file:
			data = json.load(json_file)
			user = data.get(usuario)
		return json.dumps(user, indent=4, use_decimal=True)

	def fatchSystemBar(self):
		if platform.system() == 'Linux':
			return '/model/'
		return '\\model\\'	
	
	def roboDeRecomendacoes(self, usuario):
		totais={}
		somaSimularidade={}
		base = json.loads(self.obtemBase())
		for outro in base:
			if outro == usuario: continue
			similaridade = self.euclidiana(base, usuario, outro)
			if similaridade <= 0: continue

			for item in base[outro]:
				if item not in base[usuario]:
					totais.setdefault(item, 0)
					totais[item] += base[outro][item] * similaridade
					somaSimularidade.setdefault(item, 0)
					somaSimularidade[item] += similaridade
		
		rankings=[]
		for item, total in totais.items():
			rankings.append({item: total / somaSimularidade[item]})
		print(rankings)
		
		print (rankings)
		self.writeRecomendation(rankings, usuario)
		#datas = json.dumps(rankings, indent=4, use_decimal=True)
		#return datas
	
	def writeRecomendation(self, dados, usuario):
		with open(os.getcwd() + self.fatchSystemBar() + 'base_recomendacao.json', 'r', encoding="utf-8") as json_file:
			data = json.load(json_file)
			user = data.get(usuario)
		with open(os.getcwd() + self.fatchSystemBar() + 'base_recomendacao.json', 'w') as json_file:
			data.update({usuario : dados})
			json.dump(data, json_file, indent=2)
			
	def euclidiana(self, base, user, usuario):
		si = {}
		for item in base[user]:
			if item in base[usuario]: si[item] = 1
		if len(si) == 0: return 0
		soma = sum({pow(base[user][item] - base[usuario][item], 2)
					for item in base[user] if item in base[usuario]})
		return 1/(1 + sqrt(soma))
               
	def getSimilares(self, base, usuario):
		similaridade = [(self.euclidiana(base, usuario, outro), outro)
						for outro in base if outro != usuario]
		similaridade.sort()
		similaridade.reverse()
		return similaridade
		
		
	
	def getSimilaresPorUsuario(self, usuario):
		base = json.loads(self.obtemBase())
		similaridade = [(self.euclidiana(base, usuario, outro), outro)
						for outro in base if outro != usuario]
		similaridade.sort()
		similaridade.reverse()
		return json.dumps(similaridade, indent=4, use_decimal=True)
		
	def obtemBase(self):
		with open(os.getcwd() + self.fatchSystemBar() + 'base_captura.json', 'r') as json_file:
			data = json.load(json_file)
		dataJson = json.dumps(data, indent=4, use_decimal=True)
		print(dataJson)
		return dataJson
	
	
		
	def capturarAcessoUsuario(self, acesso):
		with open(os.getcwd() + self.fatchSystemBar() + 'base_captura.json', 'r') as json_file:
			data = json.load(json_file)
			userName = acesso['idUsuario']
			print(userName)
			user = data.get(userName)
		with open(os.getcwd() + self.fatchSystemBar() + 'base_captura.json', 'w') as json_file:
			if user:
				print(data[userName])
				if(float(data[userName].get(acesso['idArtigo'])) < float(acesso['peso'])):
					data[userName].update({ acesso['idArtigo'] : acesso['peso']})
				json.dump(data, json_file, indent=2)
			else:
				data.update({userName : { acesso['idArtigo'] : acesso['peso']}})
				json.dump(data, json_file, indent=2)
				print (data)
		t = threading.Thread(target=self.roboDeRecomendacoes(acesso['idUsuario']))
		t.start()
		return json.dumps({'sucesso': 'true', 'mensagem': 'Acesso capturado!'}, indent=4, use_decimal=True)
		
		
		
		
		