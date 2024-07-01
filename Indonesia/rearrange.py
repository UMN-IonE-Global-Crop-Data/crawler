import os
import pandas as pd

# # Path to the folder containing the Excel files
# folder_path = os.path.join(os.getcwd(),"downloads","area")



####改这里的位置"area","production","harvest area"
#注意因为rearranged下你写了两个名字,没有harvest. 所以你需要这里也修改一下
input = "production"
# Load the original Excel file
folder_path = os.path.join(os.getcwd(),"downloads",input)
# set output path
output_path = os.path.join(os.getcwd(),"rearranged","production")
#list storing the empty files' name
empty_list = []

# Iterate over each file in the folder
for file in os.listdir(folder_path):
    if file.endswith('.xlsx'):
        file_path = os.path.join(folder_path, file)
    
    #get filename withour extension 
    #split the filename at each underscore
    name = os.path.splitext(file)[0]
    parts = name.split('_')

    data = pd.read_excel(file_path)

    # Remove the first column (No)
    data = data.iloc[:, 1:]
    # Remove the last row (total)
    data = data.iloc[:-1, :]

    if data.empty:
            empty_list.append(name)
            print(f"No data to process in {file}. Skipping...")
            continue

    # Melt the dataframe to change from wide to long format, using 'Lokasi' as the identifier
    long_format_data = data.melt(id_vars=['Lokasi'], var_name='Year', value_name=input)

    # Remove non-numeric year entries if present, ensuring 'Year' contains only numeric years
    long_format_data = long_format_data[long_format_data['Year'].apply(lambda x: x.isnumeric())]

    # Convert 'Year' to a numeric data type for correct ordering and display
    long_format_data['Year'] = pd.to_numeric(long_format_data['Year'])

    long_format_data.insert(2,"Cropnm",parts[0])
    long_format_data.insert(0,"Province",parts[2])
    long_format_data.rename(columns = {"Lokasi":"Location(Lokasi)","area": "Area(Ha)","production":"Production(Ton)"}, inplace=True)

    # Save the transformed data to a new Excel file
    new_file_path = os.path.join(output_path, file)
    long_format_data.to_excel(new_file_path, index=False)
    print(f"Data has been successfully saved to {new_file_path}.")
print(f"The number of empty data:{len(empty_list)}")
print(empty_list)

