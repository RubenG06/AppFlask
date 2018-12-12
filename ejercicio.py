import requests, psycopg2, sys, psycopg2.extras, re, time
from lxml import html
from flask import Flask, render_template, request, redirect


DSN = "dbname=tsr user=lab"

app = Flask(__name__) 


def enviar_datos(results):
	con = psycopg2.connect(DSN)
	cur3 = con.cursor()
	#print '\n\n\t>>>>>>>> Los datos que hay finalmente almacenado \n'
	cur3.execute("SELECT * FROM info")
	rows=cur3.fetchall()
	#print rows
	final = '<h1>NOTICIAS ENCONTRADAS: </h1>'
	for cosa in rows:
		#print '\n\t'
		#print cosa[0]
		final = final + '<p>' + cosa[0] + '  >>>  </p>'
	return final

def insert_datos(results):

 
	con = psycopg2.connect(DSN)
	cur = con.cursor()
	cur2 = con.cursor()
	cur.execute("Delete from info")
	#cur.execute( "CREATE TABLE public.info ( titulo text COLLATE pg_catalog.\"default\", meneos integer, click integer, fecha date ) WITH ( OIDS = FALSE ) TABLESPACE pg_default; ALTER TABLE public.info     OWNER to postgres;")
	
	for art in results: 
	
		nuevo = art.replace("'","")
	
		#print 'n\t'
		print("INSERT INTO info (titulo, fecha) VALUES ('"+nuevo+"', '"+ time.strftime("%d/%m/%y") +"');")
		cur2.execute("INSERT INTO info (titulo, fecha) VALUES ('"+nuevo+"', '"+ time.strftime("%d/%m/%y") +"');")
	
	
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
	
