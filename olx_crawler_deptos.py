"""
Crawler para OLX inmuebles
TODO: aca deberia crear una carpeta classes para poner mi clase request e importarla como modulo
"""
#Librerias sistema
from lxml import etree
import lxml.html
import sys
import os
import csv
#Libs, clases propias
from request import Request
#Vars
articles = []
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}
method_type = "get"

print "############ Crawling simple para OLX ##############"

#Departamentos en venta de dueno
url_seed = "http://capitalfederal.olx.com.ar/nf/departamentos-casas-en-venta-cat-367/due%C3%B1o/-flo_apartaments"
print "URL Seed: "
print url_seed
print " "

x = 1
n = 1	

while True:

	print "> Pagina: ", x
	print "> Ejecuto request ..."
	if x == 1:
		r = Request(url_seed,method_type,headers)
	else:
		r = Request(next_page,method_type,headers)	

	#Envio peticion y obtengo contenido
	status = r.get_status_response()
	html_source = r.get_contents()
	#Convierto en objeto DOM con lxml
	html = etree.HTML(html_source)

	#Aca ejecuto el crawling de la pagina
	##################################################
	#Comienzo el parseo, extraigo el html del listado 
	items = html.xpath(".//ul[@class='items-list ']/li")

	print "> Extraccion de datos ..."
	for index, item in enumerate(items):
		n+=1
		#extraigo datos
		title = item.xpath(".//div[@class='items-info']/h3/text()")
		title = title[0]
		description = item.xpath(".//div[@class='items-info']/span/text()")
		description = description[0]
		price = item.xpath(".//p[@class='items-price']/text()")
		price = price[0]
		price = price.strip()
		link = item.xpath(".//a[@data-qa='list-item']/@href")
		link = link[0]
		
		print ">> Item n: ", index
		print ">> Titulo: ", title
		print ">> Descripcion: ", description
		print ">> Precio: ", price
		

		#navego link de detalle de inmueble para extraer el telefono
		print ">> Link detalle: ", link
		print "## Request a pagina detalle ..."
		r = Request(link,method_type,headers)
		html_source_detail = r.get_contents()
		#Convierto en objeto DOM con lxml
		html_detail = etree.HTML(html_source_detail)
		if html_detail.xpath(".//p[@class='icons icon-phone user-phone']/text()"):
			phone = html_detail.xpath(".//p[@class='icons icon-phone user-phone']/text()")
			phone = phone[0]
		else:
			phone = "No informa"	

		#Los datos de superficie y dormitorio no siempre estan, entonces en la evaluacion
		#xpath lo que hay que hacer es usar el contain, y preguntar si existe antes de definir la variable
		#hay fichas que no tienen este dato . 	
		#/a[contains(text(), 'programming')]/@href
		#sup = html_detail.xpath(".//ul[@class='optionals']/li[1]/span[contains(text(), 'Metros Cuadrados')]/text()")
		#sup = sup[0]
		#dorm = html_detail.xpath(".//ul[@class='optionals']/li[4]/span[2]/text()")
		#dorm = dorm[0]
		location = html_detail.xpath(".//li[@class='icons icon-pin']/text()")
		location = location[0]			
		

		#TODO: Aca tengo que buscar la superficie, y no me informa ambientes sino dormitorios	
		
		#print ">> Superficie: ", sup
		#print ">> Dormitorios: ", dorm	
		print ">> Telefono: ", phone
		print ">> Zona: ", location

		print " "

		#Agrego a la lista de avisos
		articles.append([n, 
						title.encode("utf-8"), 
						description.encode("utf-8"), 
						price.encode("utf-8"),
						location.encode("utf-8"),
						#dorm.encode("utf-8"),
						#sup.encode("utf-8"),
						phone.encode("utf-8"),
						link.encode("utf-8")
						])

	##################################################

	#Busco la siguiente pagina
	if html.xpath(".//a[@class='icons pagination-arrow icon-arrow-right ']/@href"):
		next_page = html.xpath(".//a[@class='icons pagination-arrow icon-arrow-right ']/@href")
		next_page = next_page[0]
	else:
		next_page = None

	

	print "> Proxima pagina: "
	print next_page
	print " "
	print " "

	x += 1

	#Si no hay mas paginas viene en None, entonces salgo
	if next_page == None:	
		last_page = True
		print "Fin paginacion"
	else:
		last_page = False

	if last_page:
		break

#grab archivo
print " "
print "> Grabo archivo"   
f= open('results_olx_deptos_dueno.csv', 'wb')   
file = csv.writer(f, delimiter='|', quotechar='"', quoting=csv.QUOTE_ALL)
header_columns = [["Nro","Titulo","Descripcion","Precio","Localidad","Telefono","Link"]]
file.writerows(header_columns)
file.writerows(articles)
f.close()








#print html
