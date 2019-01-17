#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests, psycopg2, sys, psycopg2.extras, re, time, urllib2, traceback, logging
from lxml import html
from flask import Flask, render_template, request, redirect
from datetime import datetime

# Base de datos e información necesaria de flask
DSN = "dbname=tsr user=lab"
app = Flask(__name__) 

# Al acceder al primer directorio nos imprimirá nuestro template
@app.route('/')
def my_form():
	return render_template("my-form.html")
	
@app.route('/', methods=['POST'])
def my_form_post():
	text = request.form['text'] #Obtengo el parametro
	print 'Buscando por ' + text
	num_bus = int(text)
	
	con = psycopg2.connect(DSN)
	cur3 = con.cursor()
	print num_bus
	cur3.execute("SELECT * FROM info WHERE click > "+ str(num_bus) +" ORDER BY fecha DESC FETCH FIRST 10 ROWS ONLY ;")
	rows=cur3.fetchall()
	
	
	
	final = '<h2>NOTICIAS FILTRADAS por clics: </h2><table style="width:100%">'
	final = final + '<tr>' + '<th style="border: 1px solid blue; border-collapse: collapse;">' + 'TITULO' + '</th><th style="border: 1px solid blue; border-collapse: collapse;">' +'FECHA OBTENCION'+ '<th><th style="border: 1px solid blue; border-collapse: collapse;">' + 'HORA OBTENCION' + '<th><th style="border: 1px solid blue; border-collapse: collapse;">' + 'CLICKs' + '</th>'+ '<th style="border: 1px solid blue; border-collapse: collapse;">' + 'MENEOS' + '</th>' + '</tr>'
	for cosa in rows:
		final = final + '<tr>'
		#print '\n\t'
		#print cosa[0]
		dt = cosa[3] 		# El dia el mes y el anno
		hora = cosa[4]		# La hora que se ha realizado la insercion
		meneos = str(cosa[1])
		clic = str(cosa[2])
		print dt
		salida = str(dt)
		salida2 = str(hora)
			
		
		#print salida2
		final = final + '<th style="border: 1px solid blue; border-collapse: collapse;">' + cosa[0] + '</th><th style="border: 1px solid blue; border-collapse: collapse;">' +salida+ '<th><th style="border: 1px solid blue; border-collapse: collapse;">' +salida2+ '<th><th style="border: 1px solid blue; border-collapse: collapse;">' + clic + '</th>'+ '<th style="border: 1px solid blue; border-collapse: collapse;">' + meneos + '</th>'
		final = final + '</tr>'
		
	final = final + '</table>'
	return final
	
	
if __name__ == "__main__":
   app.run(host='0.0.0.0') 