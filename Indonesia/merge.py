import pandas as pd
import glob
import os
from winsound import Beep

def clean_missing(raw,cropnm,province):
# Identify columns where all values are 0
    columns_all_zero = raw.columns[(df == 0).all()].tolist()

    # Remove these columns from the dataframe
    df_cleaned = raw.drop(columns=columns_all_zero)

    # Write the column names of the removed columns to a text file
    removed_columns_file = 'missing years.txt'
    with open(removed_columns_file, 'a') as file:
        file.write(f"\n{cropnm} {province}: \n")
        for column in columns_all_zero:
            file.write(f"{column} ")
    print(f"{cropnm} {province} is cleared")
    return(df_cleaned)


def get_cropnmList(folder_path):
    file_list = glob.glob(folder_path)
    cropnm_list = []
    for file in file_list:
        file_name = os.path.basename(file)
        cropnm = file_name.split('_')[0]
        if cropnm in cropnm_list:
            continue
        else:
            cropnm_list.append(cropnm)
    return(cropnm_list)

def merge(cropnm, directory_path,output_path):
    # Use glob to find all Excel files that start with "banana"
    file_pattern = os.path.join(directory_path, f'{cropnm}_*.xlsx')
    file_list = glob.glob(file_pattern)

    # Create a list to store DataFrames
    dfs = []

    # Iterate over the list of filenames
    for filename in file_list:
        # Read each Excel file into a DataFrame
        df = pd.read_excel(filename)
        # Append the DataFrame to the list
        dfs.append(df)

    # Concatenate all the DataFrames in the list into a single DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)

    # Save the combined DataFrame to a new Excel file
    output_filename = os.path.join(output_path, f'{cropnm}_area.xlsx')
    combined_df.to_excel(output_filename, index=False)

    print(f'Combined file saved as {output_filename}')


def big_join(pathL, pathR, id_columns = [], join_way = 'outer'):
    # Load the two Excel files

    # Read the Excel files into DataFrames
    df1 = pd.read_excel(pathL)
    df2 = pd.read_excel(pathR)

    # Specify the columns to join on
    join_columns = id_columns

    # Perform the join operation
    merged_df = pd.merge(df1, df2, on=join_columns, how=join_way)

    return merged_df

    # Save the merged DataFrame to a new Excel file
    #merged_df.to_excel('merged_file.xlsx', index=False)


#
def remove_zero(file_path):

    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_path)

    # Filter out rows where both column 'A' and 'B' are 0
    df_filtered = df[~((df['Production(Ton)'] == 0) & (df['Area(Ha)'] == 0))]

    return(df_filtered)








# output_path = os.path.join(os.getcwd(),'rearranged','by cropnm')
# path_area = os.path.join(os.getcwd(),'rearranged','by cropnm','area','*.xlsx')
# path_prod = os.path.join(os.getcwd(),'rearranged','by cropnm','production','*.xlsx')
# list_area = glob.glob(path_area)
# list_prod = glob.glob(path_prod)

#输入path
folder_path = os.path.join(os.getcwd(),'downloads','production')
output_path = os.path.join(os.getcwd(),'wide cleaned','production')
file_path = os.path.join(folder_path,'*.xlsx')
file_list = glob.glob(file_path)
#columns_to_delete = ['Unnamed: 0', 'Province_y','Cropnm_y']
for file in file_list:
    name = os.path.basename(file)
    name1 = name.split('.')[0]
    parts = name1.split('_')
    df = pd.read_excel(file)
    #输入你的函数
    df = clean_missing(df,parts[0],parts[2])
    #df.drop(columns=[col for col in columns_to_delete if col in df.columns], inplace=True)
    #df.rename(columns={'Province_x': 'Province','Cropnm_x':'Cropnm'},inplace=True)
    df.to_excel(os.path.join(output_path,name),index=False)
    print(f"{name} is good")

Beep(1000,1000)


## Join the production and area
# for file_l, file_r in zip(list_prod,list_area):
#     name = os.path.basename(file_l)
#     cropnm = name.split('_')[0]
#     merged_df = big_join(file_l, file_r, id_columns = ['Location(Lokasi)', 'Year'])
#     merged_df.to_excel(os.path.join(output_path,f'{cropnm}.xlsx'), index = False)
#     print(f"Merge completed and saved to {cropnm}.xlsx")
# Beep(1000,1000)



## get crop names in the folder
# crop_list = get_cropnmList(os.path.join(path_start,'*.xlsx'))
# print(crop_list)

##Merge by crop name
# for crop in crop_list:
#     merge(crop, path_start,path_end)