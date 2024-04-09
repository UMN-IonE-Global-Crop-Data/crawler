from selenium import webdriver
from selenium.webdriver.common.by import By

import config
from crawler import Crawler
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




# level = "NUTS3 (Province Level)"
driver = webdriver.Chrome()
driver.implicitly_wait(5)
utils = Utils(driver)
crawler = Crawler(driver, utils, field_xpath_map, crop_type_map)

if __name__ == "__main__":  
    for level in levels: 
        for crop_type in crop_type_map.keys():
            set_up(crop_type)
            crawler.crawl(crop_type, level)
            utils.merge(level, crop_type)

# utils.rename_and_move_file(level)


