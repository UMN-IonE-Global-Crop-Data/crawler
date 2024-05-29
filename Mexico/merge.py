import pandas as pd
import glob
import os

def combine_excel_files(folder_path, output_file):
    # Create a list to hold dataframes
    all_data = []

    # Use glob to match the .xlsx files in the folder
    for file in glob.glob(os.path.join(folder_path, '*.xlsx')):
        # Read each Excel file into a DataFrame
        df = pd.read_excel(file)
        # Append the DataFrame to the list
        all_data.append(df)
    
    # Concatenate all dataframes into one
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Write the combined DataFrame to a new Excel file
    combined_df.to_excel(output_file, index=False)
    print(f"Combined file created at {output_file}")




def del_files(folder_path):
    #delete all the files in a folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)  # 删除文件
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')



# Example usage:
# folder_path = os.path.join(os.getcwd(),'downloads')  # Update this path
# output_file = os.path.join(os.getcwd(),'outputs','wheat(ornament).xlsx')
# combine_excel_files(folder_path, output_file)
# del_files(folder_path)
