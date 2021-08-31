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
# Exemplo de chamada: http://127.0.0.1:5000/api/v1/cookies/scan?dominio=modulo.com
# ====================================================================================

from flask import jsonify

import sys
import json
import time
import pickle

from datetime import datetime as dt

from selenium import webdriver 

from selenium.webdriver.firefox.options import Options

# Chrome
# =====================================================
# from selenium.webdriver.chrome.options import Options
# options.add_argument("--headless")
# driver = webdriver.Chrome(options=options)

options = Options()
options.headless = True

print(">>> %s - Iniciando o WebDriver..."%dt.now())
driver = webdriver.Firefox(options=options)

jsonPath = "./json/"
imgPath = "./img/"
runTag = "xyz"

try:
	for dominio in sys.argv[1].split(","):

		cookies_json = "%s.json"%dominio

		# Tratamento de excessão para requests HTTP/HTTPS
		try:
			print(">>> %s - Acessando https://%s..."%(dt.now(),dominio))
			driver.get("https://%s"%dominio)

		except Exception as e:
			print("### Erro: %s"%str(e))
			try:
				print(">>> %s - Acessando http://%s..."%dt.now())
				driver.get("http://%s"%dominio)
			except Exception as e:
				print("### Erro: %s"%str(e))

		try:
			os.sleep(5)
			imgFile = f"{runTag}_{dominio}.png"
			print(f">>> %s - Salvando o screenshot em {imgPath}{imgFile}..."%dt.now())
			driver.save_screenshot(f"{imgPath}{imgFile}.png")
		except Exception as e:
			print(">>> %s - Erro ao salvar o screenshot do site %s: %s"%(dt.now(),dominio,e))


		try:
			print(">>> %s - Gravando %s..."%(dt.now(),cookies_json))
			cookies = driver.get_cookies()
		except Exception as e:
			print(">>> %s - Erro ao ler os cookies do domínio %s: %s"%(dt.now(),dominio,e))

		with open(jsonPath+cookies_json, 'w+', newline='') as outputdata:
		    json.dump(cookies, outputdata,indent=4, sort_keys=True)

except IndexError:
	print("Erro: Nenhum argumento informado. Por favor, especifique um domínio ou uma lista de domínions separada por vírgulas.\nEx.:\"dominio1.com,dominio2.com,dominio3.com,...\"")

print(">>> %s - Finalizando o WebDriver..."%dt.now())
driver.quit()
