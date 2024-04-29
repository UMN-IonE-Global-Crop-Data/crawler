import pandas as pd
import numpy as np
import os


# traverse all file under current directory
def read_file():
    path = os.getcwd()
    for file in os.listdir(path):
        if file.endswith(".csv"):
            print(file)
            rename_file(file,1)
    
    for file in os.listdir(path):
        if file.endswith(".csv"):
            print(file)
            rename_file(file,2)


def rename_file(file,option):
    df = pd.read_csv(file,header=None)
    # tehsil file
    if df.iloc[0][2] == "Textbox63":
        state = (df.iloc[1][2])[9:]
        district = (df.iloc[1][3])[11:]
        tehsil = (df.iloc[1][4])[9:]
    # district file
    elif df.iloc[0][2] == "Textbox12":
        state = (df.iloc[1][2])[8:]
        district = (df.iloc[1][3])[12:]
        tehsil = "all"
    elif df.iloc[0][2] == "Textbox56":
        state = (df.iloc[1][2])[9:].replace("                                               SOCIAL GROUP :    ALL SOCIAL GROUPS                                          NUMBER IN   ABSOLUTE UNITS                                     AREA IN   ABSOLUTE HECTARES","")
        district = "all"
        tehsil = "all"
    year = df.iloc[1][0][22:]
    crop = (df.iloc[1][1].replace("TABLE 6 B : ESTIMATED IRRIGATED AND UNIRRIGATED AREA BY SIZE CLASSES UNDER CROP","").strip())
    crop = crop.replace('/','&')
    new_name = year + "_" + state + "_" + district + "_" + tehsil + "_" + crop + ".csv"
    new_name = new_name.replace('"','')
    print(new_name)

    # 如果文件以结

    if option == 1:
        while True:
            try:
                os.rename(file, new_name)
                break
            except FileExistsError:
                # 如果已存在，给后面加上
                new_name = new_name.replace(".csv", "_1.csv")

    elif option == 2:
        try:
            os.rename(file, new_name)
        except FileExistsError:
            # 如果已存在，删除当前文件
            os.remove(file)

read_file()