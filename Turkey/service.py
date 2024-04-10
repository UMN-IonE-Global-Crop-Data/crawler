from selenium import webdriver
from selenium.webdriver.common.by import By

from crawler import Crawler
from web_operator import WebOperator
from config import Config
from merger import merger


class Service:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)


    def start(self, dic: dict):
        crop_group = dic["Group"]
        level = dic["Level"]
        web_operator = WebOperator(self.driver, crop_group)
        config = Config(web_operator)
        data_field_xpath_map = config.setup_field_map()

        crawler = Crawler(self.driver, web_operator, data_field_xpath_map)
        crawler.crawl(crop_group, level)
        merger.merge(crop_group, level)

service = Service()