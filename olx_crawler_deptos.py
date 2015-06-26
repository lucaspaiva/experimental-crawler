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

print "############ Crawling simple para OLX ##############"

#Departamentos en venta de dueno
url_seed = "http://capitalfederal.olx.com.ar/nf/departamentos-casas-en-venta-cat-367/due%C3%B1o/-flo_apartaments"
url_seed = "http://www.olx.com.ar/"
print "URL Seed: "
print url_seed
print " "

x = 1
n = 1

while True:

	print "> Pagina: ", x
	print "> Ejecuto request ..."
	if x == 1:
		r = Request(url_seed)
	else:
		r = Request(next_page)	

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
		location = item.xpath(".//ul[@class='locations-tabs locations-empty locations-neighborhood']/li[3]/text()")
		location = location[0]
		link = item.xpath(".//li[@class='item  ']/a/@href")
		link = link[0]

		#navego link de detalle de inmueble para extraer el telefono
		
		print ">> Item n: ", index
		print ">> Titulo: ", title
		print ">> Descripcion: ", description
		print ">> Precio: ", price
		print ">> Zona: ", location
		

		print "## Request a pagina detalle ..."
		r = Request(link)
		html_source_detail = r.get_contents()
		#Convierto en objeto DOM con lxml
		html_detail = etree.HTML(html_source_detail)
		if html_detail.xpath(".//p[@class='icons icon-phone user-phone']/text()"):
			phone = html_detail.xpath(".//p[@class='icons icon-phone user-phone']/text()")
			phone = phone[0]
		else:
			phone = "No informa"	

		sup = item.xpath(".//ul[@class='optionals']/li[1]/span[2]/text()")
		sup = sup[0]
		amb = item.xpath(".//ul[@class='optionals']/li[4]/span[2]/text()")
		dorm = dorm[0]			

		#TODO: Aca tengo que buscar la superficie, y no me informa ambientes sino dormitorios	
		
		print ">> Superficie: ", sup
		print ">> Dormitorios: ", dorm	
		print ">> Telefono: ", phone

		print " "

		#Agrego a la lista de avisos
		articles.append([n, 
						title.encode("utf-8"), 
						description.encode("utf-8"), 
						price.encode("utf-8"),
						location.encode("utf-8"),
						dorm.encode("utf-8"),
						sup.encode("utf-8"),
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
header_columns = [["Nro","Titulo","Descripcion","Precio","Localidad","Dormitorios","Superficie","Telefono","Link"]]
file.writerows(header_columns)
file.writerows(articles)
f.close()








#print html
