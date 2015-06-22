#import nltk
#import HTMLParser
import os
import csv
import sys
from lxml import etree
import lxml.html

"""
def extrae_texto(texto, texto_ini, texto_fin):
    if texto.find(texto_ini) >= 0 :
        ini = texto.find(texto_ini)+len(texto_ini)
        if texto.find(texto_fin,ini) >= 0:
            fin = texto.find(texto_fin,ini)
            return texto[ini:fin]
    return None
"""    





dir_original = os.getcwd() #define el directorio de trabajo (donde esta este archivo)

path_htmls = os.path.join(dir_original, 'htmls') #define el directorio de los htmls
listado_htmls = os.listdir(path_htmls) #lista todos los archivos de la carpeta

resultados = []
for i in listado_htmls:

    arch = open(os.path.join(path_htmls, i))
    html = arch.read()

    arch.close()

    html_listado = etree.HTML(html)

    #Extraigo el contenedor de listado de hoteles
    hotel_list_container = html_listado.xpath("//div[@id='search-list']")
    hotel_list = hotel_list_container[0]

    #Extraigo la lista de items de hoteles
    hotels = hotel_list.xpath("//li[@class='hotel-item service-summary']")
    #print hotels
    #print len(hotels)  
    #print type(hotels)  
    #print lxml.html.tostring(hotels[0])
    #sys.exit()

    for index, hotel in enumerate(hotels):
        #hotel_id = hotel.xpath("//li[@class='hotel-item service-summary']/@id")
        #//li[@class='hotel-item service-summary']//a[@class='hotel-name']/text()
        #print hotel_id
        #print lxml.html.tostring(hotel)
        hotel_name = hotel.xpath("//li[@class='hotel-item service-summary']//a[@class='hotel-name']/text()")
        hotel_id = hotel.xpath("//li[@class='hotel-item service-summary']/@id")
        currency_price = hotel.xpath("//li[@class='hotel-item service-summary']//span[@class='currency-price']/text()")
        print "Hotel ID: ", hotel_id[index]
        print "Nombre: ", hotel_name[index]
        print "Precio: ", currency_price[index]
        #sys.exit()
        #print " "
        #print index
        #print " "
        #print "Hotel ID: ", hotel_id[0]
        print " "



    """
    localidad = ""

    if html_hotel.xpath("//div[@class='address']//a/text()"):
        localidad = html_hotel.xpath("//div[@class='address']//a/text()")
        localidad = localidad[0]
    """    

    """
    while html.find('<div class="descripcion-hotel">') >=0:

        ini = html.find('<div class="descripcion-hotel">') +1
        
        html_hotel = extrae_texto(html, '<div class="descripcion-hotel">', '<br class="clear" />')

        hotel_name = extrae_texto(html_hotel, '<h2 class="nombre-hotel">', '</h2>')
        hotel_name = nltk.clean_html(hotel_name)
        hotel_name = HTMLParser.HTMLParser().unescape(hotel_name)

        hotel_precio = extrae_texto(html_hotel, '<div class="precio-hotel">', '<div>')
        hotel_precio = nltk.clean_html(hotel_precio)
        hotel_precio = hotel_precio.replace('COP &#36;', '')
        hotel_precio = hotel_precio.replace('.', '')

        zona = extrae_texto(html_hotel, '<span class="ciudad-hotel">', '</span>')
        zona = nltk.clean_html(zona)
        zona = HTMLParser.HTMLParser().unescape(zona)
        
        resultados.append([i, hotel_name, zona, hotel_precio])

        html = html[ini:]
    """    

        

#grab archivo
"""
arch= open('lostiquetesmasbaratos.csv', 'wb')
archivo = csv.writer(arch, delimiter='|', quotechar='"', quoting=csv.QUOTE_ALL)
archivo.writerows(resultados)
arch.close()
"""
