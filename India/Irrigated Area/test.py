import os
import pandas as pd

def convert_xls_to_xlsx():
    path = os.getcwd()
    for file in os.listdir(path):
        if file.endswith(".xls"):
            filename = os.path.splitext(file)[0]  # 提取文件名（不包含扩展名）
            xls_filepath = os.path.join(path, file)  # .xls 文件的完整路径

            # 使用 pandas 读取 .xls 文件
            df = pd.read_excel(xls_filepath, header = None)

            # 将 .xls 文件另存为 .xlsx 文件
            xlsx_filepath = os.path.join(path, f"{filename}.xlsx")
            df.to_excel(xlsx_filepath, index=False, header = None)

            # 删除原始 .xls 文件
            os.remove(xls_filepath)


def convert_xlsx_to_csv():
    path = os.getcwd()
    for file in os.listdir(path):
        if file.endswith(".xlsx"):
            filename = os.path.splitext(file)[0]  # 提取文件名（不包含扩展名）
            xlsx_filepath = os.path.join(path, file)  # .xlsx 文件的完整路径

            # 使用 pandas 读取 .xlsx 文件
            df = pd.read_excel(xlsx_filepath, header = None)

            # 将 DataFrame 数据保存为 .csv 文件
            csv_filepath = os.path.join(path, f"{filename}.csv")
            df.to_csv(csv_filepath, index=False, header = None)

            # 删除原始 .xlsx 文件
            os.remove(xlsx_filepath)

convert_xlsx_to_csv()