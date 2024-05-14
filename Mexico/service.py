from crawler import DistrictCrawler, StateCrawler
import numpy as np
import pandas as pd
import os

class Service:

    def __init__(self, dic) -> None:
        self.dic = dic    

    def start(self):
        
        if self.dic["State"] is None:
            file_name = f"State_{self.dic['Crop']}_{self.dic['Year']}.xlsx"
            new_craw = StateCrawler(self.dic)
            raw_df = new_craw.crawling()
        else:
            file_name = f"{self.dic['State']}_{self.dic['Crop']}_{self.dic['Year']}.xlsx"
            new_craw = DistrictCrawler(self.dic)
            raw_df = new_craw.crawling()

        download_path = os.path.join(os.getcwd(),'downloads',file_name)
        raw_df.to_excel(download_path,index=False)
    

    