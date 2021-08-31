#!/usr/bin/env python3

import pathlib as pl
import sqlite3
import json
import os
import sys
import datetime
import xlsxwriter as xw
import glob
import re

from datetime import datetime as dt

from io import BytesIO
from urllib.request import urlopen

imageHexa = 'data:image/jpeg;base64,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'

url = 'https://media-exp1.licdn.com/dms/image/C4D0BAQHgz1UTAYCVsQ/'+\
		'company-logo_200_200/0/1520443609757?e=2159024400&v=beta&t='+\
		'1ULy5mQAVb2o0FYAY212WhDdNi2cpFskuLJdONs72YY'

imageData = BytesIO(urlopen(url).read())

filel=glob.glob("./json/*.json")

xfile = sys.argv[1]

wb = xw.Workbook("./xlsx/{}.xlsx".format(xfile))

# Formato do cabeçalho
headerFormat = wb.add_format()
headerFormat.set_pattern(1) 
headerFormat.set_bg_color('#0071BB')
headerFormat.set_font_color('#FFFFFF')
headerFormat.set_bold(True)
headerFormat.set_align('center')
headerFormat.set_align('vcenter')
headerFormat.set_border(1)
headerFormat.set_font_size(14)

# Formato do conteúdo
contentFormat = wb.add_format()
contentFormat.set_pattern(0) 
contentFormat.set_bg_color('#FFFFFF')
contentFormat.set_font_color('#000000')
contentFormat.set_bold(False)
contentFormat.set_align('center')
contentFormat.set_align('vcenter')
contentFormat.set_text_wrap(True)
contentFormat.set_border(1)
contentFormat.set_font_size(12)

# Formato avulso
dummyFormat = wb.add_format()
dummyFormat.set_pattern(1) 
dummyFormat.set_bg_color('#FFFFFF')
dummyFormat.set_bold(False)
dummyFormat.set_align('left')
dummyFormat.set_align('vcenter')
dummyFormat.set_font_color('#333333')
dummyFormat.set_font_size(20)



coringas = []

try:
	con = sqlite3.connect('./db/cookies_db.db')
	cur = con.cursor()

	query = """ 
				select
						nome
				from
						all_cookies
				where
						coringa = 1
				order by
						nome
			"""
	ds = cur.execute(query)

	for item in ds:

		coringas.append(item[0])

	coringas.sort(key=len, reverse=True)

except Exception as e:
	print(">>> Catched: {0}".format(str(e)))
	print(">>> %s - Erro ao conectar a base de cookies para efetuar a carga dos cookies variantes..."%(dt.now()))

finally:
	con.close()

def getCookieName(cookieStr):

	for cookie in coringas:
		if cookie in cookieStr:
			 return(cookie)
	return cookieStr


