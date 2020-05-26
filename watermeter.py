from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os, csv
from datetime import datetime, timedelta, date
import pandas as pd
import plotly.express as px

class Watermeter:
    
    def __init__(self):
        self.url = 'https://datastudio.google.com/reporting/188wX_8wKVwiG8VBhAGheljpcqU18Dov1/page/bCkF'
        self.dataColected = []  # dataCollected
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
                self.dataColected.append(i.text)

        except AssertionError as error:
            print('!!! error !!!',error)

        finally:
            if bool(self.dataColected):  #check se the dataColected was created and not 
                print("... fetched data ... ")
                print('... created dataColected ...')
                print("... printing dataColected ...", self.dataColected)
            else: 
                print("!!! erro dataColected not created !!!")
            
            self.driver.quit()
            print("... closed webdriver ...")

            return self.dataColected

    def sanitize_data(self, dataColected ,delimited='.'):
        print('... combine field date + field hour ...')
        hr = datetime.strptime(dataColected[1], '%H:%M')
        dt = datetime(datetime.now().year,datetime.now().month, int(dataColected[0]))
        Combine_HourData = datetime(dt.year, dt.month, dt.day, hr.hour, hr.minute)
        dataColected[0]= Combine_HourData
        print("... formatting % ...")
        dataColected[3] = dataColected[3].split(delimited)[0]
        print('... data sanitized ...')
        self.dataSanitized = dataColected
        return dataColected
    
    def save_data(self):
        pass

    def save_graph(self):
        pass

class handle: #Datahandler
    def __init__(self, dataColected):  #dataColected = data collected
        print("... START HANDLE DATA ...")
        self.dataCollected = dataColected
        self.dataStructure = {
            'timestamp': datetime.now().strftime('%d/%m/%y %H:%M'),
            'data': dataColected[0], 
            'horas': dataColected[1], 
            'tamanho': dataColected[2], 
            'medicao': dataColected[3], 
            'tamanho_cx': dataColected[4], 
            'distancia': dataColected[5]
        }
        # create list get all keys=(columns dataStructure) from dataStructure
        self.fieldnames = [col for col in self.dataStructure.keys()] 
        self.dataframe = ''
                    
    # CSV or transform
    def csv_file(self, filename='data.csv'):
        print("... Generate CSV Dataframe ...")
        dirpath = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(dirpath, filename)

        if os.path.isfile(filepath):
            print("... file < %s > already exist ..." %filename)
            self.__open_file(filename)
        else:
            self.__create_file(filename)

        self.dataframe = pd.read_csv(filename, index_col= False , parse_dates = ["data"])

        return self.dataframe

    def __open_file(self, filename):
        print("... opening file < %s > " %filename)  
        with open(filename, mode='a', encoding='utf-8', newline='' ) as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames, dialect='excel')
            writer.writerow(self.dataStructure)

    def __create_file(self, filename):
        print("... creating file < %s > " %filename)  
        with open(filename, mode='w', encoding='utf-8', newline='' ) as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames, dialect='excel')
            writer.writeheader()
            writer.writerow(self.dataStructure)
    
    def period(self, day=1):
        dateperiod = pd.datetime.now() - timedelta(days=day)
        print('... period selected  from %s - %s...' %(dateperiod ,pd.datetime.now()))
        self.dataframe = self.dataframe[self.dataframe['data'] > dateperiod]
        print('... period data selected ... ')
    
    def create_graph(self): 
        fig = px.bar(self.dataframe, x="horas", y="medicao")
        fig.write_html("templates/plot.html")
        

