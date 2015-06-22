"""
Crawler para mercadolibre inmuebles
TODO: aca deberia crear una carpeta classes para poner mi clase request e importarla como modulo
"""
#Librerias sistema
from lxml import etree
import lxml.html
#Libs, clases propias
from request import Request

#Departamentos en venta de dueno
#url_seed = "http://inmuebles.mercadolibre.com.ar/departamentos/due%C3%B1o_DisplayType_LF_PrCategId_AD"
#Departamentos en venta dueno capital federal
url_seed = "http://inmuebles.mercadolibre.com.ar/departamentos/capital-federal/due%C3%B1o_DisplayType_LF_PrCategId_AD"

r = Request(url_seed)
#Envio peticion y obtengo contenido
status = r.get_status_response()
html_source = r.get_contents()
#Convierto en objeto DOM con lxml
html = etree.HTML(html_source)

#Comienzo el parseo, extraigo el html del listado 
items = html.xpath(".//li[@class='list-view-item rowItem']")

for index, item in enumerate(items):
	#extraigo datos
	title = item.xpath(".//h3[@class='list-view-item-title']/a[1]/text()")
	title = title[0]
	description = item.xpath(".//p[@class='list-view-item-subtitle']/text()")
	description = description[0]
	price = item.xpath(".//span[@class='price-info-cost']/strong[@class='ch-price']/text()")
	price = price[0]
	location = item.xpath(".//li[@class='extra-info-location']/text()")
	location = location[0]
	link = item.xpath(".//h3[@class='list-view-item-title']/a/@href")
	link = link[0]
	sup = item.xpath(".//ul[@class='classified-details']/li[1]/text()")
	sup = sup[0]
	amb = item.xpath(".//ul[@class='classified-details']/li[2]/text()")
	amb	= amb[0]

	#navego link de detalle de inmueble para extraer el telefono
	link_with_phone = link + "?noIndex=true&showPhones=true"
	print "Item n: ", index
	print "Titulo: ", title
	print "Descripcion: ", description
	print "Precio: ", price
	print "Zona: ", location
	print "Superficie: ", sup
	print "Ambientes: ", amb

	print "Request a pagina detalle ..."
	r = Request(link_with_phone)
	html_source_detail = r.get_contents()
	#Convierto en objeto DOM con lxml
	html_detail = etree.HTML(html_source_detail)
	if html_detail.xpath(".//span[@class='seller-details-box showPhone']/text()"):
		phone = html_detail.xpath(".//span[@class='seller-details-box showPhone']/text()")
		phone = phone[0]
	else:
		phone = "No informa"	
	print "Telefono: ", phone

	print " "



#print html
