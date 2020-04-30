my_url = 'https://datastudio.google.com/reporting/188wX_8wKVwiG8VBhAGheljpcqU18Dov1/page/bCkF'

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
import time
from bs4 import BeautifulSoup
import csv
from datetime import datetime

class MedidorAgua():
    def __init__(self):
        self.url = 'https://datastudio.google.com/reporting/188wX_8wKVwiG8VBhAGheljpcqU18Dov1/page/bCkF'
        self.data_collected = []

    # Open HeadLess chromedriver
    def start_driver(self):
        print("... starting driver ...")
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        self.driver = webdriver.Chrome()

    def close_driver(self):
        print(' closing driver ...')
        self.display.stop()
        self.driver.quit()
        print('closed!...')

    def get_page(self, url):
        print('getting page...')
        self.driver.get(self.url)
        try:
            element = WebDriverWait(self.driver, 30).until(
            #  Aguarda carregar a  tabela com todos os medidores
            EC.presence_of_element_located((By.XPATH, '//*[@id="body"]/div/div/div[1]/div[2]/div/div[1]/div/div[1]/div/lego-report/lego-canvas-container/div/file-drop-zone/span/content-section/canvas-component[2]/div/div/div/div/div/lego-table/div/div[3]'))
            )
            pageSource = self.driver.page_source
            bsobj = BeautifulSoup(pageSource, features="html.parser")
            for i in bsobj.find("div", {"class": "word-wrap"}, text="2019.0071").next_siblings:
                self.data_collected.append(i.text)

        except AssertionError as error:
            print(error)

        finally:
            print("printing data...", self.data_collected)


    def save_data_csv(self, data):
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


    def parse(self):
        self.start_driver()
        self.get_page()
        self.close_driver()
        self.save_data_csv(self.data_collected)

# run selenium

Leitor = MedidorAgua()
medidas = Leitor.parse()
