from crawler import DistrictCrawler, StateCrawler
import numpy as np
import pandas as pd
import os

class Service:


    def __init__(self, dic) -> None:
        self.dic = dic  
        self.crop_name = {}
        self.indicator_eng = {
            "LUAS PANEN": "harvest area (Ha)",
            "LUAS AREAL": "Area (Ha)",
            "PRODUKSI": "production (Ton)",
            "PRODUKTIVITAS": "productivity (Quintal/Ha)"
        }
    
        filepath = os.path.join(os.getcwd(),'dict','Ind to Eng.txt')
        with open(filepath, 'r',encoding='utf-8') as file:
            for line in file:
                if line.strip():  # Ensure that the line is not empty
                    key, value = line.strip().split(': ')
                    self.crop_name[key] = value
            file.close
  

    def start(self):
        
        if self.dic["Level"] == "Kabupaten":
            file_name = f"{self.crop_name.get(self.dic['Crop'])}_{self.indicator_eng.get(self.dic['Indicator'])}_{self.dic['Province']}.xlsx"
            new_craw = DistrictCrawler(self.dic)
            df = new_craw.crawling()
        else:
            file_name = f"{self.dic['Crop']}.xlsx"
            new_craw = StateCrawler(self.dic)
            df = new_craw.crawling()

        download_path = os.path.join(os.getcwd(),'downloads',file_name)
        df.to_excel(download_path,index=False)
   
    
