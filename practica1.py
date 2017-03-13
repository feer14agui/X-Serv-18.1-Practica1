#!/usr/bin/python3

import webapp
import csv
import os

class contentApp (webapp.webApp):
   # Declare and initialize content
	urls_Acotadas = {}
	sec_urls = {}
	secuencia = -1
	httpCode = " "
	htmlBody = " "


	def escribirURL(self,urlLong,urlShort):
		with open("fich.csv", "a") as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow([int(urlShort)] + [urlLong])
		return None

	def leerDicc(self,file):

		with open('fich.csv', 'r') as csvfile:
			if os.stat('fich.csv').st_size == 0: #si es igual a 0 el fichero esta vacio
				print("EL FICHERO ESTA VACIO")
			else:
				reader = csv.reader(csvfile)
				for row in reader: #siguiendo lo que hemos hecho, row[0] = urlshort y row[1] = urlLong
					self.urls_Acotadas[row[1]] = int(row[0])
					self.sec_urls[int(row[0])] = row[1]
					self.secuencia = self.secuencia + 1
				return None 

	def parse(self, request):

		recurso = request.split(' ', 2)[1]
		metodo = request.split(' ', 2)[0]

		if metodo == "POST":
			cuerpo = request.split('\r\n\r\n', 1)[1]
			cuerpo = cuerpo.split("=")[1].replace("+", " ")
		elif metodo == "GET":
			cuerpo = ""

		return (metodo, recurso, cuerpo)
	
	def process(self, resourceName):
		
		global httpCode, htmlBody

		(metodo, recurso, cuerpo) = resourceName
		formulario = '<form action="" method="POST">'
		formulario += 'Acortar url: <input type="text" name="valor">'
		formulario += '<input type="submit" value="Enviar">'
		formulario += '</form>'

		if len(self.urls_Acotadas) == 0:
			self.leerDicc('fich.csv')
		if metodo == "GET":
			if recurso == "/":
				httpCode = "200 OK"
				htmlBody = "<html><body>" + formulario\
								+ "<p>" + str(self.urls_Acotadas)\
								+ "</p></body></html>"
			else:

				try:
					recurso = int(recurso[1:])
					if recurso in self.sec_urls:
						httpCode = "300 Redirect"
						htmlBody = "<html><body><meta http-equiv='refresh'"\
										+ "content='1 url="\
										+ self.sec_urls[recurso] + "'>"\
										+ "</p>" + "</body></html>"
					else:
						httpCode = "404 Not Found"
						htmlBody = "<html><body>"\
										+ "Error: Recurso no disponible"\
										+ "</body></html>"
				except ValueError:
					httpCode = "404 Not Found"
					htmlBody = "<html><body>"\
									+ "Error: Recurso no disponible"\
									+ "</body></html>"

			return (httpCode, htmlBody)

		elif metodo == "POST":
			print(cuerpo)

			if cuerpo == "":
				httpCode = "404 Not Found"
				htmlBody = "<html><body>"\
								+ "Error: no se introdujo ninguna url"\
		                  + "</body></html>"
				return(httpCode, htmlBody)
			elif cuerpo.find("http") == -1:
				cuerpo = "http://" + cuerpo
				while cuerpo.find("%2F") != -1:
					cuerpo = cuerpo.replace("%2F", "/")
				self.secuencia = self.secuencia + 1
				secuencia = self.secuencia
				self.urls_Acotadas[cuerpo] = secuencia
				self.sec_urls[secuencia] = cuerpo
				self.escribirURL(cuerpo,secuencia)
				httpCode = "200 OK"
				htmlBody = "<html><body>"\
							+ "<a href=" + cuerpo + ">" + cuerpo + "</href>"\
							+ "<p><a href=" + str(secuencia) + ">" + str(secuencia)\
							+ "</href></body></html>"
			else:
				
				while cuerpo.find("%2F") != -1:
					print("hola")
					cuerpo = cuerpo.replace("%2F", "/")
					if cuerpo in self.urls_Acotadas:
						secuencia = self.urls_Acotadas[cuerpo]
						self.secuencia = self.secuencia + 1
						secuencia = self.secuencia
						self.urls_Acotadas[cuerpo] = secuencia
						self.sec_urls[secuencia] = cuerpo
						self.escribirURL(cuerpo,secuencia)
						httpCode = "200 OK"
						htmlBody = "<html><body>"\
									+ "<a href=" + cuerpo + ">" + cuerpo + "</href>"\
									+ "<p><a href=" + str(secuencia) + ">" + str(secuencia)\
									+ "</href></body></html>"
					else:
						cuerpo = "http://" + cuerpo[9:]
						self.secuencia = self.secuencia + 1
						secuencia = self.secuencia
						self.urls_Acotadas[cuerpo] = secuencia
						self.sec_urls[secuencia] = cuerpo
						self.escribirURL(cuerpo,secuencia)
						httpCode = "200 OK"
						htmlBody = "<html><body>"\
									+ "<a href=" + cuerpo + ">" + cuerpo + "</href>"\
									+ "<p><a href=" + str(secuencia) + ">" + str(secuencia)\
									+ "</href></body></html>"
			print(self.urls_Acotadas)
			return (httpCode, htmlBody)

		else:

			httpCode = "404 Not Found"
			htmlBody = "<html><body>Metodo no soportado</body></html>"

			return (httpCode, htmlBody)



if __name__ == "__main__":
    try:
        testWebApp = contentApp("localhost", 1234)
    except KeyboardInterrupt:
        print ("")
        print ("Finalizando aplicación")
