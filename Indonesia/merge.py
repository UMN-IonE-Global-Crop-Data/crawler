import pandas as pd
import glob
import os
from winsound import Beep


def clean_missing(raw,cropnm,province):
    """
    Rmove the columns that values are all zero, and write down the crop name, province and removed years in the 'missing years.txt'

    Parameters: 
    raw(DataFrame)
    cropnm(str)
    province(str)

    Return: DataFrame
    """
    
# Identify columns where all values are 0
    columns_all_zero = raw.columns[(raw == 0).all()].tolist()

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

def merge_cropnm(cropnm, directory_path,output_path):
    """
    Traverse through the folder and merge the excel files by cropnm, and export the file in a new folder
    """
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
    output_filename = os.path.join(output_path, f'{cropnm}.xlsx')
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

def outer_adjust(file_path):
    """
    remove the extra columns and complete the province columns
    """
    df = pd.read_excel(file_path)
    name = os.path.basename(file_path).split('.')[0] #get cropnm to fill in later

    #complete missing provinces:
    for index, row in df.iterrows():
        if pd.isna(row['Province_x']):
            if pd.isna(row['Province_y']):
                print("Row with missing Province_y:", row)
                break  # End the program after printing the row
            else:
                df.at[index, 'Province_x'] = row['Province_y']  # Fill Province_x with Province_y

    #drop/insert/rename columns
    df.drop(columns=['Cropnm_x','Cropnm_y','Province_y'],inplace=True)
    df.insert(2,'Cropnm',name)
    df.rename(columns={'Province_x':'Province'},inplace=True)

    return df










# output_path = os.path.join(os.getcwd(),'rearranged','by cropnm')
# path_area = os.path.join(os.getcwd(),'rearranged','by cropnm','area','*.xlsx')
# path_prod = os.path.join(os.getcwd(),'rearranged','by cropnm','production','*.xlsx')
# list_area = glob.glob(path_area)
# list_prod = glob.glob(path_prod)

#输入path
folder_path = os.path.join(os.getcwd(),'long cleaned','joined')
output_path = os.path.join(os.getcwd(),'long cleaned','final')
file_path = os.path.join(folder_path,'*.xlsx')
file_list = glob.glob(file_path)
for file in file_list:
    name = os.path.basename(file)
    #name1 = name.split('.')[0]
    #parts = name1.split('_')

    df = pd.read_excel(file)
    #输入你的函数

    #df = clean_missing(df, parts[0],parts[2])
    df=outer_adjust(file)

    df.to_excel(os.path.join(output_path,name),index=False)
    print(f"{name} is good")

Beep(1000,1000)


# # Join the productivity and final(previous)
# list_prod = glob.glob(os.path.join(folder_path,'productivity','*.xlsx'))
# list_fina = glob.glob(os.path.join(folder_path,'final','*.xlsx'))

# for file_l, file_r in zip(list_prod,list_fina):
#     name = os.path.basename(file_l)
#     cropnm = name.split('_')[0]
#     merged_df = big_join(file_l, file_r, id_columns = ['Location(Lokasi)', 'Year'])
#     merged_df.to_excel(os.path.join(output_path
#                                     ,f'{cropnm}.xlsx'), index = False)
#     print(f"Merge completed and saved to {cropnm}.xlsx")
# Beep(1000,1000)



# # get crop names in the folder
# crop_list = get_cropnmList(os.path.join(folder_path,'*.xlsx'))
# print(crop_list)
# print(folder_path)
# #Merge by crop name
# for crop in crop_list:
#     merge_cropnm(crop, folder_path,output_path)