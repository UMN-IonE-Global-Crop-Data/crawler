from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import time
from constant import CROP_NAME_TABLE_XPATH, GROUP_TO_XPATH_MAP, FIELD_TABLE_XPATH, CROP_INPUT_PATH


class WebOperator:
    def __init__(self, driver, crop_group):
        self.driver = driver
        self.crop_group = crop_group

    def reload_page_and_select_crop_type(self):
        self.driver.get("https://biruni.tuik.gov.tr/medas/?kn=92&locale=en")

        crop_type = self.driver.find_element(By.XPATH, GROUP_TO_XPATH_MAP[self.crop_group])
        crop_type.click()

        # ok_button is disabled in the first place, wait until it is available
        ok_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div/div[3]/div[2]/div[1]/div/div[3]/div[2]/table/tbody/tr/td/table/tbody/tr/td[3]/div/div[2]/table/tbody/tr/td/table/tbody/tr[3]/td/div/table/tbody/tr/td/table/tbody/tr/td[5]/div/button[1]"))
        )

        if ok_button.is_enabled():
            ok_button.click()
        else:
            print("button is not available!")

        time.sleep(0.5)

    def get_field_table(self):
        return self.driver.find_elements(By.XPATH, FIELD_TABLE_XPATH)

    def unclick_crop(self, index, page, total_index):

        # unclick the previous crop element
        crop_table = self.driver.find_elements(By.XPATH, CROP_NAME_TABLE_XPATH)

        # 不要
        # if index > 8: # for test
        if (page == 1 and index > 1) or (page > 1 and index > 0):
            crop_table[index-1].click()
            self.change_page(page)

        # if index > 8:   # for test
        if (total_index > 0) and ((page == 1 and index > 1) or (page > 1 and index > 0)) :
            # delete the preivous indictor
            preivous_indictor = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/div[2]/div[1]/div/div[8]/div[2]/div[1]/div/div/div[3]/table/tbody[1]/tr/td[1]/div/a").click()
        time.sleep(0.5)

    def choose_crop(self, crop_name):
        crop_input = self.driver.find_element(By.XPATH, CROP_INPUT_PATH)

        crop_input.send_keys(crop_name)
        crop_input.send_keys(Keys.ENTER)

    def change_page(self, page):
        xpath = "/html/body/div[1]/div[1]/div/div[3]/div[2]/div[1]/div/div[4]/div[2]/div/div[2]/div[2]/div[3]/div[1]/div/ul/li[3]/input"

        try:
            # Find the element
            page_input = self.driver.find_element(By.XPATH, xpath)
            # Perform actions on the element
            page_input.send_keys(Keys.CONTROL + "a")  # select all things in the input
            page_input.send_keys(page)
            page_input.send_keys(Keys.ENTER)

        except StaleElementReferenceException:
            # If element is stale, wait and attempt to find it again
            time.sleep(1)
            page_input = self.driver.find_element(By.XPATH, xpath)
            page_input.send_keys(Keys.CONTROL + "a")  # select all things in the input
            page_input.send_keys(page)
            page_input.send_keys(Keys.ENTER)


    def select_unit(self):
        unit_xpath = "/html/body/div/div[1]/div/div[3]/div[2]/div[1]/div/div[4]/div[2]/div/div[3]/div[2]/div[3]/div[4]/table/tbody[1]/tr"
        unit = self.driver.find_elements(By.XPATH, unit_xpath)

        if len(unit) != 1:
            raise Exception("abnormal measurements")

        unit[0].click()
        time.sleep(0.5)

    def select_a_single_crop_and_unit(self, index):
        crop_table = self.driver.find_elements(By.XPATH, CROP_NAME_TABLE_XPATH)
        crop_table[index].click()
        time.sleep(0.5)
        self.select_unit()
        add_measurement_button = self.driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[3]/div[2]/div[1]/div/div[6]/div[1]/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/a/span").click()

        return True

    def select_crop_and_unit(self, index, page, total_index):
        # the crop selected last time needs to be un-checked
        self.unclick_crop(index, page, total_index)

        if total_index != 0:
            self.select_unit()

        self.change_page(page)

        time.sleep(0.5)
        crop_table = self.driver.find_elements(By.XPATH, CROP_NAME_TABLE_XPATH)
        crop_table[index].click()
        time.sleep(0.5)

        self.select_unit()

        add_measurement_button = self.driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div[3]/div[2]/div[1]/div/div[6]/div[1]/div/div/div/table/tbody/tr/td/table/tbody/tr/td[1]/a/span").click()

        return True

    def select_field(self, xpath, page=1, total_index=0):
        if page == 1 or total_index == 0:
            self.driver.find_element(By.XPATH, xpath).click()
            time.sleep(0.5)

    def get_crop_table(self):
        crop_table = self.driver.find_elements(By.XPATH, CROP_NAME_TABLE_XPATH)
        time.sleep(0.5)

        return crop_table


    def return_to_homepage(self):
        by_indicotor_page = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/div[1]/ul/li[1]/a/span")
        self.driver.execute_script("window.scrollTo(0, 0)")  # scoll up to include target the button
        by_indicotor_page.click()
        time.sleep(0.5)


    def select_the_indictor(self):
        indictors_table_xpath = "/html/body/div/div[1]/div/div[3]/div[2]/div[1]/div/div[8]/div[2]/div[1]/div/div/div[3]/table/tbody[1]/tr/td"

        indictor_table = self.driver.find_elements(By.XPATH, indictors_table_xpath)

        # if more than three, means there are more than one indictors
        if len(indictor_table) != 3:
            raise Exception("abnormal indictors")

        self.driver.find_element(By.XPATH, f"{indictors_table_xpath}[2]/div").click()

        forward_button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/div[2]/div[1]/div/div[9]/button").click()
        time.sleep(0.7)


    def select_all_years(self):
        all_year_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/div[2]/div[2]/div/div[1]/div[2]/table/tbody/tr/td/table/tbody/tr/td[1]/div/div[1]/table/tbody/tr/th[1]/div/span"))
        )
        all_year_button.click()

        forward_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/div[2]/div[2]/div/div[2]/button[2]"))
        )
        forward_button.click()


    def select_all_regions(self, level):
        time.sleep(0.5)
        region_dropdown_xpath = "/html/body/div[1]/div[1]/div/div[3]/div[2]/div[3]/div/div[1]/div/div[1]/div/div/div/select"

        try:
            option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'''{region_dropdown_xpath}//option[text()="{level}"]'''))
            )
            option.click()
            time.sleep(0.5)
        except Exception as e:
            print(e)
            return False


        # select all regions
        all_region_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/div[2]/div[3]/div/div[1]/div/div[2]/table/tbody/tr/td/table/tbody/tr/td[1]/div/div[1]/table/tbody/tr/th[1]/div/span")
        ))
        all_region_button.click()
        time.sleep(0.5)
        return True


    def generate_report(self):
        time.sleep(0.5)
        create_report_button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/div[2]/div[3]/div/div[2]/button[2]")
        time.sleep(0.5)
        create_report_button.click()

        try:
            xslx_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/div[2]/div[4]/div[1]/div[3]/div/div/div/div[2]/div[3]/div/div/div[3]/a/span"))
            )
            xslx_button.click()

            time.sleep(0.5)
        except Exception as e:
            xslx_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/div[2]/div[4]/div[1]/div[3]/div/div/div/div[2]/div[3]/div/div/div[3]/a/span"))
            )
            xslx_button.click()

            time.sleep(0.5)