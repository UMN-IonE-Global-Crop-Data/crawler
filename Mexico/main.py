import pandas as pd
import numpy as np
from service import Service
from merge import combine_excel_files, del_files
import os
import winsound

if __name__ == '__main__':
    df = pd.read_excel('input.xlsx')
    df = df.replace(np.nan, None)
    dict_list = df.to_dict(orient='records')

    print(dict_list)

    print('program starts')

    for dic in dict_list:
        service = Service(dic)
        service.start()
    
    folder_path = os.path.join(os.getcwd(),'downloads')  # Update this path
    output_file = os.path.join(os.getcwd(),'outputs','sunflower(forage)).xlsx')
    combine_excel_files(folder_path, output_file)
    del_files(folder_path)
        
    print("Program ends")
    winsound.Beep(900,1300)


