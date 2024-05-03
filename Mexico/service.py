from crawler import DistrictCrawler, StateCrawler

class Service:

    def __init__(self, dic) -> None:
        self.dic = dic    

    def start(self):
        new_craw = DistrictCrawler(self.dic)
        raw_df = new_craw.crawling()
