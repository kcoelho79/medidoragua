from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os, csv
from datetime import datetime, timedelta
import pandas as pd



class Watermeter:
    
    def __init__(self):
        self.url = 'https://datastudio.google.com/reporting/188wX_8wKVwiG8VBhAGheljpcqU18Dov1/page/bCkF'
        self.dataset = []
        self.filepath = ''

        # Open HeadLess chromedriver
    def start_display(self):
        print("... starting display ...")
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        print("... started ... ")
        
    def close_display(self):
        print('... closing display ...')
        self.display.stop()
        print('... closed!...')


    def get_page(self,url=None):
        if url:
            self.url = url
        print('... getting page from %s ...' %self.url)
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        print('... got page ...')
        print('... fechting data by Selenium ...')
        try:
            element = WebDriverWait(self.driver, 30).until(
            #  Aguarda carregar a  tabela com todos os medidores
            EC.presence_of_element_located((By.XPATH, '//*[@id="body"]/div/div/div[1]/div[2]/div/div[1]/div/div[1]/div/lego-report/lego-canvas-container/div/file-drop-zone/span/content-section/canvas-component[2]/div/div/div/div/div/lego-table/div/div[3]'))
            )
            pageSource = self.driver.page_source
            bsobj = BeautifulSoup(pageSource, features="html.parser")
            for i in bsobj.find("div", {"class": "word-wrap"}, text="2019.0071").next_siblings:
                self.dataset.append(i.text)

        except AssertionError as error:
            print('!!! error !!!',error)

        finally:
            if bool(self.dataset):  #check se the dataset was created and not 
                print("... fetched data ... ")
            else: 
                print("!!! erro dataset not created !!!")
            print('... created dataset ...')
            print("... printing dataset ...", self.dataset)
            self.driver.quit()
            print("... closed webdriver ...")

            return self.dataset

        # return self.dataset -- see todo #4 

    def dict_tocsv(self,dataset=dict ,namefilecsv= 'data.csv'): 
        # if namefilecsv:
        #     self.namefilecsv = namefilecsv

        dirpath = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(dirpath, namefilecsv)

        print('... converting dict to %s...' %namefilecsv)
        fieldnames =[   
                'data',
                'dia',
                'horas',
                'tamanho', 
                'medicao', 
                'tamanho_cx', 
                'distancia'
                ]
        
        if os.path.isfile(filepath):
            print("... file %s already exist ..." %namefilecsv )
            with open(namefilecsv, mode='a', encoding='utf-8', newline='' ) as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, dialect='excel')
                writer.writerow({
                    'data': self.__append_timestamp(),
                    'dia': dataset[0], 
                    'horas': dataset[1], 
                    'tamanho': dataset[2], 
                    'medicao': dataset[3], 
                    'tamanho_cx': dataset[4], 
                    'distancia': dataset[5]
                    })

        else:
            print("... create file %s ..." %namefilecsv)
            # create the file and write the header to first row 
            with open(namefilecsv, mode='w', encoding='utf-8', newline='' ) as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, dialect='excel')
                writer.writeheader()
                writer.writerow({
                    'data': self.__append_timestamp(),
                    'dia': dataset[0], 
                    'dia': dataset[0],
                    'horas': dataset[1],
                    'tamanho': dataset[2],
                    'medicao': dataset[3],
                    'tamanho_cx': dataset[4],
                    'distancia': dataset[5]
                })

        self.filepath = filepath     
        return filepath

    def __append_timestamp(self):
        print('... appending timestamp ...')
        return datetime.now().strftime('%d/%m/%y %H:%M')

    # clean dataset, delimited is used para demiliter the chah . or , from percentual  
    def clean_dataset(self, csvfilepath , delimited = '.', day=1 ):
        print('... cleanning dataset ...')
        print('... created dataframe from dataset ...')
        dataframe = pd.read_csv(csvfilepath, index_col= False , parse_dates = ["data"])
        dataframe['medicao'] = pd.to_numeric(dataframe['medicao'].str.split(delimited).str.get(0))
        dataframe['horas'] = pd.to_datetime(dataframe['horas'], format='%H:%M').dt.time
        print('... selected period dataframe...')
        dateperiod = pd.datetime.now() - timedelta(days=day)
        df2 = dataframe[dataframe['data'] > dateperiod]
        print('... dataframe cleanned ... ')
        return df2