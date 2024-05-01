from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
#import numpy as np



class Crawler:
    def __init__(self, input_dic):
        self.year = input_dic["Year"]
        self.crop = input_dic["Crop"]
        self.state = input_dic["State"]
        self.distict = input_dic["District"]
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

class StateCrawler(Crawler):
    # get all state level crop data
    def crawling(self):
        wb = webdriver.Chrome(options=self.options)
        wb.implicitly_wait(10)
        wb.get("https://nube.siap.gob.mx/cierreagricola")

        #years
        wb.find_element(By.XPATH,f"//*[@id='anioagric']/option[text()={self.year}]").click()
        
        #state
        wb.find_element(By.XPATH,f"//*[@id='entidad']/option[text()='Nacional']").click()

        #crops
        wb.find_element(By.XPATH, f"//*[@id='cultivo']/option[text()= '{self.crop}']").click()

        time.sleep(2)
        wb.find_element(By.XPATH, "//*[@id='divNoImprimir']/div[3]/div/div[2]/input").click()

        #download data
        wb.find_element(By.XPATH,"//*[@id='divNoImprimir']/div[3]/div/div[5]/img").click()


class DistrictCrawler(Crawler):
    # get all district level crop data within one state
    def crawling(self):
        wb = webdriver.Chrome()
        wb.implicitly_wait(10)
        wb.get("https://nube.siap.gob.mx/cierreagricola")
        time.sleep(1)
        #
        wb.find_element(By.XPATH,"//*[@id='opcionDDRMpio3']").click()

        #years
        wb.find_element(By.XPATH,f"//*[@id='anioagric']/option[text()={self.year}]").click()

        #state
        wb.find_element(By.XPATH,f"//*[@id='entidad']/option[text()='{self.state}']").click()

        #district

        wb.find_element(By.XPATH,f"//*[@id='distrito']/option[text()=' Todos ']").click()

        #crops
        wb.find_element(By.XPATH, f"//*[@id='cultivo']/option[text()= '{self.crop}']").click()

        time.sleep(1)
        wb.find_element(By.XPATH, "//*[@id='divNoImprimir']/div[3]/div/div[2]/input").click()
        

        #download data
        wb.find_element(By.XPATH,"//*[@id='divNoImprimir']/div[3]/div/div[5]/img").click()
        time.sleep(1)




