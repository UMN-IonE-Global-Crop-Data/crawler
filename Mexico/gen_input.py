import pandas as pd
import os
states = ["Nacional"]

# crops_in_spanish_capitalized = [
#     "Cebada" ('Cebada forrajera en verde','Cebada grano'), "Yuca"(didn't find cassava), "Maíz(Maíz grano, Elote,Maíz forrajero en verde)", "Colza/Mostaza", "Arroz",
#     "Sorgo", "Soja", "Caña de Azúcar", "Trigo", "Palma de Aceite",
#     "Algodón", "Papa", "Maní", "Camote", "Remolacha Azucarera",
#     "Mijo", "Coco", "Frijoles", "Avena", "Girasol",
#     "Plátano", "Caucho", "Té", "Tomate", "Cebolla"
# ]

# states = ["Aguascalientes", "Baja California", "Baja California Sur", "Campeche",
#            "Coahuila", "Colima", "Chiapas", "Chihuahua", "Mexico City", "Durango", "Guanajuato",
#              "Guerrero", "Hidalgo", "Jalisco", "Mexico", "Michoacán", "Morelos", "Nayarit", "Nuevo Leon",
#                "Oaxaca", "Puebla", "Queretaro", "Quintana Roo", "San Luis Potosi", "Sinaloa", "Sonora",
#                  "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatan", "Zacatecas"]
years = list(range(1988, 2023))

data = []

for state in states:
    for year in years:
        data.append([state, year,'Mostaza'])


df = pd.DataFrame(data, columns=['State', 'Year', 'Crop'])

print(df.head())

download_path = os.path.join(os.getcwd(),"input.xlsx")
df.to_excel(download_path,index=False)
