from file_saver import file_saver


class ICrawler:
    def __init__(self, driver, web_operator, data_field_xpath_map, group, level):
        self.driver = driver
        self.web_operator = web_operator
        self.field_xpath_map = data_field_xpath_map
        self.saver = file_saver
        self.group = group
        self.level = level

    def crawl(self):
        pass


