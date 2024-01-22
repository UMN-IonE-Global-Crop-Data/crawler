from selenium import webdriver
from selenium.webdriver.common.by import By
from strategy import NonSubCrawler, SubCrawler

import config
import utils


crop_type_map = config.crop_type_map
field_xpath_map = config.field_xpath_map
table_xpath = config.table_xpath
levels = config.levels


def set_up(crop_type):
    utils.reload_page_and_select_crop_type(driver, crop_type, crop_type_map)

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
    if crop_type == "Subprovince Level":
        crawler = SubCrawler()
    else:
        crawler = NonSubCrawler(crop_type, level)
    
    for xpath in field_xpath_map.values():
        if xpath == "":
            continue
        
        utils.reload_page_and_select_crop_type(driver, crop_type, crop_type_map)

        page = 1
        total_index = 0
        page_maximum = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/div[2]/div[1]/div/div[4]/div[2]/div/div[2]/div[2]/div[3]/div[1]/div/ul/li[3]/span").text
        # 会得到 "/ 9"，要去掉/
        page_maximum = page_maximum.replace("/", "")

        while (page <= int(page_maximum)):
            crawler.change_page(driver, page)
            # select crop:
            crop_table = crawler.select_field_and_get_crop_table(driver, xpath, page, total_index)
            length = len(crop_table)

            for i in range(0,length):
                crop_table = driver.find_elements(By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/div[2]/div[1]/div/div[4]/div[2]/div/div[2]/div[2]/div[3]/div[4]/table/tbody[1]/tr")
                crop_name = crop_table[i].text

                if crop_name == "<All>":
                    continue

                select_crop_successful = crawler.select_crop_and_unit(driver, i, page, total_index)
                if not select_crop_successful:
                    utils.save_missing_crop_data(level, crop_name)
                    crawler.return_to_homepage(driver)
                    continue

                # select the indictor
                crawler.select_the_indictor(driver)
                crawler.select_all_years(driver)
                select_all_regions_sucessful = crawler.select_all_regions(driver, level)

                if not select_all_regions_sucessful:
                    utils.save_missing_crop_data(level, crop_name)
                    crawler.return_to_homepage(driver)
                    continue
    
                crawler.generate_report(driver)
                crawler.return_to_homepage(driver)

                total_index += 1

            crawler.unclick_crop(driver, i+1, page, total_index)
            page += 1

        utils.rename_and_move_file(level, crop_type)



level = "NUTS3 (Province Level)"
driver = webdriver.Chrome()
driver.implicitly_wait(5)


for level in levels: 
    for crop_type in crop_type_map.keys():
        set_up(crop_type)
        crawl(crop_type, level)
        utils.merge(level, crop_type)


# if __name__ == "__main__":  
#     for level in levels: 
#         for crop_type in crop_type_map.keys():
#             set_up(crop_type)
#             crawl(crop_type, level)
#             utils.merge(level, crop_type)

# utils.rename_and_move_file(level)


