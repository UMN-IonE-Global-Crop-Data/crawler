import time
import numpy as np
import pandas as pd
from selenium.webdriver import Chrome

import config
import service


chrome_options = config.chrome_options

if __name__ == '__main__':
    # convert excel data to python dictionary 
    try:
        df = pd.read_excel('input.xlsx')
        df = df.replace({np.nan: None})
        keys = df.to_dict(orient='records')
    except Exception as er:
        raise Exception("incorrect excel input format!")

    # start crawling
    start_time = time.time()

    driver = Chrome(options=chrome_options)
    for key in keys:
        service.crawl(driver, **key)
    
    end_time = time.time()
    print(end_time - start_time)
