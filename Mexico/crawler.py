from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
#import numpy as np



class Crawler:
    def __init__(self, input_dic):
        self.year = input_dic["Year"]
        self.crop = input_dic["Crop"]
        self.state = input_dic["State"]
       # self.distict = input_dic["District"]
        self.state_list = ["National", "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", 
                           "Coahuila", "Colima", "Chiapas", "Chihuahua", "Mexico City", "Durango", "Guanajuato",
                            "Guerrero", "Hidalgo", "Jalisco", "Mexico", "Michoacán", "Morelos", "Nayarit", "Nuevo Leon", 
                            "Oaxaca", "Puebla", "Queretaro", "Quintana Roo", "San Luis Potosi", "Sinaloa", "Sonora", 
                            "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatan", "Zacatecas"]

        download_path = os.path.join(os.getcwd(), 'downloads')
        self.options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": download_path,
                 "download.prompt_for_download": False,
                 "download.directory_upgrade": True,
                 "safebrowsing.enabled": True
                 }
        self.options.add_experimental_option('prefs', prefs)

    def crawling(self):
        pass

    # def arrange(self,df):
    #     new_header = df.iloc[0]
    #     print(f"new header: {new_header}" )  
    #     df = df.iloc[:-1, :]
    #     print(df)
    #     df.columns = new_header 
    #     df.reset_index(drop=True, inplace=True)
    #     print(df)
    #     #df = df.drop(df.tail(1).index)

    #     #select and rename the column
    #     selected_columns = df[['Entidad', 'Distrito','Sembrada', 'Cosechada', 'Producción','Valor Producción (miles de Pesos)']]
    #     selected_columns.columns = ['State', 'District','Sown Area (ha)', 'Harvested Area  (ha)', 'Production','Value of production']

    #     #insert year and crop name
    #     selected_columns.insert(2, 'year', self.year)
    #     selected_columns.insert(3, 'crop', self.crop)

    #     #cleaned dataframe
    #     selected_columns.to_excel('.\\arranged\\arranged.xlsx', index= False)
        
        
class StateCrawler(Crawler):
    # get all state level crop data
    def crawling(self):
        wb = webdriver.Chrome(options=self.options)
        wb.implicitly_wait(7)
        wb.get("https://nube.siap.gob.mx/cierreagricola")

        #years
        wb.find_element(By.XPATH,f"//*[@id='anioagric']/option[text()={self.year}]").click()
        
        #state
        wb.find_element(By.XPATH,f"//*[@id='entidad']/option[text()='Nacional']").click()

        #crops
        time.sleep(1)
        wb.find_element(By.XPATH, f"//*[@id='cultivo']/option[text()= '{self.crop}']").click()

        time.sleep(1)
        wb.find_element(By.XPATH, "//*[@id='divNoImprimir']/div[3]/div/div[2]/input").click()
        time.sleep(1)

        #download data
        #wb.find_element(By.XPATH,"//*[@id='divNoImprimir']/div[3]/div/div[5]/img").click()

        #download table(html)
        
        table = wb.find_element(By.XPATH,"//*[@id='Resultados-reporte']")
        table_html = table.get_attribute('outerHTML')

        #Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(table_html, 'lxml')

        # Find the table in the HTML
        table = soup.find('table')
        # Convert the table to a DataFrame
        df = pd.read_html(str(table))[0]

        print("raw:")
        print(df)
        df = df.iloc[:-1, 1:]
        print("sliced")
        print(df)
        df.columns =['Entity','Sown','Harvested', 'Damaged',
                      'Production', 'Yield(udm/ha)', 'PMR($/udm)', 'Production Value (thousands of Pesos)']
        df.insert(1, 'year', self.year)
        df.insert(2, 'crop', self.crop)
        print("final df:")
        print(df)

        return df


class DistrictCrawler(Crawler):
    # get all district level crop data within one state
    def crawling(self):
        wb = webdriver.Chrome()
        wb.implicitly_wait(7)
        wb.get("https://nube.siap.gob.mx/cierreagricola")
        time.sleep(1)
        #district
        wb.find_element(By.XPATH,"//*[@id='opcionDDRMpio3']").click()

        #years
        wb.find_element(By.XPATH,f"//*[@id='anioagric']/option[text()={self.year}]").click()

        #state
        time.sleep(1)
        wb.find_element(By.XPATH,f"//*[@id='entidad']/option[text()='{self.state}']").click()

        #district
        #wb.find_element(By.XPATH,f"//*[@id='distrito']/option[text()=' Todos ']").click()

        #crops
        try:
            time.sleep(1)
            wb.find_element(By.XPATH, f"//*[@id='cultivo']/option[text()= '{self.crop}']").click()
            
        except NoSuchElementException:
            # If the specific option is not found, return an empty DataFrame
            print("Specified crop option not found. Returning empty DataFrame.")
            columns = ['Entity', 'District', 'Sown', 'Harvested', 'Damaged',
                       'Production', 'Yield(udm/ha)', 'PMR($/udm)', 'Production Value (thousands of Pesos)']
            return pd.DataFrame(columns=columns)

        #consult
        time.sleep(1)
        wb.find_element(By.XPATH, "//*[@id='divNoImprimir']/div[3]/div/div[2]/input").click()
        time.sleep(1)
        
        #download table(html)'
        
        table = wb.find_element(By.XPATH,"//*[@id='Resultados-reporte']")
        table_html = table.get_attribute('outerHTML')

        #Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(table_html, 'lxml')

        #click excel
        #wb.find_element(By.XPATH,"//*[@id='divNoImprimir']/div[3]/div/div[5]/img").click()

        # Find the table in the HTML
        table = soup.find('table')
        # Convert the table to a DataFrame
        df = pd.read_html(str(table))[0]
        print("raw:")
        print(df)
        df = df.iloc[:-1, 1:]
        print("sliced")
        print(df)
        #df.columns = ['Entidad', 'Distrito', 'Cosechada','Sembrada','Siniestrada','Producción','Rendimiento', 'PMR','Valor Producción (miles de Pesos)']
        df.columns =['Entity', 'District', 'Sown','Harvested', 'Damaged',
                      'Production', 'Yield(udm/ha)', 'PMR($/udm)', 'Production Value (thousands of Pesos)']
        df.insert(2, 'year', self.year)
        df.insert(3, 'crop', self.crop)
        print("final df:")
        print(df)
       
        return df

    




