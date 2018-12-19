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
	final = final + '<tr>' + '<th style="border: 1px double blue; border-collapse: collapse;">' + 'TITULO' + '</th><th style="border: 1px solid blue; border-collapse: collapse;">' +'FECHA OBTENCION'+ '<th><th style="border: 1px solid blue; border-collapse: collapse;">' + 'HORA OBTENCION' + '<th><th style="border: 1px solid blue; border-collapse: collapse;">' + 'CLICKs' + '</th>'+ '<th style="border: 1px solid blue; border-collapse: collapse;">' + 'MENEOS' + '</th>' + '</tr>'
	for cosa in rows:
		final = final + '<tr>'
		#print '\n\t'
		#print cosa[0]
		dt = cosa[3] 		# El dia el mes y el anno
		hora = cosa[4]		# La hora que se ha realizado la insercion
		meneos = str(cosa[1])
		clic = str(cosa[2])
		#salida = '{0.month}/{0.day}/{0.year}'.format(dt)
		salida = str(dt)
		salida2 = str(hora)
		#print salida2
		final = final + '<th style="border: 1px double blue; border-collapse: collapse;"><h3>' + cosa[0] + '</h3></th><th style="border: 1px double blue; border-collapse: collapse;">' +salida+ '<th><th style="border: 1px solid blue; border-collapse: collapse;">' +salida2+ '<th><th style="border: 1px solid blue; border-collapse: collapse;">' + clic + '</th>'+ '<th style="border: 1px solid blue; border-collapse: collapse;">' + meneos + '</th>'
		final = final + '</tr>'
		
	final = final + '</table>'
	return final

def gethtml():
	url = 'http://www.meneame.net'
	req = urllib2.Request(url)	
	return urllib2.urlopen(req).read()

def insert_datos(results, r_c, r_m):

	cl = r_c[0]
	
	nuevo_c = cl.replace(" clics","")
	clic = int(nuevo_c)
	print clic
	meneos = int(r_m[0])
	print meneos

	resu = results[0]
 
	con = psycopg2.connect(DSN)
	cur = con.cursor()
	cur2 = con.cursor()
	# Si se quiere reiniciar los contenidos de la base de datos
	#cur.execute("DELETE FROM INFO")	
	#cur.execute("DROP TABLE info")
	#cur.execute( "CREATE TABLE public.info ( titulo text COLLATE pg_catalog.\"default\", meneos integer, click integer, fecha date, hora reltime ) WITH ( OIDS = FALSE ) TABLESPACE pg_default; ALTER TABLE public.info     OWNER to postgres;")
	
	
	nuevo = resu.replace("'","")
	
	print 'PASO POR AQUUIIIIIIIIIIIIIIIIIIIIIIIIII'
	f = time.strftime("%m/%d/%y")
	h = time.strftime("%H:%M:%S")
	#print 'n\t'
	#print "INSERT INTO info (titulo, fecha, hora, click, meneos) VALUES ('"+nuevo+"', '"+ time.strftime("%m/%d/%y") +"', ' "+time.strftime("%H:%M:%S") +"' , "+clic+" ," + meneos+ " );"
	
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
	
	
	
	if page:
		tree = html.fromstring(page.content) 
		xpath_string = '//h2/a/text()'
		xpath_string_clics = '//div[contains(@class,"clics")]/text()'
		xpath_string_meneos = '//div[contains(@class,"votes")]/a/text()'
		results = tree.xpath(xpath_string)
		r_c = tree.xpath(xpath_string_clics)
		r_m = tree.xpath(xpath_string_meneos)
		
	
	insert_datos(results, r_c, r_m)
	#return '\n\t'.join(results)
	return enviar_datos(results)
	

	
if __name__ == "__main__":
	app.run(host='0.0.0.0') 
	