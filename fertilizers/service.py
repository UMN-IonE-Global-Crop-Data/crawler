from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
import os
import time
import shutil
import pandas as pd


import config

table = config.table



def crawl(driver, Year, State=None, District=None, Fertilizer=None, Crop=None):
    driver.get("https://inputsurvey.dacnet.nic.in/districttables.aspx")

    driver.find_element(By.XPATH, f'''//select[@ onchange="return ONChangeddlYear();"]//option[text()="{Year}"]''').click()

    states = []
    districts = []

    if State is None:
        select_element = driver.find_element(By.XPATH, f'''//select[@ onchange="return ONChangeddlState();"]''')
        states = [option.text for option in select_element.find_elements(By.XPATH, './/option')]
        print(states)
        # select all first 
        get_datapoint(Year, "all", "all", Fertilizer, Crop, driver)
        for State in states:
            get_datapoint(Year, State, District, Fertilizer, Crop, driver)
        return
    else:
        get_datapoint(Year, State, District, Fertilizer, Crop, driver)


    if District is None:
        select_element = driver.find_element(By.XPATH, f'''//select[@ onchange="return OnChangeddlDistrict();"]''')
        districts = [option.text for option in select_element.find_elements(By.XPATH, './/option')]
        print(districts)
        get_datapoint(Year, State, "all", "all", Crop, driver)
        for District in districts:
            get_datapoint(Year, State, District, Fertilizer, Crop, driver)
        return
    else:
        get_datapoint(Year, State, District, Fertilizer, Crop, driver)

def get_datapoint(year, state, district, fertilizer, crop,  driver):
    if state == "all":
        driver.get("https://inputsurvey.dacnet.nic.in/nationaltables.aspx")
    elif district == "all":
        driver.get("https://inputsurvey.dacnet.nic.in/statetables.aspx")
    
    select_year = driver.find_element(By.XPATH, f'''//select[contains(@onchange, "Year")]/option[text()="{year}"]''').click()

    # select state
    if state != "all":
        driver.find_element(By.XPATH, f'''//select[contains(@onchange, "State")]/option[text()="{state}"]''').click()

    if district != "all":
        driver.find_element(By.XPATH, f'''//select[contains(@onchange, "District")]/option[text()="{district}"]''').click()

    select_table = driver.find_element(By.XPATH, '//select[contains(@onchange, "Table")]/option[@value="7"]').click()
    
    time.sleep(0.5)

    if crop == None:
        select_element = driver.find_element(By.XPATH, f'''//select[@ onchange="return ONChangeddlCrop1();"]''')
        crops = [option.text for option in select_element.find_elements(By.XPATH, './/option')]
        for crop in crops:
            get_datapoint(year, state, district, fertilizer, crop,  driver)
        return
    else:  
        select_crop = driver.find_element(By.XPATH, f'''//select[contains(@onchange, "Crop")]/option[text()="{crop}"]''').click()

    if fertilizer == None:
        select_element = driver.find_element(By.XPATH, f'''//select[@ onchange="return ONChangeddlFetilizer();"]''')
        fertilizers = [option.text for option in select_element.find_elements(By.XPATH, './/option')]
        for fertilizer in fertilizers:
            get_datapoint(year, state, district, fertilizer, crop,  driver)
        return
    else:
        select_fertilizer = driver.find_element(By.XPATH, f'''//select[contains(@onchange, "Fetilizer")]/option[text()="{fertilizer}"]''').click()

    submit = driver.find_element(By.XPATH, f'''//input[@type="submit"]''').click()
    time.sleep(1)

    N = driver.find_element(By.XPATH, "/html/body/form/table/tbody/tr[2]/td/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td[8]/div/div/div/span[2]").text
    P = driver.find_element(By.XPATH, "/html/body/form/table/tbody/tr[2]/td/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td[9]/div/div/div/span[2]").text
    K = driver.find_element(By.XPATH, "/html/body/form/table/tbody/tr[2]/td/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[4]/td[11]/div/div/div/span[2]").text

    name = "_".join([year, state, district, crop, fertilizer])
    name += f"N{N}%P{P}%K{K}%".replace('\xa0', "")

    download_data(driver, name)

def download_data(driver, name):
        driver.execute_script("$find('ReportViewer1').exportReport('CSV');")
        time.sleep(0.5)
        if rename_and_move_csv_files('.', 'table', name):
            return 
        
        raise Exception("fail to download")

def rename_and_move_csv_files(directory, keyword, new_name):
    # 创建csv文件夹
    tim = time.time()
    while time.time()-tim < 5:
        csv_directory = os.path.join(directory, 'csv')
        os.makedirs(csv_directory, exist_ok=True)

        # 遍历当前目录下的文件
        for filename in os.listdir(directory):
            if filename.endswith('.csv') and keyword in filename:
                # 构造新的文件名
                new_filename = new_name.replace('/', '&') + '.csv'
                new_filename = new_filename.replace('"', '')

                # 源文件路径
                source_path = os.path.join(directory, filename)
                # 目标文件路径
                destination_path = os.path.join(csv_directory, new_filename)

                if os.path.exists(destination_path):
                    print(f"file {new_filename} already exists")
                
                # 重命名文件并移动到csv文件夹
                time.sleep(0.5)
                shutil.move(source_path, destination_path)
                return True
    else:
        return False

def save_txt(filename, data):
    with open(filename, 'a', newline='') as file:
        file.write(data + "\n")
