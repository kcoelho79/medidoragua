my_url = 'https://datastudio.google.com/reporting/188wX_8wKVwiG8VBhAGheljpcqU18Dov1/page/bCkF'

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def read_data_csv():
    with open('data.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

def save_data_csv(data):
    fieldnames = ['data',  'dia', 'horas', 'tamanho' , 'medicao' , 'tamanho_cx' , 'distancia']
    data_hora = datetime.now().strftime('%d/%m/%y %H:%M')
    
    if os.path.isfile('data.csv'):
        print(" ARQUIVO JA EXISTENTE")
        with open('data.csv', mode='a', encoding='utf-8', newline='' ) as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, dialect='excel')
            #writer.writeheader()
            writer.writerow({'data': data_hora, 'dia': data[0], 'horas': data[1], 'tamanho': data[2], 'medicao': data[3], 'tamanho_cx': data[4], 'distancia': data[5]})

    else:
        print("cria arquivo")
        # create the file and write the header to first row 
        with open('data.csv', mode='w', encoding='utf-8', newline='' ) as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, dialect='excel')
            writer.writeheader()
            writer.writerow({
                'data': data_hora,
                'dia': data[0],
                'horas': data[1],
                'tamanho': data[2],
                'medicao': data[3],
                'tamanho_cx': data[4],
                'distancia': data[5]
            })


url = 'https://datastudio.google.com/reporting/188wX_8wKVwiG8VBhAGheljpcqU18Dov1/page/bCkF'
driver = webdriver.Chrome() # can be Firefox(), PhantomJS() and more
driver.get(url)

data_collected=[]
try:
    element = WebDriverWait(driver, 30).until(
    #  Aguarda carregar a  tabela com todos os medidores
       EC.presence_of_element_located((By.XPATH, '//*[@id="body"]/div/div/div[1]/div[2]/div/div[1]/div/div[1]/div/lego-report/lego-canvas-container/div/file-drop-zone/span/content-section/canvas-component[2]/div/div/div/div/div/lego-table/div/div[3]'))
    )
    pageSource = driver.page_source
    bsobj = BeautifulSoup(pageSource, features="html.parser")
    for i in bsobj.find("div", {"class": "word-wrap"}, text="2019.0071").next_siblings:
        data_collected.append(i.text)
    print("dados", data_collected)

    save_data_csv(data_collected)
    #read_data_csv()


except AssertionError as error:
    print(error)

finally:
    driver.quit()
