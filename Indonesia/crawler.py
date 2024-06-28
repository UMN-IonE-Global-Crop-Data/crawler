from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoAlertPresentException
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import winsound
class Crawler:
    def __init__(self, input_dic):
        self.subsection = input_dic["Subsection"]
        self.indictor = input_dic["Indicator"]
        self.year_start = input_dic["Start Year"] #1970
        self.year_end = input_dic["End Year"] #2024
        self.crop = input_dic["Crop"]
        self.state = input_dic["Province"]
        self.level = input_dic["Level"]
        self.max_retries = 4

        #self.distict = input_dic["District"]
        download_path = os.path.join(os.getcwd(), 'downloads')
        self.options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": download_path,
                 "download.prompt_for_download": False,
                 "download.directory_upgrade": True,
                 "safebrowsing.enabled": True
                 }
        self.options.add_experimental_option('prefs', prefs)

    def init_webdriver(self):
        """Initialize a new WebDriver session."""
        wb = webdriver.Chrome(options=self.options)
        wb.implicitly_wait(50)
        wb.get("https://bdsp2.pertanian.go.id/bdsp/id/lokasi")
        return wb
    

    def crawling(self):
        pass

class StateCrawler(Crawler):
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

        #select  level "National" or "Province"
        wb.find_element(By.XPATH,f"//*[@id='level']/option[text()='{self.level}']").click()
    

        #select unit "ton" "Ha" "Quiantal/Ha"
        wb.find_element(By.XPATH,f"//*[@id='satuan']/option[{self.index}]").click()

        #start year and end year
        wb.find_element(By.XPATH,f"//*[@id='tahunAwal']/option[text()={self.year_start}]").click()
        wb.find_element(By.XPATH,f"//*[@id='tahunAkhir']/option[text()={self.year_end}]").click()
        
        #consult
        wb.find_element(By.XPATH,"//*[@id='search']").click()
        time.sleep(5)

        #download_excel
        wb.find_element(By.XPATH,"//*[@id='excel1']").click()

class DistrictCrawler(Crawler):
     def check_and_handle_alert(self, wb):
        """Check for and handle alerts. Return True if an alert was handled, False otherwise."""
        try:
            alert = wb.switch_to.alert
            alert_text = alert.text
            if "status:" in alert_text:
                print(f"Specific alert handled with text: {alert_text}")
                alert.accept()  # Dismiss the alert
                return True  # Indicating that the specific alert was handled
            return False  # Alert was present but not the specific one we're looking for
        except NoAlertPresentException:
            return False  # No alert to handle
        
     def crawling(self):
        wb = self.init_webdriver()
        
        retries = 0
        #refresh the page if any elements aren't found, if the page are refreshed more than 3 times, raise an error
        while retries < self.max_retries:
            try:
                if self.check_and_handle_alert(wb):
                    print("This error message come from 1st page")
                    print("Alert handled, restarting WebDriver.")
                    wb.quit()
                    wb = self.init_webdriver()
                    time.sleep(2)  # Wait after restarting the WebDriver
                    continue
                if retries == 0:
                    wb.refresh()
                    retries += 1
                    time.sleep(2)  # Wait for the page to reload

                #select subsector "crop", "horticulture"
                wb.find_element(By.XPATH,f"//*[@id='subsektor']/option[text()='{self.subsection}']").click()

                #select commodity (crop)
                wb.find_element(By.XPATH,f"//*[@id='komoditas']/option[text()='{self.crop}']").click()

                #select indicator "harvest area", "production", "productitvty"
                wb.find_element(By.XPATH,f"//*[@id='indikator']/option[text()='{self.indictor}']").click()

                #select  level "National" or "Province"
                wb.find_element(By.XPATH,f"//*[@id='level']/option[text()='{self.level}']").click()

                #select Province
                wb.find_element(By.XPATH,f"//*[@id='prov']/option[text()='{self.state}']").click()
            
                #select unit "ton" "Ha" "Quiantal/Ha"
                wb.find_element(By.XPATH,"//*[@id='satuan']/option[2]").click()

                #start year and end year
                wb.find_element(By.XPATH,f"//*[@id='tahunAwal']/option[text()={self.year_start}]").click()
                wb.find_element(By.XPATH,f"//*[@id='tahunAkhir']/option[text()={self.year_end}]").click()
                

                break  # If no exceptions, break the loop
            except Exception as e:
                print(f"Attempt {retries + 1} failed: {e}")
                retries += 1
                if retries < self.max_retries:
                    wb.refresh()
                    time.sleep(2)  # Wait for the page to reload
                else:
                    winsound.Beep(1000,1800)
                    raise RuntimeError("Max retries reached. Element not found or page load failed.")

        
        #download table(html)
        # Click the search element
        search_button = WebDriverWait(wb, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='search']"))
        )
        search_button.click()

        if self.check_and_handle_alert(wb):
                    print("This error message come from 2nd page")
                    print("Alert handled, restarting WebDriver.")
                    wb.quit()
                    wb = self.init_webdriver()
                    
                    
        table = WebDriverWait(wb, 50).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='example']"))
        )

        table = wb.find_element(By.XPATH,"//*[@id='example']")
        table_html = table.get_attribute('outerHTML')

        #Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(table_html, 'lxml')

        # Find the table in the HTML
        table = soup.find('table')
        # Convert the table to a DataFrame
        df = pd.read_html(str(table))[0]

        return(df)