import os
import pandas as pd

# crops = {}
# filepath = os.path.join(os.getcwd(),'dict','food_crop.txt')
# with open(filepath, 'r',encoding='utf-8') as file:
#     for line in file:
#         if line.strip():  # Ensure that the line is not empty
#             key, value = line.strip().split(': ')
#             crops[key] = value


        # List of provinces from the dropdown menu
provinces = [
            "Aceh", "Sumatera Utara","Sumatera Barat","Riau","Jambi","Sumatera Selatan","Bengkulu",
            "Lampung","Kepulauan Bangka Belitung","Kepulauan Riau","Daerah Khusus Ibukota Jakarta",
            "Jawa Barat","Jawa Tengah","Daerah Istimewa Yogyakarta","Jawa Timur","Banten","Bali",
            "Nusa Tenggara Barat","Nusa Tenggara Timur","Kalimantan Barat","Kalimantan Tengah","Kalimantan Selatan",
            "Kalimantan Timur","Kalimantan Utara","Sulawesi Utara","Sulawesi Tengah","Sulawesi Selatan","Sulawesi Tenggara",
            "Gorontalo","Sulawesi Barat","Maluku","Maluku Utara","Papua Barat","Papua","Papua Barat Daya","Papua Selatan","Papua Tengah","Papua Pegunungan"
        ]

  
#level = ["Nasional", "Provinsi", "Kabupaten"]
#indicator = ["LUAS PANEN","PRODUKSI","PRODUKTIVITAS"] LUAS AREAL -> planatation


def input_gen(filepath, indicator ="LUAS PANEN",subsection="Tanaman Pangan", level = "Kabupaten", provs = provinces):
        crops = {}
        with open(filepath, 'r',encoding='utf-8') as file:
            for line in file:
                if line.strip():  # Ensure that the line is not empty
                    key, value = line.strip().split(': ')
                    crops[key] = value

        data = []
        for crop in crops.values():
            for prov in provs:
                data.append([level, prov, crop,subsection,indicator, 1970, 2024])
        df = pd.DataFrame(data, columns=['Level', 'Province','Crop','Subsection','Indicator', 'Start Year', 'End Year'])
        print(df.head())
        download_path = os.path.join(os.getcwd(),"input.xlsx")
        df.to_excel(download_path,index=False)

#
input_gen(os.path.join(os.getcwd(),'dict','plantation.txt'), indicator="PRODUKSI",subsection="Perkebunan") #"Perkebunan"




