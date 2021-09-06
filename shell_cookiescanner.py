#!/usr/bin/env python3

# CookieScanner v.0.1
# ====================================================================================
# Scanner e classificador de cookies
# Autor: Christiano Medeiros <christiano.medeiros@modulo.com>
# ====================================================================================
# Instalação:
# sudo yum install chromium-chromedriver
# sudo yum install firefox
# sudo -H python3 -m pip install selenium
# ====================================================================================
# Exemplo de chamada: http://127.0.0.1:5000/api/v1/cookies/scan?URI=modulo.com
# ====================================================================================

import os
from flask import jsonify
import sys
import json
import time
import pickle
from datetime import datetime as dt
from selenium import webdriver 
from selenium.webdriver.firefox.options import Options
import logging
class bscrctl:
	CLEAR50   = '\033[50D'
	CLEAR100  = '\033[100D'
	CLEAR500  = '\033[500D'
	CLEARLINE = '\033[2K'
	FIRSTCOL  = '\033[1G'
	MOVEDN1   = '\033[1B'
	MOVEUP1   = '\033[1A'
	MOVER15   = '\033[15C'
	MOVEL15   = '\033[15D'
	SAVE	  = '\033[s'
	LOAD	  = '\033[u'

class bcolors:
	HEADER	= '\033[95m'
	OKBLUE	= '\033[94m'
	OKGREEN   = '\033[92m'
	WARNING   = '\033[93m'
	FAIL	  = '\033[91m'
	ENDC	  = '\033[0m'
	BOLD	  = '\033[1m'
	UNDERLINE = '\033[4m'


def msg(code, message):
	switcher = {
		'ROSA' : bcolors.HEADER,
		'AZUL' : bcolors.OKBLUE,
		'VERD' : bcolors.OKGREEN,
		'WARN' : bcolors.WARNING,
		'ERRO' : bcolors.FAIL,
		'NONE' : bcolors.ENDC,
		'BOLD' : bcolors.BOLD,
		'SUBL' : bcolors.UNDERLINE
	}
	print(f"{switcher.get(code,bcolors.ENDC)}{message}{bcolors.ENDC}")


def main():

	msg('VERD',"============================================================================================")
	msg('VERD'," CookieReporter | v.1.0 |                                                 ACKnology (c) 2021")
	msg('VERD'," Author: Christiano Medeiros <christiano.medeiros@acknology.com.br>                         ")
	msg('VERD',"--------------------------------------------------------------------------------------------")
	msg('VERD'," Scanner/Relatório de cookies em lote.                                                      ")
	msg('VERD',"============================================================================================")

	logging.basicConfig(filename='myapp.log', format='%(asctime)s|%(levelname)s|%(message)s', level=logging.INFO)


	# Chrome
	# =====================================================
	# from selenium.webdriver.chrome.options import Options
	# options.add_argument("--headless")
	# driver = webdriver.Chrome(options=options)

	options = Options()
	options.headless = True

	try:
		runTag = sys.argv[2]
		arqURI = sys.argv[1]
	except:
		print(f"Nenhum argumento informado.\nSintaxe: {sys.argv[0]} [arquivo_de_URIs] [tag]")
		exit(1)

	try:
		with open(arqURI) as file:
			lines = file.readlines()
			lines = [line.rstrip() for line in lines]
	except:
		pass
	finally:
		file.close()

	jsonPath = f"./json/{runTag}/"
	imgPath = f"./img/{runTag}/"
	#runTag = "xyz"

	try:
		os.mkdir(f"{jsonPath}")
	except Exception as e:
		print(f"Não foi possível criar o diretório de trabalho {jsonPath}. Erro: {e}")
		exit(1)

	try:
		os.mkdir(f"{imgPath}")
	except Exception as e:
		print(f"Não foi possível criar o diretório de trabalho {imgPath}. Erro: {e}")
		exit(1)

	print(">>> %s - Iniciando o WebDriver..."%dt.now())
	driver = webdriver.Firefox(options=options)

	try:
		#for URI in sys.argv[1].split(","):
		for URI in lines:

			strURI = URI.replace('/', '-').replace(':', '=')
			cookies_json = "%s.json"%strURI

			# Tratamento de excessão para URIs malformadas e HTTP/HTTPS
			if URI[:4].upper()=="HTTP":
				try:
					print(">>> %s - Acessando %s..."%(dt.now(),URI))
					driver.get("%s"%URI)
				except Exception as e:
					print("### Erro: %s"%str(e))
			else:
				try:
					print(">>> %s - Acessando https://%s..."%(dt.now(),URI))
					driver.get("https://%s"%URI)

				except Exception as e:
					print("### Erro: %s"%str(e))
					try:
						print(">>> %s - Acessando http://%s..."%dt.now())
						driver.get(f"http://%s"%URI)
					except Exception as e:
						print("### Erro: %s"%str(e))
			
			time.sleep(5) #Importante para dar tempo de carregar o máximo de conteúdo da URI

			try:
				imgFile = f"{strURI}.png"
				print(f">>> %s - Salvando o screenshot em {imgPath}{imgFile}..."%dt.now())
				driver.save_screenshot(f"{imgPath}{imgFile}")
			except Exception as e:
				print(">>> %s - Erro ao salvar o screenshot do site %s: %s"%(dt.now(),URI,e))

			try:
				print(">>> %s - Gravando %s..."%(dt.now(),cookies_json))
				cookies = driver.get_cookies()
			except Exception as e:
				print(">>> %s - Erro ao ler os cookies do domínio %s: %s"%(dt.now(),URI,e))

			with open(jsonPath+cookies_json, 'w+', newline='') as outputdata:
				json.dump(cookies, outputdata,indent=4, sort_keys=True)

	except IndexError:
		#print("Erro: Nenhum argumento informado. Por favor, especifique um domínio ou uma lista de domínions separada por vírgulas.\nEx.:\"URI1.com,URI2.com,URI3.com,...\"")
		pass

	print(">>> %s - Finalizando o WebDriver..."%dt.now())
	driver.quit()

if __name__ == '__main__':
	main()
