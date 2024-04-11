from selenium import webdriver
import os

from crawler.Impl.all_crop_crawler import AllCropCrawler
from crawler.Impl.single_crop_crawler import SingleCropCrawler
from web_operator import WebOperator
from config import Config
from merger import merger


class Service:

    def __init__(self):
        download_path = os.path.join(os.getcwd(), 'downloads')
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": download_path,
                 "download.prompt_for_download": False,
                 "download.directory_upgrade": True,
                 "safebrowsing.enabled": True
                 }
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)

    def start(self, dic: dict):
        group = dic["Group"]
        level = dic["Level"]
        crop = dic["Crop"]

        web_operator = WebOperator(self.driver, group)
        config = Config(web_operator)
        data_field_xpath_map = config.set_up_everything()

        if not crop:
            crawler = AllCropCrawler(self.driver, web_operator, data_field_xpath_map, group, level)
        else:
            crawler = SingleCropCrawler(self.driver, web_operator, data_field_xpath_map, group, level, crop)
        crawler.crawl()

        # finish data downloading
        merger.merge(level, group)


service = Service()