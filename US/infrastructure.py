import requests
import pandas as pd
import numpy as np
import os

api_key = "789AAD3D-2872-3A4D-87F5-59CB6B246889"
data_item = ""
prod_unit = ""
source = ""
crop = ""
year = ""

# 第一步：从网站fetch数据
def fetch(type, dic):
    # census里面没有irr/non-irr production数据，直接返回
    
    global data_item, prod_unit, source, crop, year

    crop = dic["Commodity"].replace("&", "%26")
    year = int(dic["Year"])                     # input will be set to float automatically
    source = dic["Program"]
    sector = dic["Sector"].replace("&", "%26")
    group = dic["Group"].replace("&", "%26")  # replace "&" with %26 so that it won't affect API url
    domain_desc = dic["Domain"].replace("&", "%26")

    if dic["Data_item"] == "":
        data_item = crop
    else:
        data_item = dic["Data_item"] # config.data_item
    
    prod_unit = dic["Prod_unit"]
    # if dic["Irrigated"] != None:
    #     irr = dic["Irrigated"] # if we want irrigated or non-irrigated data, this will label the final file with corresponding names

    
    if type == "production" and crop == "TOMATOES":
    # if type == "production" and "IRRIGATED" in data_item and "CENSUS" in source: 
        return []
    
    url = f"https://quickstats.nass.usda.gov/api/api_GET/?key={api_key}" \
    f"&source_desc={source}&sector_desc={sector}&group_desc={group}" \
    f"&commodity_desc={crop}&domain_desc={domain_desc}" \
    f"&year={year}&reference_period_desc=YEAR&format=JSON"
    if type == "area":
        url += f"&short_desc={data_item} - ACRES HARVESTED"
    elif type == "production":
        url += f"&short_desc={data_item} - PRODUCTION, MEASURED IN {prod_unit}"

    response = requests.get(url)

    data = None

    if response.status_code == 200:
        # 获取返回的数据
        data = response.json()['data']  # 使用 .json() 方法解析 JSON 数据
        return data
    else:
        raise RuntimeError(f"This request for {crop} in {year} is incorrect, please go to the website to check all fields")

# 筛选出state级别数据
def filterState(data):
    return filterLevel(data, "STATE")

# 筛选出county级别数据
def filterCounty(data):
    return filterLevel(data, "COUNTY")

def filterLevel(data, level):
    filteredData = myFilter(data, level)
    df = buildDF(filteredData, level)
    return df


def myFilter(arr, level):
    result = []
    for ele in arr:
        if ele["agg_level_desc"] == level:
            result.append(ele)
    return result


#  拿到数据后，建立df
def buildDF(arr, level):

    header = []
    if level == "STATE":
        header = ["Program", "State", "Year", "Cropnm", "Area(Acre)"]
    
   
    elif level == "COUNTY":
        header = ["Program", "State", "Ag District", "County", "Year", "Cropnm", "Area(Acre)"]
    
    df = pd.DataFrame(columns= header)

    # 添加新的行
    for dp in arr:
        if level == "STATE":
           new_row = [dp['source_desc'], dp['state_name'], dp['year'], dp['commodity_desc'], dp['Value']]

        elif level == "COUNTY":
            new_row = [dp['source_desc'], dp['state_name'], dp['asd_desc'], dp['county_name'], dp['year'], dp['commodity_desc'], dp['Value']]
        
        df.loc[len(df)] = new_row

    return df

def merge(area, prod, level):
    rowsA = len(area)
    rowsB = len(prod)
    
    length = area.shape[1]

    if not os.path.exists("CENSUS"):
        os.mkdir("CENSUS")
        os.mkdir("CENSUS/State_Level")
        os.mkdir("CENSUS/County_Level")

    if not os.path.exists("SURVEY"):
        os.mkdir("SURVEY")
        os.mkdir("SURVEY/State_Level")
        os.mkdir("SURVEY/County_Level")

    irr = ""
    if "IRRIGATED" in data_item and "NON-IRRIGATED" not in data_item:
        irr = "-irr"
    elif "NON-IRRIGATED" in data_item:
        irr = "-nonirr"


    # census里面没有irr/non-irr production数据，直接返回
    if rowsA != 0 and rowsB == 0:
        if level == "State":
            area.to_csv(f"{source}\\State_Level\\State_{area.iloc[0,2]}_{area.iloc[0,3]}{irr}.csv", index = False)
        elif level == "County":
            area.to_csv(f"{source}\\County_Level\\County_{area.iloc[0,4]}_{area.iloc[0,5]}{irr}.csv", index = False)
        return


    # guard clause
    if rowsA != rowsB:
        print(f"Producation and area have different rows, please check the file error{area.iloc[0,2]}_{area.iloc[0,3]}.csv in the folder to fix the problem")
        result_df = pd.concat([area, prod], ignore_index=True)
        result_df.to_csv(f"error{area.iloc[0,2]}_{area.iloc[0,3]}.csv", index = False)
        return
        

    if rowsA == 0:
        print(f"{crop} in {year} at {level} not found")
        return

    area[f"Production({prod_unit})"] = np.where((area.iloc[:, :-2] == prod.iloc[:, :-2]).all(axis=1), prod.iloc[:, -1], np.nan)
    filename = ""
    filepath = ""

    # merge后length 变化了，需要重新计算
    length = area.shape[1]

    if length == 6:
        filename = f"State_{area.iloc[0,2]}_{area.iloc[0,3]}"
        filepath = os.path.join(f"{source}/State_Level", filename)
    
    elif length == 8:
        filename = f"County_{area.iloc[0,4]}_{area.iloc[0,5]}"
        filepath = os.path.join(f"{source}/County_Level", filename)
    

    filepath += f"{irr}.csv"
    area.to_csv(filepath, index = False)
    


