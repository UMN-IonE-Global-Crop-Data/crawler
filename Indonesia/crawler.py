from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

class Crawler:
    def __init__(self, input_dic):
        self.subsection = input_dic["Subsection"]
        self.indictor = input_dic["Indicator"]
        self.year_start = input_dic["Start Year"]
        self.year_end = input_dic["End Year"]
        self.crop = input_dic["Crop"]
        #self.state = input_dic["State"]
        #self.distict = input_dic["District"]
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

class NationalCrawler(Crawler):
    def crawling(self):
        wb = webdriver.Chrome(options=self.options)
        wb.implicitly_wait(10)
        wb.get("https://bdsp2.pertanian.go.id/bdsp/id/lokasi")
        #refresh
        wb.refresh()
        #select subsector "crop", "horticulture"
        wb.find_element(By.XPATH,f"//*[@id='subsektor']/option[text()='{self.subsection}']").click()

        #select commodity (crop)
        
        print(f"//*[@id='komoditas']/option[text()='{self.crop}']")
        time.sleep(2)
        wb.find_element(By.XPATH,f"//*[@id='komoditas']/option[text()='{self.crop}']").click()

        #select indicator "harvest area", "production", "productitvty"
        wb.find_element(By.XPATH,f"//*[@id='indikator']/option[text()='{self.indictor}']").click()

        #select  level "National"
        wb.find_element(By.XPATH,"//*[@id='level']/option[text()='Nasional']").click()

        #select unit "ton" "Ha" "Quiantal/Ha"
        wb.find_element(By.XPATH,"//*[@id='satuan']/option[2]").click()

        #start year and end year
        wb.find_element(By.XPATH,f"//*[@id='tahunAwal']/option[text()={self.year_start}]").click()
        wb.find_element(By.XPATH,f"//*[@id='tahunAkhir']/option[text()={self.year_end}]").click()
        
        #consult
        wb.find_element(By.XPATH,"//*[@id='search']").click()
        time.sleep(1)

        #download_excel
        wb.find_element(By.XPATH,"//*[@id='excel1']").click()
       
  
