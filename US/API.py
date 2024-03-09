import pandas as pd
import numpy as np

from service import Service


if __name__ == '__main__':
    df = pd.read_excel('input.xlsx')
    df = df.replace({np.nan: ""})
    dict_list = df.to_dict(orient='records')

    print("Program starts")

    for dic in dict_list:
        cur_service = Service(dic)
        cur_service.fetchData()
    
    print("Program ends")











