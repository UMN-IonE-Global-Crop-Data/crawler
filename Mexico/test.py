from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pandas as pd
from bs4 import BeautifulSoup
#import numpy as np


# URL of the page
wb = webdriver.Chrome()
wb.implicitly_wait(10)
wb.get("https://nube.siap.gob.mx/cierreagricola")

#years
wb.find_element(By.XPATH,"//*[@id='anioagric']/option[2]").click()

        #crops
wb.find_element(By.XPATH, "//*[@id='cultivo']/option[2]").click()

time.sleep(2)
wb.find_element(By.XPATH, "//*[@id='divNoImprimir']/div[3]/div/div[2]/input").click()
time.sleep(8)
# Assuming you want the first table

table = wb.find_element(By.XPATH,"//*[@id='Resultados-reporte']")
table_html = table.get_attribute('outerHTML')
print(table_html)

#Use BeautifulSoup to parse the HTML content
soup = BeautifulSoup(table_html, 'lxml')  # You can also use 'html.parser' if lxml is not installed

# Find the table in the HTML
table = soup.find('table')

# Convert the table to a DataFrame
df = pd.read_html(str(table))[0]

# Save the DataFrame to an Excel file
df.to_excel('output.xlsx')


