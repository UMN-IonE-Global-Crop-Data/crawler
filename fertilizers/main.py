import time

import numpy as np
import pandas as pd
from selenium.webdriver import Chrome
import shutil
import config
import os

tables = config.tables
chrome_options = config.chrome_options

def rename_and_move_csv_files(directory, keyword, new_name):
    tim = time.time()
    while time.time()-tim < 5:
        # 创建csv文件夹
        csv_directory = os.path.join(directory, 'csv')
        os.makedirs(csv_directory, exist_ok=True)

        # 遍历当前目录下的文件
        for filename in os.listdir(directory):
            if filename.endswith('.csv') and keyword in filename:
                # 构造新的文件名
                new_filename = new_name.replace('/', '&') + '.csv'
                new_filename = new_filename.replace('"', '')

                # 源文件路径
                source_path = os.path.join(directory, filename)
                # 目标文件路径
                destination_path = os.path.join(csv_directory, new_filename)



                # 重命名文件并移动到csv文件夹
                shutil.move(source_path, destination_path)
                # print(f"已将文件'{filename}'重命名为'{new_filename}'并移动到csv文件夹。")
                return True
    else:
        return False



if __name__ == '__main__':
    # ds = [{
    #     'year': "2010-11",
    #     'state': "A & N ISLANDS",
    #     'district': None,
    #     "tehsil": None,
    #     "crop": "TOMATO"
    # }]

    # convert excel data to python dictionary 
    try:
        df = pd.read_excel('input.xlsx')
        df = df.replace({np.nan: None})
        keys = df.to_dict(orient='records')
    except Exception as er:
        print("incorrect excel input format!", er)

    # start crawling
    start_time = time.time()

    driver = Chrome(options=chrome_options)
    for key in keys:
        get_district(**key)
    
    end_time = time.time()
    print(end_time - start_time)
