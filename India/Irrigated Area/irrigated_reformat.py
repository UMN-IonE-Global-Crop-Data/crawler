import pandas as pd
import numpy as np
import os

def load_data():
    path = os.getcwd()
    for file in os.listdir(path):
        if file.endswith(".xlsx"):
            district_level(file)

def district_level(file):
    df = pd.read_excel(file, header = None)
    df = df.replace({np.nan: None})
    format(df)
    # 获取year
    year = df.iloc[1][0][-17:-10]
    #找到" State"对应字符下标
    index = df.iloc[1][0].find(" State")
    # 获取state
    state = df.iloc[1][0][55:index]

    # 去除第一列的序号
    df.iloc[:, 0] = df.iloc[:, 0].replace(r'\d+\.(.*)',r'\1', regex = True)
    


    col_len = len(df.columns)
    print(col_len)


    # if col_len == 44:
    #     # 填充作物名
    #     df.iloc[5, 2:5] = "Rice"
    #     df.iloc[5, 6:8] = "Jowar"
    #     df.iloc[5, 14:16] = "Other Cereals"
    #     df.iloc[5, 21:23] = "Other Pulses"
    #     df.iloc[5][24] = df.iloc[4][24]
    #     df.iloc[5, 26:30] = df.iloc[4, 26:30]
    #     df.iloc[5, 40:43] = df.iloc[4, 40:43]
    #     df.iloc[5,43] = df.iloc[3,43]
    #         # 删除空白列
    #     df = df.drop(df.columns[16], axis=1)

    # elif col_len == 43:
    #     df.iloc[5, 2:5] = "Rice"
    #     df.iloc[5, 6:8] = "Jowar"
    #     df.iloc[5, 14:16] = "Other Cereals"
    #     df.iloc[5, 21:23] = "Other Pulses"
    #     df.iloc[5, 25:29] = df.iloc[4, 25:29]
    #     df.iloc[5, 39:42] = df.iloc[4, 39:42]
    #     df.iloc[5,42] = df.iloc[3,42]
    #     # 删除空白列
    #     df = df.drop(df.columns[16], axis=1)


    # elif col_len == 2:
    #     #将文件名保存到err.txt文件
    #     with open("err.txt", "a") as f:
    #         f.write(file)
    #         f.write("\n")
    #     return
    
    # elif col_len == 14:
    #     df.iloc[5, 2:5] = "Rice"
    #     df.iloc[5][8] = df.iloc[4][8]
    #     df.iloc[5, 10:13] = df.iloc[4, 10:13]
    #     df.iloc[5, 13] = df.iloc[3, 13]

    # elif col_len == 45:
    #     df.iloc[5, 2:6] = "Rice"
    #     df.iloc[5, 7:9] = "Jowar"
    #     df = df.drop(df.columns[16], axis=1)
    #     df.iloc[5, 15:17] = "Other Cereals"
    #     df.iloc[5, 21:23] = "Other Pulses"
    #     df.iloc[5, 24] = df.iloc[4, 24]
    #     df.iloc[5, 26:30] = df.iloc[4, 26:30]
    #     df.iloc[5, 40:43] = df.iloc[4, 40:43]
    #     df.iloc[5,43] = df.iloc[3,43]


    # elif col_len == 46:
    #     df.iloc[5, 2:5] = "Rice"
    #     df.iloc[5, 6:8] = "Jowar"

    # else:
    #     # 只能处理两种类型的file
    #     raise Exception("Wrong format")
    

    district_level_df = pd.DataFrame(columns=["State","District", "Year", "Season", "Crop", "Irrigated Area(ha)"])
    state_level_df = pd.DataFrame(columns = ["State", "Year", "Season", "Crop", "Irrigated Area(ha)"])
    for i in range(7, len(df)):
        # 获取district名
        district = df.iloc[i][0]
        for j in range(1, len(df.columns)):
            crop = df.iloc[5][df.columns[j]]
            season = df.iloc[6][df.columns[j]]
            area = df.iloc[i][df.columns[j]]
            # 如果是最后一行，保留到state_level
            if i == len(df) - 1:
                new_row = [state, year, season, crop, area]
                state_level_df.loc[len(state_level_df)] = new_row
            else:
                new_row = [state, district, year, season, crop, area]
                district_level_df.loc[len(district_level_df)] = new_row
    # 接着把该文件转入./finished/District Level路径下
    district_level_df.to_excel(file, index=False)

    # 保存state_level文件到相对路径os.path -> finished -> State Level
    filename = f"{state}.xlsx"
    file_path = os.path.join("finished", "State Level", filename)

    # Check if the file already exists
    file_exists = os.path.isfile(file_path)

    # Write the DataFrame to the file
    if file_exists:
        # Append the DataFrame to the existing file
        existing_data = pd.read_excel(file_path)
        existing_data = existing_data.append(state_level_df, ignore_index=True)
        existing_data.to_excel(file_path, index=False)
    else:
        state_level_df.to_excel(file_path, index=False)

load_data()