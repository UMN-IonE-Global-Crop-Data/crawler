import pandas as pd
import numpy as np
from service import service

if __name__ == "__main__":
    df = pd.read_excel("input.xlsx")
    df = df.replace({np.nan: None})
    dic_list = df.to_dict(orient="records")

    print("Program Starts")

    for dic in dic_list:
        service.start(dic)

    print("Program Ends")