for jfile in filel:

	print(">> %s - Lendo o arquivo %s"%(dt.now(),jfile))

	dtCriacaoJSON = dt.fromtimestamp(os.stat(pl.Path(jfile)).st_ctime).strftime('%Y-%m-%d %H:%M:%S')

	f = open("%s"%jfile,)
	js = json.load(f)

	regexPattern = re.compile(".*/(.*)\.json", re.IGNORECASE)

	regexResult = regexPattern.search(jfile)
	
	workSheetName = regexResult.group(1)

	if len(workSheetName) > 31: workSheetName = workSheetName[0:28]+"..."

	print(">> %s - Criando a planilha %s"%(dt.now(),workSheetName)) 

	ws = wb.add_worksheet(workSheetName)

	ws.set_row(0, 80)
	ws.set_row(1, 20)

	ws.set_column('A:A', 50, dummyFormat)
	ws.set_column('A:C', 15, dummyFormat)
	ws.set_column('D:D', 15, dummyFormat)
	ws.set_column('E:E', 50, dummyFormat)
	ws.set_column('F:F', 50, dummyFormat)
	ws.set_column('G:G', 15, dummyFormat)
	ws.set_column('H:I', 15, dummyFormat)
	ws.set_column('J:J', 25, dummyFormat)
	ws.set_column('K:N', 10, dummyFormat)
	ws.set_column('O:P', 30, dummyFormat)
	ws.merge_range('D1:P1', f"CookieScan - Relatório extraído em {dtCriacaoJSON}", dummyFormat)

	# Insert an image with scaling.
	# ws.insert_image('A1', 'logo_modulo_decorado.png', {'x_scale': 1, 'y_scale': 1, 'x_offset': 5, 'y_offset': 5})
	ws.insert_image('A1', 'logo_modulo.png')
	# ws.insert_image('A1', url, {'image_data': imageData, 'x_scale': 0.5, 'y_scale': 0.5, 'x_offset': 15, 'y_offset': 10})
	# ws.insert_image('B23', url,'python.png', {'x_scale': 0.5, 'y_scale': 0.5})



	con = sqlite3.connect('./db/cookies_db.db')
	cur = con.cursor()

	hdr = (['Cookie', 'Categoria', 'Controlador', 'Plataforma', 'Descricao', 'Politica' , 'Retencao', 'Expiracao', 'Dominio', 'DscDominio', 'HttpOnly', 'Path', 'SameSite', 'Secure', 'Value', 'EU_AI'])

	xrow=1
	xcol=0

	for c in hdr:
	   ws.write(xrow,xcol,c,headerFormat)
	   xcol=xcol+1

	xrow=2

	for ck in js:
		xcol = 0
		query = "select EU_IA, plataforma, categoria, dominio, retencao, controlador, politica, descricao from all_cookies where nome like \'{}%\' order by nome limit 1".format(getCookieName(ck['name']))
		#print(query)
		#pass
		ds = cur.execute(query)

		xds = list()

		# try:
		# 	#xds = ([ck['domain'], ck['expiry'], ck['httpOnly'], ck['path'], ck['sameSite'], ck['secure'], ck['value']])
		# 	xds = ([ck['name'],ck['domain'], datetime.datetime.fromtimestamp(int(ck['expiry'])).strftime('%Y-%m-%d %H:%M:%S'), ck['httpOnly'], ck['path'], ck['sameSite'], ck['secure'], ck['value']])
		# except:
		# 	xds = ([ck['name'],ck['domain'], '-1', ck['httpOnly'], ck['path'], ck['sameSite'], ck['secure'], ck['value']])

		for r in ds:
			xds.append(ck['name'])
			xds.append(r[2]) #categria
			xds.append(r[5]) #controlador
			xds.append(r[1]) #plataforma
			xds.append(r[7]) #descricao
			xds.append(r[6]) #politica
			xds.append(r[4]) #retencao
			try:
				xds.append(dt.fromtimestamp(int(ck['expiry'])).strftime('%Y-%m-%d %H:%M:%S')) 
			except:
				xds.append('-1')
			xds.append(ck['domain'])
			xds.append(r[3]) #dominio
			xds.append(ck['httpOnly'])
			xds.append(ck['path'])
			xds.append(ck['sameSite'])
			xds.append(ck['secure'])
			xds.append(ck['value'])
			xds.append(r[0]) #EU_IA


		for c in xds:
			#print("xrow:%d, xcol:%d, xds:%s"%(xrow,xcol,xds))
			ws.write(xrow,xcol,xds[xcol],contentFormat)
			xcol = xcol + 1
		xrow = xrow + 1

print(">> %s - Gravando o arquivo ./xlsx/%s.xlsx"%(dt.now(),xfile))

# worksheet.insert_image('B12', 'python.png', {'x_offset': 15, 'y_offset': 10})

# Insert an image with scaling.
# ws.insert_image('A1', 'logo_modulo.png', {'x_scale': 1, 'y_scale': 1, 'x_offset': 5, 'y_offset': 5})
ws.insert_image('A1', 'logo_modulo.png')

# ws.insert_image('A1', url, {'image_data': imageData, 'x_scale': 0.5, 'y_scale': 0.5, 'x_offset': 15, 'y_offset': 10})
# ws.insert_image('B23', url,'python.png', {'x_scale': 0.5, 'y_scale': 0.5})

wb.close()
con.close()


#cell_format.set_font_color('#FF0000')
#cell_format = workbook.add_format({'bold': True, 'font_color': 'red'})








