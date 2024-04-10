from selenium.webdriver.common.by import By
from file_saver import file_saver


class Crawler:
    def __init__(self, driver, utils, field_xpath_map, crop_type_map):
        self.driver = driver
        self.utils = utils
        self.field_xpath_map = field_xpath_map
        self.crop_type_map = crop_type_map
        self.saver = file_saver

    def crawl(self, crop_type, level):
        for xpath in self.field_xpath_map.values():
            if xpath == "":
                continue
            # reload the current page
            self.utils.reload_page_and_select_crop_type(crop_type, self.crop_type_map)

            page = 1
            total_index = 0
            page_maximum = self.driver.find_element(By.XPATH,
                                               "/html/body/div[1]/div[1]/div/div[3]/div[2]/div[1]/div/div[4]/div[2]/div/div[2]/div[2]/div[3]/div[1]/div/ul/li[3]/span").text
            # 会得到 "/ 9"，要去掉/
            page_maximum = page_maximum.replace("/", "")

            while (page <= int(page_maximum)):
                self.utils.change_page(page)
                # select crop:
                crop_table = self.utils.select_field_and_get_crop_table(xpath, page, total_index)
                length = len(crop_table)

                for i in range(0, length):
                    crop_table = self.driver.find_elements(By.XPATH,
                                                      "/html/body/div[1]/div[1]/div/div[3]/div[2]/div[1]/div/div[4]/div[2]/div/div[2]/div[2]/div[3]/div[4]/table/tbody[1]/tr")
                    crop_name = crop_table[i].text

                    if crop_name == "<All>":
                        continue

                    select_crop_successful = self.utils.select_crop_and_unit(i, page, total_index)
                    if not select_crop_successful:
                        self.saver.save_missing_crop_data(level, crop_name)
                        self.utils.return_to_homepage()
                        continue

                    # select the indictor
                    self.utils.select_the_indictor()
                    self.utils.select_all_years()
                    select_all_regions_successful = self.utils.select_all_regions(level)

                    if not select_all_regions_successful:
                        print("incorrect regions")
                        self.saver.save_missing_crop_data(level, crop_name)
                        self.utils.return_to_homepage()
                        continue

                    self.utils.generate_report()
                    self.utils.return_to_homepage()

                    total_index += 1

                self.utils.unclick_crop(i + 1, page, total_index)
                page += 1

            self.saver.rename_and_move_file(level, crop_type)