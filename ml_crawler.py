"""
Crawler para mercadolibre inmuebles
TODO: aca deberia crear una carpeta classes para poner mi clase request e importarla como modulo
"""

from request import Request

url_seed = "http://inmuebles.mercadolibre.com.ar/venta/due%C3%B1o_DisplayType_LF"

r = Request(url_seed)
#Envio peticion y obtengo contenido
status = r.get_status_response()
html = r.get_contents()

print html