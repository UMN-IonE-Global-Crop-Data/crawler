import pandas as pd
import numpy as np
from crawler import DistrictCrawler, StateCrawler



if __name__ == '__main__':
    df = pd.read_excel('input.xlsx')
    df = df.replace({np.nan, ""})
    dict_list = df.to_dict(orient='records')

    print(dict_list)

    print('program starts')

    for i in range(0,len(dict_list)):
        new_craw = DistrictCrawler(dict_list[i])
        new_craw.crawling()

        
    print("Program ends")