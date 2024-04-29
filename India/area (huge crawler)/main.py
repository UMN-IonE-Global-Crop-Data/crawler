import time
from retry import retry

import numpy as np
import pandas as pd
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
import concurrent.futures
from lxml import etree
import shutil
import csv
import os

chrome_options = ChromeOptions()
# 禁用CSS文件加载
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")
# 获取当前程序运行目录
downloads_path = os.getcwd()

# 创建下载目录的完整路径
# downloads_path = os.path.join(current_directory, "csv")

# 创建 ChromeOptions 对象并设置下载目录
# chrome_options.add_argument(f"--force-fieldtrials=SiteIsolationExtensions/Control")  # 解决 Chrome 93 以上版本的下载目录设置问题
# chrome_options.add_argument(f"--download-directory={downloads_path}")
prefs = {
    'download.default_directory': downloads_path,  # 设置默认下载路径
}
chrome_options.add_experimental_option("prefs", prefs)
# tehsi = "CAMPBELL BAY"
tables = "CROPPING PATTERN"

def rename_and_move_csv_files(directory, keyword, new_name):
    tim = time.time()
    while time.time()-tim < 5:
        # 创建csv文件夹
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



                # 重命名文件并移动到csv文件夹
                shutil.move(source_path, destination_path)
                # print(f"已将文件'{filename}'重命名为'{new_filename}'并移动到csv文件夹。")
                return True
    else:
        return False

def get_bg(driver, name):
    tim = time.time()
    while time.time()-tim < 60:
        try:
            driver.find_element(By.XPATH, '//div[contains(text(), "TABLE")] | //span[contains(text(), "TABLE")]')
            driver.execute_script("$find('ReportViewer1').exportReport('CSV');")
            # keeps calling rename_and_move_csv_files until it returns True
            # if it is false, sleep for 1 minute and call it again
            if rename_and_move_csv_files('.', 'splay', name):
                return
        except JavascriptException:
            time.sleep(3)
            get_bg(driver, name)
        except NoSuchElementException:
            try:
                driver.find_element(By.XPATH, "//div[text()='No Record Found']")
                save_txt("Missing Data.txt", name)
                return
            except NoSuchElementException:
                save_txt("err.txt", name)
                time.sleep(0.5)
        except TimeoutException:
            save_txt("err.txt", name)
            return
        except NoSuchWindowException:
            year = name.split("_")[0]
            state = name.split("_")[1]
            district = name.split("_")[2]
            tehsil = name.split("_")[3]
            crop = name.split("_")[4]
            get_tehsil(year, state, district, tehsil, crop, None)
    else:
        save_txt("err.txt", name)
        return
    # try:
    #     ht = driver.find_element(By.XPATH, '//tr[@ valign="top"]/td/div/../../..').get_attribute('innerHTML')
    # except NoSuchElementException:
    #     return "err"
    # x = etree.HTML(ht)
    # trs = x.xpath("//tr[position() > 5 and position() < last()]")
    # tb = []
    # for tr in trs:
    #     tb.append(tr.xpath("td/div/text()"))
    # tb.pop(1)
    # return tb

@retry(exceptions=TimeoutException or UnexpectedAlertPresentException,tries=3, delay=1)
def get_crop(year, state, district, tehsil, crop, driver):
    wc = False
    name = "_".join([year, state, district, tehsil.replace('\xa0', ""), crop])
    if district == "all":
        driver.get("https://agcensus.dacnet.nic.in/StateCharacteristic.aspx")
    elif tehsil == "all":
        driver.get("https://agcensus.dacnet.nic.in/DistCharacteristic.aspx")
    else:
        driver.get("https://agcensus.dacnet.nic.in/TalukCharacteristics.aspx")

    driver.find_element(By.XPATH, f'''//select[contains(@onchange, "Year")]/option[text()="{year}"]''').click()

    driver.find_element(By.XPATH, f'''//select[contains(@onchange, "State")]/option[text()="{state}"]''').click()

    if district != "all":
        driver.find_element(By.XPATH, f'''//select[contains(@onchange, "District")]/option[text()="{district}"]''').click()

    if tehsil != "all":
        driver.find_element(By.XPATH, f'''//select[contains(@onchange, "Tehsil")]/option[text()='{tehsil}']''').click()

    driver.find_element(By.XPATH, f'''//select[contains(@onchange, "SocialGroup")]/option[@value="4"]''').click()

    driver.find_element(By.XPATH, f'''//select[contains(@onchange, "Tables")]/option[text()="{tables}"]''').click()

    try:
        driver.find_element(By.XPATH, f'''//select[contains(@onchange, "Crop")]/option[text()="{crop}"]''').click()
    # if there is no such crop in district level
    except NoSuchElementException:
        save_txt("Missing Data.txt", name)
        return
    driver.find_element(By.XPATH, f'''//input[@type="submit"]''').click()
    get_bg(driver, name)
    time.sleep(3)
    # wc = True
    # if data != "err":
    #     save_csv(name + ".csv", data)
    # else:
    #     save_txt("err.txt", name)
    # except Exception as er:
    #     print("BUG！！BUG！！BUG！！", er)
    #     save_txt("错误日志.txt", "BUG！！BUG！！BUG！！"+str(er))


