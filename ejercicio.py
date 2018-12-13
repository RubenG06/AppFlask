import requests, psycopg2, sys, psycopg2.extras, re, time
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
	for cosa in rows:
		final = final + '<tr>'
		#print '\n\t'
		#print cosa[0]
		dt = cosa[3] 		# El dia el mes y el anno
		fecha = cosa[4]		# La hora que se ha realizado la insercion
		salida = '{0.month}/{0.day}/{0.year}'.format(dt)
		print fecha
		final = final + '<th style="border: 1px solid black; border-collapse: collapse;">' + cosa[0] + '</th><th style="border: 1px solid black; border-collapse: collapse;">' +salida+ '<th><th style="border: 1px solid black; border-collapse: collapse;">' +''+ '<th>'
		final = final + '</tr>'
		
	final = final + '</table>'
	return final

def insert_datos(results):

	resu = results[0]
 
	con = psycopg2.connect(DSN)
	cur = con.cursor()
	cur2 = con.cursor()
	# Si se quiere reiniciar los contenidos de la base de datos 
	#cur.execute("DROP TABLE info")
	#cur.execute( "CREATE TABLE public.info ( titulo text COLLATE pg_catalog.\"default\", meneos integer, click integer, fecha date, hora reltime ) WITH ( OIDS = FALSE ) TABLESPACE pg_default; ALTER TABLE public.info     OWNER to postgres;")
	
	
	nuevo = resu.replace("'","")
	
	#print 'n\t'
	print("INSERT INTO info (titulo, fecha, hora) VALUES ('"+nuevo+"', '"+ time.strftime("%m/%d/%y") +"', ' "+time.strftime("%H:%M:%S") +"');")
	cur2.execute("INSERT INTO info (titulo, fecha, hora) VALUES ('"+nuevo+"', '"+ time.strftime("%m/%d/%y") +"', ' "+time.strftime("%H:%M:%S") +"');")
	
	
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
	
