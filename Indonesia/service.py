from crawler import DistrictCrawler, StateCrawler
import numpy as np
import pandas as pd
import os

class Service:

    def __init__(self, dic) -> None:
        self.dic = dic    

    def start(self):
        
        if self.dic["Level"] == "Kabupaten":
            file_name = f"{self.dic['Province']}_{self.dic['Level']}_{self.dic['Crop']}.xlsx"
            new_craw = DistrictCrawler(self.dic)
            df = new_craw.crawling()
        else:
            file_name = f"{self.dic['Level']}_{self.dic['Crop']}.xlsx"
            new_craw = StateCrawler(self.dic)
            df = new_craw.crawling()

        download_path = os.path.join(os.getcwd(),'downloads',file_name)
        df.to_excel(download_path,index=False)
   
    
