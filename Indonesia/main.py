import pandas as pd
import numpy as np
from service import Service
from crawler import StateCrawler
if __name__ == '__main__':
    df = pd.read_excel('input.xlsx')
    df = df.replace(np.nan, None)
    dict_list = df.to_dict(orient='records')

    print(dict_list)

    print('program starts')

    for dic in dict_list:
        service = Service(dic)
        service.start()
        #craw = StateCrawler(dic)
        #craw.crawling()

    print("Program ends")