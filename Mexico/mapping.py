import pandas as pd
import glob
import os

dict_Mex = {}
filepath = os.path.join(os.getcwd(),'sub_district_to_district_dict.txt')
with open(filepath, 'r',encoding='utf-8') as file:
    for line in file:
        if line.strip():  # Ensure that the line is not empty
            key, value = line.strip().split(': ')
            dict_Mex[key] = value

# Directory containing the Excel files
directory_path = os.path.join(os.getcwd(), 'outputs', 'sub-District Level')


# Process each Excel file in the directory
for excel_file in glob.glob(os.path.join(directory_path, '*.xlsx')):
    df = pd.read_excel(excel_file)

    # Get the file name without extension to use as 'crop' column value
    crop_name = os.path.splitext(os.path.basename(excel_file))[0]

    # Replace all values in 'crop' column with the file name without extension
    df['crop'] = crop_name

    # Insert a new column for 'district' by mapping 'sub-district' through the dictionary
    # Assuming 'sub-district' is in the second column, we add 'district' as the third column
    df.insert(1, 'District', df['Sub-District'].map(dict_Mex))

    # Save the updated DataFrame back to Excel in a separate 'updated_files' folder
    updated_directory = os.path.join(os.getcwd(), 'outputs', 'Dstrict-Sub')
    if not os.path.exists(updated_directory):
        os.makedirs(updated_directory)
    new_file_path = os.path.join(updated_directory, os.path.basename(excel_file))
    df.to_excel(new_file_path, index=False)

    # Check for unmapped 'Sub-District' entries where 'District' is NaN
    unmapped_sub_districts = df[df['District'].isna() & df['Sub-District'].notna()]
    if not unmapped_sub_districts.empty:
        print(f"Unmapped sub-districts in file {os.path.basename(excel_file)}:")
        print(unmapped_sub_districts['Sub-District'])
        break
    else: 
        print(f"{os.path.basename(excel_file)} is mapped:")

print("All files have been processed.")







