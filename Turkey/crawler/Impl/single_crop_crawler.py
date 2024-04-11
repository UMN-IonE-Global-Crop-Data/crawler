import time

from selenium.webdriver.common.by import By
from crawler.Icrawler import ICrawler

class SingleCropCrawler(ICrawler):

    def __init__(self, driver, utils, data_field_xpath_map, group, level, crop):
        super(SingleCropCrawler, self).__init__(driver, utils, data_field_xpath_map, group, level)
        self.crop = crop

    def crawl(self):
        self.web_operator.reload_page_and_select_crop_type()

        for xpath in self.field_xpath_map.values():
            self.web_operator.reload_page_and_select_crop_type()
            self.web_operator.select_field(xpath)
            self.web_operator.choose_crop(self.crop)
            time.sleep(0.5)
            crop_table = self.web_operator.get_crop_table()

            i = 1
            crop_table = self.driver.find_elements(By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/div[2]/div[1]/div/div[4]/div[2]/div/div[2]/div[2]/div[3]/div[4]/table/tbody[1]/tr")
            crop_name = crop_table[i].text

            select_crop_successful = self.web_operator.select_a_single_crop_and_unit(i)

            if not select_crop_successful:
                self.saver.save_missing_crop_data(self.level, crop_name)
                self.web_operator.return_to_homepage()
                continue

            # select the indictor
            self.web_operator.select_the_indictor()
            self.web_operator.select_all_years()
            select_all_regions_successful = self.web_operator.select_all_regions(self.level)

            if not select_all_regions_successful:
                print("incorrect regions")
                self.saver.save_missing_crop_data(self.level, crop_name)
                self.web_operator.return_to_homepage()
                continue

            self.web_operator.generate_report()
            self.web_operator.return_to_homepage()

        self.saver.rename_and_move_file(self.level, self.group)


