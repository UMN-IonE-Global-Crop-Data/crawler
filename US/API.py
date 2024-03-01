# parameters = {
#     "key": "789AAD3D-2872-3A4D-87F5-59CB6B246889",
#     "source_desc": "SURVEY",
#     "sector_desc": "CROPS",
#     "group_desc": "FIELD CROPS",

#     "commodity_desc": "CORN",
#     "prodn_practice_desc": "GRAIN",
#     "statisticcat_desc": "AREA HARVESTED",
#     "short_desc": f"{crop}, {prodn_practice_desc} - ACRES HARVESTED",

#     "year": 2012,
#     "format" : "JSON"
# }

# url = "https://quickstats.nass.usda.gov/api/api_GET/?"



import pandas as pd
import numpy as np
from datetime import datetime

import service


# 1. download are
# 2. download production
# 3. merge the area and production
def fetchData(dic):

    # area data
    areaDFArr = service.fetchArea(dic)
    areaState, areaCounty = areaDFArr[0], areaDFArr[1]

    # production data
    prodDFArr = service.fetchProduction(dic)
    prodState, prodCounty = prodDFArr[0], prodDFArr[1]

    # merge
    service.merge(areaState, prodState, "State")
    service.merge(areaCounty, prodCounty, "County")


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
            fetchData(dic)
    
    print("Program ends")











