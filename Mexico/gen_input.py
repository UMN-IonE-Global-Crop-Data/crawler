import pandas as pd
import os
states = ["National", "Aguascalientes", "Baja California", "Baja California Sur", "Campeche",
           "Coahuila", "Colima", "Chiapas", "Chihuahua", "Mexico City", "Durango", "Guanajuato",
             "Guerrero", "Hidalgo", "Jalisco", "Mexico", "Michoacán", "Morelos", "Nayarit", "Nuevo Leon",
               "Oaxaca", "Puebla", "Queretaro", "Quintana Roo", "San Luis Potosi", "Sinaloa", "Sonora",
                 "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatan", "Zacatecas"]
years = list(range(2010, 2023))

data = []

for state in states:
    for year in years:
        data.append([state, year, "Elote"])


df = pd.DataFrame(data, columns=['State', 'Year', 'Crop'])

print(df.head())

download_path = os.path.join(os.getcwd(),"input.xlsx")
df.to_excel(download_path,index=False)
