import pandas as pd
import numpy as np

import service


if __name__ == '__main__':
    df = pd.read_excel('input.xlsx')
    df = df.replace({np.nan: ""})
    dict_list = df.to_dict(orient='records')

    print("Program starts")

    for dic in dict_list:
        # if dic["Year"] == None:
        #     # traverse all years
        #     cur_year = int(datetime.now().strftime("%Y"))
        #     for year in range(1998,cur_year):
        #         dic["Year"] = year
        #         fetchData(dic)
        # else:
            service.fetchData(dic)
    
    print("Program ends")











