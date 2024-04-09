from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

import config
from utils import Utils


crop_type_map = config.crop_type_map
field_xpath_map = config.field_xpath_map
table_xpath = config.table_xpath
levels = config.levels


def set_up(crop_type):
    utils.reload_page_and_select_crop_type(crop_type, crop_type_map)

    # get all elements in the table
    table = driver.find_elements(By.XPATH, config.table_xpath)
    
    if len(table) == 3:
        field_xpath_map["production"] = f"{table_xpath}[3]/td/div"
    elif len(table) == 5:
        field_xpath_map["harvest_area"] = f"{table_xpath}[3]/td/div"
        field_xpath_map["yield"] = f"{table_xpath}[4]/td/div"
        field_xpath_map["production"] = f"{table_xpath}[5]/td/div"
    elif len(table) == 6: # fruit
        field_xpath_map.clear()
        field_xpath_map["area_of_compact"] = f"{table_xpath}[2]/td/div"
        field_xpath_map["number_of_bearing"] = f"{table_xpath}[3]/td/div"
        field_xpath_map["number_of_non_bearing"] = f"{table_xpath}[4]/td/div"
        field_xpath_map["yield"] = f"{table_xpath}[5]/td/div"
        field_xpath_map["production"] = f"{table_xpath}[6]/td/div"


def crawl(crop_type, level):
    # select field (sown_area, harvest_area, yield, sown_area, production)
    for xpath in field_xpath_map.values():
        if xpath == "":
            continue
        # reload the current page
        utils.reload_page_and_select_crop_type(crop_type, crop_type_map)
    
        page = 1
        total_index = 0
        page_maximum = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/div[2]/div[1]/div/div[4]/div[2]/div/div[2]/div[2]/div[3]/div[1]/div/ul/li[3]/span").text
        # 会得到 "/ 9"，要去掉/
        page_maximum = page_maximum.replace("/", "")

        while (page <= int(page_maximum)):
            utils.change_page(page)
            # select crop:
            crop_table = utils.select_field_and_get_crop_table(xpath, page, total_index)
            length = len(crop_table)

            for i in range(0,length):
                crop_table = driver.find_elements(By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/div[2]/div[1]/div/div[4]/div[2]/div/div[2]/div[2]/div[3]/div[4]/table/tbody[1]/tr")
                crop_name = crop_table[i].text

                if crop_name == "<All>":
                    continue

                select_crop_successful = utils.select_crop_and_unit(i, page, total_index)
                if not select_crop_successful:
                    utils.save_missing_crop_data(level, crop_name)
                    utils.return_to_homepage()
                    continue

                # select the indictor
                utils.select_the_indictor()
                utils.select_all_years()
                select_all_regions_sucessful = utils.select_all_regions(level)

                if not select_all_regions_sucessful:
                    utils.save_missing_crop_data(level, crop_name)
                    utils.return_to_homepage()
                    continue
    
                utils.generate_report()
                utils.return_to_homepage()

                total_index += 1

            utils.unclick_crop(i+1, page, total_index)
            page += 1

            # search_input = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[3]/div[2]/div[1]/div/div[4]/div[2]/div/div[2]/div[2]/div[1]/input")
            # # send page number to the page_input
            # search_input.send_keys(Keys.CONTROL + "a")  # select all things in the input
            # search_input.clear()
            # search_input.send_keys(Keys.ENTER)
            # time.sleep(0.5)

        utils.rename_and_move_file(level, crop_type)


    # # Close the browser window
    # driver.quit()

# level = "NUTS3 (Province Level)"
driver = webdriver.Chrome()
driver.implicitly_wait(5)
utils = Utils(driver)

if __name__ == "__main__":  
    for level in levels: 
        for crop_type in crop_type_map.keys():
            set_up(crop_type)
            crawl(crop_type, level)
            utils.merge(level, crop_type)

# utils.rename_and_move_file(level)


