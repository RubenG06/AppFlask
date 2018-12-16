import requests, psycopg2, sys, psycopg2.extras, re, time, urllib2
from lxml import html
from flask import Flask, render_template, request, redirect
from datetime import datetime


DSN = "dbname=tsr user=lab"

app = Flask(__name__) 


def enviar_datos(results):
	con = psycopg2.connect(DSN)
	cur3 = con.cursor()
	#print '\n\n\t>>>>>>>> Los datos que hay finalmente almacenado \n'
	cur3.execute("SELECT * FROM info")
	rows=cur3.fetchall()
	#print rows
	final = '<h1>NOTICIAS ENCONTRADAS: </h1><table style="width:100%">'
	final = final + '<tr>' + '<th style="border: 1px solid black; border-collapse: collapse;">' + 'TITULO' + '</th><th style="border: 1px solid black; border-collapse: collapse;">' +'FECHA OBTENCION'+ '<th><th style="border: 1px solid black; border-collapse: collapse;">' + 'HORA OBTENCION' + '<th><th style="border: 1px solid black; border-collapse: collapse;">' + 'CLICKs' + '</th>'+ '<th style="border: 1px solid black; border-collapse: collapse;">' + 'MENEOS' + '</th>' + '</tr>'
	for cosa in rows:
		final = final + '<tr>'
		#print '\n\t'
		#print cosa[0]
		dt = cosa[3] 		# El dia el mes y el anno
		hora = cosa[4]		# La hora que se ha realizado la insercion
		meneos = str(cosa[1])
		clic = str(cosa[2])
		salida = '{0.month}/{0.day}/{0.year}'.format(dt)
		salida2 = str(hora)
		#print salida2
		final = final + '<th style="border: 1px solid black; border-collapse: collapse;">' + cosa[0] + '</th><th style="border: 1px solid black; border-collapse: collapse;">' +salida+ '<th><th style="border: 1px solid black; border-collapse: collapse;">' +salida2+ '<th><th style="border: 1px solid black; border-collapse: collapse;">' + clic + '</th>'+ '<th style="border: 1px solid black; border-collapse: collapse;">' + meneos + '</th>'
		final = final + '</tr>'
		
	final = final + '</table>'
	return final

def gethtml():
	url = 'http://www.meneame.net'
	req = urllib2.Request(url)	
	return urllib2.urlopen(req).read()

def insert_datos(results):

	# Veo el numero de clicks
	#Obtengo el html
	texto_html =  gethtml()
	#Busco las coincidencias con el patron
	patron = re.compile('<div class="clics">  [1-9]+ clics  </div>')
	resultado = patron.findall(texto_html)
	# Me quedo con solo la informacion de la primera noticia
	#print resultado[0] 
	# Ahora recortare el string
	patron2 = re.compile('[1-9]+')
	numero = patron2.findall(resultado[0])
	clic = str(numero[0])
	
	
	#Veo ahora el numero de meneos
	patron3 = re.compile('[1-9]+</a> meneos </div>')
	resultado3 = patron3.findall(texto_html)
	numero2 = patron2.findall(resultado3[0])
	meneos = str(numero2[0])
	
	#Veo el titulo de la noticia

	resu = results[0]
 
	con = psycopg2.connect(DSN)
	cur = con.cursor()
	cur2 = con.cursor()
	# Si se quiere reiniciar los contenidos de la base de datos
	#cur.execute("DELETE FROM INFO")	
	#cur.execute("DROP TABLE info")
	#cur.execute( "CREATE TABLE public.info ( titulo text COLLATE pg_catalog.\"default\", meneos integer, click integer, fecha date, hora reltime ) WITH ( OIDS = FALSE ) TABLESPACE pg_default; ALTER TABLE public.info     OWNER to postgres;")
	
	
	nuevo = resu.replace("'","")
	
	#print 'n\t'
	#print("INSERT INTO info (titulo, fecha, hora, click) VALUES ('"+nuevo+"', '"+ time.strftime("%m/%d/%y") +"', ' "+time.strftime("%H:%M:%S") +"' , "+clic+" );")
	cur2.execute("INSERT INTO info (titulo, fecha, hora, click, meneos) VALUES ('"+nuevo+"', '"+ time.strftime("%m/%d/%y") +"', ' "+time.strftime("%H:%M:%S") +"' , "+clic+" ," + meneos+ " );")
	
	
	con.commit()


def download(url):
    
    r = requests.get(url)
    if r.status_code != 200:
        sys.stderr.write("! Error {} retrieving url {}".format(r.status_code, url))
        return None
    return r

	
@app.route('/')
def my_form():
	url = "http://www.meneame.net"
	page = download(url)
	
	if page:
		tree = html.fromstring(page.content)
		xpath_string = '//h2/a/text()'
        results = tree.xpath(xpath_string)
		
	insert_datos(results)
	#return '\n\t'.join(results)
	return enviar_datos(results)
	

	
if __name__ == "__main__":
	app.run(host='0.0.0.0') 
	
