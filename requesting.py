import requests

url = "http://capitalfederal.olx.com.ar/nf/departamentos-casas-en-venta-cat-367/due%C3%B1o/-flo_apartaments"

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}

r = requests.post(url, headers=headers)

print "Status: ", r.status_code
print " "
print "Headers: ", r.headers
print " "
print "Contenido: "
print r.content