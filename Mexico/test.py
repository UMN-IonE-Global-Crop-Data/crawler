import pandas as pd



# Load the Excel file, assuming header information starts properly from the third row
df = pd.read_excel('.\\downloads\\output.xlsx', header=1)
df = df.drop(index=0)

# Select the relevant columns and rename them for clarity
selected_columns = df[['Entidad', 'Distrito','Sembrada', 'Cosechada', 'Producción','Valor Producción (miles de Pesos)']]
selected_columns.columns = ['State', 'District', 'Sown Area (ha)', 'Harvested Area  (ha)', 'Production','Value of production']

selected_columns.insert(2, 'year', 2021)
selected_columns.insert(3, 'crop', 'corn')

# Display the first few rows of the cleaned dataframe
selected_columns.to_excel('.\\arranged\\arranged.xlsx',index=False)




