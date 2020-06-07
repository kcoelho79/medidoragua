from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os, csv
from datetime import datetime, timedelta, date, time
import pandas as pd
from flask import Flask, render_template
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io
import base64

class Watermeter:
    
    def __init__(self):
        self.url = 'https://datastudio.google.com/reporting/188wX_8wKVwiG8VBhAGheljpcqU18Dov1/page/bCkF'
        self.dataColected = []  # dataCollected
        self.dataSanitised = ''
        self.delimited = ''

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
        if not url:
            self.url = 'https://datastudio.google.com/reporting/188wX_8wKVwiG8VBhAGheljpcqU18Dov1/page/bCkF'
        print('... getting page from %s ...' %self.url)
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        print('... got page ...')
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

  
    def save_data(self, filename ):
       
        print("... START SAVE FILE ...")
        self.dataStructure = {
            'timestamp': datetime.now().strftime('%d/%m/%y %H:%M'),
            'data': self.__format_date(self.dataColected[0]),
            'horas': self.__format_hour(self.dataColected[1]), 
            'tamanho': self.dataColected[2], 
            'medicao': self.__format_percentual(self.dataColected[3]), 
            'tamanho_cx': self.dataColected[4], 
            'distancia': self.dataColected[5]
        }
        # create filedname list get all keys=(columns) from dataStructure
        self.fieldnames = [col for col in self.dataStructure.keys()] 
        print(">>> Field %s " %(self.fieldnames))
        self.fileCSV = ''

        dirpath = os.path.abspath(os.path.dirname(__file__))
        filepath = os.path.join(dirpath, filename)

        if os.path.isfile(filepath):
            print("... file < %s > already exist ..." %filename)
            self.__open_file(filename)
        else:
            self.__create_file(filename)

        #transform data Sanitized to FileCSV
        self.fileCSV = pd.read_csv(filename, index_col= False , parse_dates = ["data"])


        return self.fileCSV

    def __format_date(self, d):
        return date.today().replace(day=int(d)).strftime('%d/%m')

    def  __format_hour(self, t):
        h , m =  t.split(':')
        return time(hour=int(h),minute=int(m)).strftime('%H:%M')

    def __format_percentual(self, v, delimited='.'):
        if bool(self.delimited):
            delimited = self.delimited
        return int(v.split(delimited)[0])


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

    def save_graph(self, filename, day=10):
        
        #df = pd.read_csv(filename, parse_dates = ["data"] )
        df = pd.read_csv(filename, usecols=['horas','medicao'])

        #dateperiod = pd.datetime.now() - timedelta(days=day)
        #df[df['data'] >  dateperiod]

        print(df['horas'])
        print(df.dtypes)


        # df.set_index('horas',inplace=True)


        #fig, ax = plt.subplots(figsize=(15,7))
        df.plot(x='horas',y='medicao', grid=True)
        # formatar label x para visualizar hora em hora 
        #ax.xaxis.set_major_locator(mdates.HourLocator(byhour=range(1), interval=1))
       # ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        img = io.BytesIO()
       # ax.figure.savefig(img, format='png')   
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        return plot_url

    
    # def period(self, day=1):
    #     # dateperiod = pd.datetime.now() - timedelta(days=day)
    #     # print('... period selected  from %s - %s...' %(dateperiod ,pd.datetime.now()))
    #     # self.dataframe = self.dataframe[self.dataframe['data'] > dateperiod]
    #     # print('... period data selected ... ')
    
    def create_graph(self):
        pass

