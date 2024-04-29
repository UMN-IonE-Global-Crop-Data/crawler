import numpy as np
import pandas as pd
import os


def district_level(filename):
    # 读取excel文件作为dataframe，删除第一行和第二行
    # 读取时把第三行作为df的表头
    df = pd.read_excel(filename)
    df = df.replace({np.nan: None})
    df = df.iloc[2:]
    
    # 选取第1列，将所有格式为"\d+\.(.*)",的字符中间的内定替换为空样，并且删除空格替换后字符串最前面的空格
    df.iloc[:, 0] = df.iloc[:, 0].replace(r'\s\d+\.(.*)', r'\1', regex=True)


    # 把第4,5列移动到第5,6列
    df.iloc[:, 5] = df.iloc[:, 4]
    df.iloc[:, 4] = df.iloc[:, 3]

    # 记录下state名称
    state = df.iloc[0, 0]
    # 删除第一行
    df = df.iloc[1:]
    # 在第一列前插入新的一列，并且全部等于当前最左上角单元格的值
    df.insert(0, 'State', state)

    # 将表头修改为[State, District, Year, Season, Crop, Area(ha), Production(t)]
    df.columns = ['State', 'District', 'Year', 'Season', 'Crop', 'Area(ha)', 'Production(t)']

    # 填充取消合并单元格后残缺的District和Year
    df.iloc[:, [1, 2]] = df.iloc[:, [1, 2]].fillna(method='ffill')

    # 遍历每一行，如果该行的的第二列为含有“Total”,删除该行，并且更新i
    i = 0
    bound = len(df)
    while i < bound:
        # Total
        if 'Total' in df.iloc[i, 1]:
            df = df.drop(df.index[i])
            bound -= 1
        # Crop name
        elif df.iloc[i,3] == None and df.iloc[i,4] == None:
            crop = df.iloc[i,1]
            df = df.drop(df.index[i])
            bound -= 1
        # noraml cell
        else:
            df.iloc[i,4] = crop
            i += 1


    # 根据第Year列的大小从小到大排序，Year相同的，根据Crop排序
    df = df.sort_values(by=['Year', 'Crop'], ascending = True)

    # 将修改后的df保存到源文件中去
    df.to_excel(filename, index=False)



def state_level(filename):
    df = pd.read_excel(filename,header=None)
    df = df.replace({np.nan: None})
    year = df.iloc[5,1]
    df = df.iloc[3:]
    
    #移除产量列
    df = df.drop(5,axis = 1)
    i = 0
    while (i < len(df)):
        if i == 0:
            # 第一行
            state = df.iloc[i,0]
            crop = df.iloc[i+1,0]
            i += 1
        elif df.iloc[i,0] == None:
            # 合并单元格接触后出现空白行，如果检查是否含有Total会出现NULLpointer错误
            df = df.drop(df.index[i])
        elif 'Total' in df.iloc[i,0] and df.iloc[i,3] != None:
            # 遇到“Total - crop" 行，reformate
            # 并且更新crop，因为下一行就是新的crop
            df.iloc[i,0] = state
            df.iloc[i,2] = crop
            # 条件检查到达最后一行，i+1会报错
            if (i + 1 == len(df)):
                break
            crop = df.iloc[i+1,0]
            i += 1
        elif df.iloc[i-1,0] == state and df.iloc[i,0] != None and df.iloc[i,3] == None and df.iloc[i+1,0] != None and df.iloc[i+1,3] == None:
            # 遇到新state，更新state，crop
            state = df.iloc[i,0]
            crop = df.iloc[i+1,0]
            df = df.drop(df.index[i])
        else:
            df = df.drop(df.index[i])
    
    df = df.drop(df.index[0],axis = 0)
    # 第二列全部填充为year
    df.iloc[:, 1] = year

    #设置表头
    df.columns = ['State', 'Year', 'Crop', 'Area(ha)', 'Production(t)']

    print(df)

    df.to_excel(filename, index=False)


# 遍历当前文件夹下的所有文件，获取其中excel文件的文件名，然后是用load_and_clean函数处理
def main():
    path = os.listdir(os.getcwd())
    for filename in path:
        if filename.endswith('.xls'):
            state_level(filename)


main()