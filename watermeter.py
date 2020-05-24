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
        self.dataset = []  # dataCollected
        self.filepath = ''
        self.dataframe = ''

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


    def get_page(self,url=None):  #fetchWaterLevel
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
                print('... created dataset ...')
                print("... printing dataset ...", self.dataset)
            else: 
                print("!!! erro dataset not created !!!")
            
            self.driver.quit()
            print("... closed webdriver ...")

            return self.dataset

        # return self.dataset -- see todo #4 

    def manipular_dados(self, dataset = None  ,namefilecsv= 'data.csv'):
        dataset = self.dataset
        dirpath = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(dirpath, namefilecsv)
        

class handle:
    def __init__(self, dataset):  #dataset = data collected
        print("... START HANDLE DATA ...")
        self.dataset = dataset
        self.dataframe = {
            'data': datetime.now().strftime('%d/%m/%y %H:%M'),
            'dia': dataset[0], 
            'horas': dataset[1], 
            'tamanho': dataset[2], 
            'medicao': dataset[3], 
            'tamanho_cx': dataset[4], 
            'distancia': dataset[5]
        }
        # create list get all keys=(columns dataframe) from dataframe
        self.fieldnames = [col for col in self.dataframe.keys()] 
                    

    def csv_file(self, filename):
        print("... Generate CSV Dataframe ...")
        dirpath = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(dirpath, filename)

        if os.path.isfile(filepath):
            print("... file < %s > already exist ..." %filename)
            self.__open_file(filename)
        else:
            self.__create_file(filename)

        self.filename = filename 
        return filename

    def __open_file(self, filename):
        print("... opening file < %s > " %filename)  
        with open(filename, mode='a', encoding='utf-8', newline='' ) as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames, dialect='excel')
            writer.writerow(self.dataframe)

    def __create_file(self, filename):
        print("... creating file < %s > " %filename)  
        with open(filename, mode='w', encoding='utf-8', newline='' ) as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames, dialect='excel')
            writer.writeheader()
            writer.writerow(self.dataframe)
     

    # # clean dataset, delimited is used para demiliter the char . or , from percentual  
    # def clean_dataset(self, csvfilepath=None , delimited = '.', day=1 ):
    #     csvfilepath = self.filepath
    #     print('... cleanning dataset ...')
    #     print('... created dataframe from dataset ...')
    #     dataframe = pd.read_csv(csvfilepath, index_col= False , parse_dates = ["data"])
    #     dataframe['medicao'] = pd.to_numeric(dataframe['medicao'].str.split(delimited).str.get(0))
    #     dataframe['horas'] = pd.to_datetime(dataframe['horas'], format='%H:%M').dt.time
    #     print('... selected period dataframe...')
    #     dateperiod = pd.datetime.now() - timedelta(days=day)
    #     df2 = dataframe[dataframe['data'] > dateperiod]
    #     print('... dataframe cleanned ... ')
    #     self.dataframe = df2
    #     return df2