from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
import os
import time

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

def get_datapoint(year, state, district, tehsil, crop, driver):
    name = "_".join([year, state, district, tehsil.replace('\xa0', ""), crop])
    if district == "all":
        driver.get("https://inputsurvey.dacnet.nic.in/nationaltables.aspx")
    elif tehsil == "all":
        driver.get("https://inputsurvey.dacnet.nic.in/statetables.aspx")
    else:
        driver.get("https://inputsurvey.dacnet.nic.in/districttables.aspx")

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


def get_(Year, State, District=None, Tehsil=None, Crop=None, driver=None):
    driver.get("https://inputsurvey.dacnet.nic.in/statetables.aspx")

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




def save_txt(filename, data):
    with open(filename, 'a', newline='') as file:
        file.write(data + "\n")
