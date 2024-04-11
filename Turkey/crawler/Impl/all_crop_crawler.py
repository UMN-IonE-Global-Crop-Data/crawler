from selenium.webdriver.common.by import By
from crawler.Icrawler import ICrawler

class AllCropCrawler(ICrawler):

    def __init__(self, driver, web_operator, data_field_xpath_map, group, level):
        super(AllCropCrawler, self).__init__(driver, web_operator, data_field_xpath_map, group, level)

    def crawl(self):
        for xpath in self.field_xpath_map.values():
            # reload the current page
            self.web_operator.reload_page_and_select_crop_type()

            page = 1
            total_index = 0
            page_maximum = self.driver.find_element(By.XPATH,
                                                    "/html/body/div[1]/div[1]/div/div[3]/div[2]/div[1]/div/div[4]/div[2]/div/div[2]/div[2]/div[3]/div[1]/div/ul/li[3]/span").text
            # 会得到 "/ 9"，要去掉/
            page_maximum = page_maximum.replace("/", "")

            while (page <= int(page_maximum)):
                self.web_operator.change_page(page)
                # select crop:
                self.web_operator.select_field(xpath, page, total_index)

                crop_table = self.web_operator.get_crop_table()
                length = len(crop_table)

                for i in range(0, length):
                    crop_table = self.driver.find_elements(By.XPATH,
                                                           "/html/body/div[1]/div[1]/div/div[3]/div[2]/div[1]/div/div[4]/div[2]/div/div[2]/div[2]/div[3]/div[4]/table/tbody[1]/tr")
                    crop_name = crop_table[i].text

                    if crop_name == "<All>":
                        continue

                    select_crop_successful = self.web_operator.select_crop_and_unit(i, page, total_index)
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

                    total_index += 1

                self.web_operator.unclick_crop(i + 1, page, total_index)
                page += 1

            self.saver.rename_and_move_file(self.level, self.group)