@retry(exceptions=NoSuchElementException, tries=3, delay=3, backoff=1)
def get_tehsil(Year, State, District=None, Tehsil=None, Crop=None, driver=None):
    if driver is None:
        driver = Chrome(options=chrome_options)
        cl = True
    else:
        cl = False
    driver.get("https://agcensus.dacnet.nic.in/TalukCharacteristics.aspx")

    driver.find_element(By.XPATH, f'''//select[@ onchange="return ONChangeYear('Year');"]//option[text()="{Year}"]''').click()

    driver.find_element(By.XPATH, f'''//select[@ onchange="return ONChangedState('State');"]//option[text()="{State}"]''').click()

    if District is None:
        select_element = driver.find_element(By.XPATH, f'''//select[@ onchange="return OnChangedDistrict('District');"]''')
        districts = [option.text for option in select_element.find_elements(By.XPATH, './/option')]
        print(districts)
        get_crop(Year, State, "all", "all", Crop, driver)
        for District in districts:
            get_tehsil(Year, State, District, Tehsil, Crop, driver)
        return
    else:
        driver.find_element(By.XPATH, f'''//select[@ onchange="return OnChangedDistrict('District');"]//option[text()="{District}"]''').click()

    if Tehsil is None:
        select_element = driver.find_element(By.XPATH, f'''//select[@ onchange="return ONChangedTehsil('Tehsil');"]''')
        tehsils = [option.text for option in select_element.find_elements(By.XPATH, './/option')]
        print(tehsils)
        get_crop(Year, State, District, "all", Crop, driver)
        for Tehsil in tehsils:
            get_crop(Year, State, District, Tehsil, Crop, driver)
        return
    else:
        get_crop(Year, State, District, Tehsil, Crop, driver)
    # else:
    #     driver.find_element(By.XPATH, f'''//select[@ onchange="return ONChangedTehsil('Tehsil');"]//option[text()="{Tehsil}"]''').click()
    #
    # driver.find_element(By.XPATH, f'''//select[@ onchange="return ONChangedTables('Tables');"]//option[text()="{tables}"]''').click()
    # driver.find_element(By.XPATH, f'''//select[@ onchange="return ONChangedSocialGroup('SocialGroup');"]//option[@ value="4"]''').click()

    if cl:
        driver.quit()


def save_txt(filename, data):
    with open(filename, 'a', newline='') as file:
        # for item in data:
        try:
            file.write(data + "\n")
        except:
            file.write("weird" + "\n")
        


def process_tehsil(key):
    try:
        get_tehsil(**key)
    except Exception as s:
        print(s)


def main(keys):
    # err = []
    # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    #     # 提交任务到线程池
    #     executor.map(process_tehsil, keys)
    for key in keys:
        get_tehsil(**key)
        # every time finish a key, erase corresponding line in the excel file
        # df.drop(1)
        # df.to_excel('input.xlsx', index=False) 
    # save_txt("err.txt", err)


if __name__ == '__main__':
    # ds = [{
    #     'year': "2010-11",
    #     'state': "A & N ISLANDS",
    #     'district': None,
    #     "tehsil": None,
    #     "crop": "TOMATO"
    # }]

    # 将数据转换为字典列表
    try:
        df = pd.read_excel('input.xlsx')
        df = df.replace({np.nan: None})
        ds = df.to_dict(orient='records')
    except Exception as er:
        print("BUG!!读取excel时", er)
        save_txt("错误日志.txt", "BUG!!BUG!!BUG!!" + str(er))
        while True:
            time.sleep(10)
    ti = time.time()
    # try:
    main(ds)
    # except Exception as er:
    #     print("BUG!!!!!!主程序", er)
    #     save_txt("错误日志.txt", "BUG！！BUG！！BUG！！" + str(er))
    #     while True:
    #         time.sleep(999)
    print(time.time() - ti)
