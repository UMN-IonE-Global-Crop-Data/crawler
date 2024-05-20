import pandas as pd
import os


# crops_in_spanish_capitalized = [
#     "Cebada" ('Cebada forrajera en verde','Cebada grano'), "Yuca"(didn't find cassava), 
#      "Maíz(Maíz grano, Elote,Maíz forrajero en verde)", "Colza/Mostaza", "Arroz",
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


# (1) barley(('Cebada forrajera en verde','Cebada grano')), (2) cassava(Yuca alimenticia), (3) maize(Maíz grano, Elote,Maíz forrajero en verde,Maíz palomero,Semilla de maíz grano), (4) rapeseed/canola and mustard (Colza/Canola/Canola forrajera and mostaza), 
# (5) rice(Arroz palay), (6) sorghum(Sorgo escobero,Sorgo forrajero en verde,Sorgo grano,Semilla de sorgo grano), (7) soybean(Soya,Semilla de soya), 
# (8) sugarcane(Caña de azúcar,Caña de azúcar otro uso(~for other uses),Semilla(seed) de caña de azúcar?), (9) wheat(Trigo ornamental,Trigo grano, Trigo forrajero verde,Semilla de trigo grano), 
# (10) oil palm("Palma africana o de aceite", Palma camedor(槟榔) ,Palma de ornato,Palma taco?), 
# (11) cotton(Algodón hueso(bone cotton)?), (12) potato(Papa,Semilla de papa), (13) groundnut(Cacahuate,Semilla de cacahuate), 

# (14) sweet potato(Camote), (15) sugar beet(Remolacha azucarera),  (16) millet (group) (Mijo,Mijo forrajero verde), 
# (17) coconut (Coco fruta), (18) beans (group) (Frijol,Frijol forrajero, Frijol x pelón?), (19) oat (Avena forrajera en verde,Avena grano,Semilla de avena grano), 

# (20) sunflower(Girasol , Girasol forrajero, Semilla de girasol), (21) banana(Plátano), (22) rubber(Hule hevea), (23) tea(Té limón?), (24) tomato(Tomate rojo (jitomate), Tomate verde), (25) onion(Cebolla)


def input_gen(crop, states = ["Nacional"], years = list(range(1980, 2023))):
    data = []
    for state in states:
        for year in years:
            data.append([state, year,crop])
    df = pd.DataFrame(data, columns=['State', 'Year', 'Crop'])
    print(df.head())
    download_path = os.path.join(os.getcwd(),"input.xlsx")
    df.to_excel(download_path,index=False)


#input_gen(crop = "Cebolla")
input_gen(states=["Sub"], crop = "Maíz grano",years=list(range(2009,2023)))


