import requests, psycopg2, sys, psycopg2.extras, re, time, urllib2
from lxml import html
from flask import Flask, render_template, request, redirect
from datetime import datetime

# Informacion de la base de datos y flask 

DSN = "dbname=tsr user=lab"

app = Flask(__name__) 


def enviar_datos(results):
	con = psycopg2.connect(DSN)
	cur3 = con.cursor()
	#Consultamos los datos
	cur3.execute("SELECT * FROM info ORDER BY fecha, hora DESC")
	rows=cur3.fetchall()
	#Imprimimos los datos 
	final = '<h1>NOTICIAS ENCONTRADAS: </h1><table style="width:100%">'
	final = final + '<tr style="background-color: orange;">' + '<th style="border: 1px double blue; border-collapse: collapse;">' + 'TITULO' + '</th><th style="border: 1px solid blue; border-collapse: collapse;">' +'FECHA OBTENCION'+ '<th><th style="border: 1px solid blue; border-collapse: collapse;">' + 'HORA OBTENCION' + '<th><th style="border: 1px solid blue; border-collapse: collapse;">' + 'CLICKs' + '</th>'+ '<th style="border: 1px solid blue; border-collapse: collapse;">' + 'MENEOS' + '</th>' + '</tr>'
	for cosa in rows:
		final = final + '<tr style="background-color: Aquamarine;">'
		dt = cosa[3] 		# El dia el mes y el anno
		hora = cosa[4]		# La hora que se ha realizado la insercion
		meneos = str(cosa[1])
		clic = str(cosa[2])
		#salida = '{0.month}/{0.day}/{0.year}'.format(dt)
		salida = str(dt)
		salida2 = str(hora)
		final = final + '<th style="border: 1px double blue; border-collapse: collapse;"><h3>' + cosa[0] + '</h3></th><th style="border: 1px double blue; border-collapse: collapse;">' +salida+ '<th><th style="border: 1px solid blue; border-collapse: collapse;">' +salida2+ '<th><th style="border: 1px solid blue; border-collapse: collapse;">' + clic + '</th>'+ '<th style="border: 1px solid blue; border-collapse: collapse;">' + meneos + '</th>'
		final = final + '</tr>'
		
	final = final + '</table>'
	return final

def gethtml():
	url = 'http://www.meneame.net'
	req = urllib2.Request(url)	
	return urllib2.urlopen(req).read()

def insert_datos(results, r_c, r_m):

	# Obtenemos el titulo con el numero de clics y meneos 
	cl = r_c[0]
	
	# eliminamos parte de la etiqueta 
	nuevo_c = cl.replace(" clics","")
	clic = int(nuevo_c)
	meneos = int(r_m[0])

	resu = results[0]
 
	con = psycopg2.connect(DSN)
	cur = con.cursor()
	cur2 = con.cursor()
	# Si se quiere reiniciar los contenidos de la base de datos
	#cur.execute("DELETE FROM INFO")	
	#cur.execute("DROP TABLE info")
	#cur.execute( "CREATE TABLE public.info ( titulo text COLLATE pg_catalog.\"default\", meneos integer, click integer, fecha date, hora reltime ) WITH ( OIDS = FALSE ) TABLESPACE pg_default; ALTER TABLE public.info     OWNER to postgres;")
	
	# Eliminamos las comillas simples para que no de problemas el programa 
	nuevo = resu.replace("'","")
	
	# Obtenemos las fechas en el formato correcto
	f = time.strftime("%m/%d/%y")
	h = time.strftime("%H:%M:%S")
	#Ejecutamos la consulta 
	query = 'insert into info (titulo, meneos, click, fecha, hora) values (\'%s\',%d, %d, \'%s\', \'%s\' );' % (nuevo, clic,meneos, f, h)
	cur2.execute(query)
	
	print 'Operacion realizada'
	
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
	
	#Obtenemos la informacion y filtramos lo que deseemos con xpath y xquery
	
	if page:
		tree = html.fromstring(page.content) 
		xpath_string = '//h2/a/text()'
		xpath_string_clics = '//div[contains(@class,"clics")]/text()'
		xpath_string_meneos = '//div[contains(@class,"votes")]/a/text()'
		results = tree.xpath(xpath_string)
		r_c = tree.xpath(xpath_string_clics)
		r_m = tree.xpath(xpath_string_meneos)
		
	
	insert_datos(results, r_c, r_m)
	return enviar_datos(results)
	

	
if __name__ == "__main__":
	app.run(host='0.0.0.0') 
	