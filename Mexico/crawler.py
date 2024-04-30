from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Crawler:
    def __init__(self, input_dic):
        self.year = input_dic["Year"]
        self.crop = input_dic["Crop"]
        self.region = input_dic["State"]

    def crawling(self):
        wb = webdriver.Chrome()
        wb.implicitly_wait(10)
        wb.get("https://nube.siap.gob.mx/cierreagricola")

        #federal entities
        wb.find_element(By.XPATH,f"//*[@id='entidad']/option[text()='{self.region}']").click()

        #years
        wb.find_element(By.XPATH,f"//*[@id='anioagric']/option[text()={self.year}]").click()

        #crops
        wb.find_element(By.XPATH, f"//*[@id='cultivo']/option[text()= '{self.crop}']").click()

        time.sleep(2)
        wb.find_element(By.XPATH, "//*[@id='divNoImprimir']/div[3]/div/div[2]/input").click()

        #download data
        wb.find_element(By.XPATH,"//*[@id='divNoImprimir']/div[3]/div/div[5]/img").click()



