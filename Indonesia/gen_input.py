import os
import pandas as pd
indonesian_crops_list = [
    'barley', 'singkong', 'jagung', 'kanola', 'mustar','padi',
    'sorgum', 'kedelai', 'tebu', 'gandum', 'kelapa sawit',
    'kapas', 'kentang', 'kacang tanah', 'ubi jalar', 'bit gula',
    'millet', 'kelapa', 'kacang', 'gandum', 'bunga matahari',
    'pisang', 'karet', 'teh', 'tomat', 'bawang merah'
]

        # List of provinces from the dropdown menu
provinces = [
            "Aceh", "Sumatera Utara","Sumatera Barat","Riau","Jambi","Sumatera Selatan","Bengkulu",
            "Lampung","Kepulauan Bangka Belitung","Kepulauan Riau","Daerah Khusus Ibukota Jakarta",
            "Jawa Barat","Jawa Tengah","Daerah Istimewa Yogyakarta","Jawa Timur","Banten","Bali",
            "Nusa Tenggara Barat","Nusa Tenggara Timur","Kalimantan Barat","Kalimantan Tengah","Kalimantan Selatan",
            "Kalimantan Timur","Kalimantan Utara","Sulawesi Utara","Sulawesi Tengah","Sulawesi Selatan","Sulawesi Tenggara",
            "Gorontalo","Sulawesi Barat","Maluku","Maluku Utara","Papua Barat","Papua"
        ]

  
#level = ["Nasional", "Provinsi", "Kabupaten"]
#indicator = ["LUAS PANEN","PRODUKSI","PRODUKTIVITAS"]

def input_gen(crop,indicator ="LUAS PANEN",subsection="Tanaman Pangan", level = "Kabupaten", start_year = 1970, end_year = 2024, sliced = None, provs = provinces):
        data = []
        if sliced is not None:
            provs = provs[provs.index(sliced):]
        for prov in provs:
            data.append([level, prov, crop,subsection,indicator, start_year, end_year])
        df = pd.DataFrame(data, columns=['Level', 'Province','Crop','Subsection','Indicator', 'Start Year', 'End Year'])
        print(df.head())
        download_path = os.path.join(os.getcwd(),"input.xlsx")
        df.to_excel(download_path,index=False)


input_gen(crop = "JAGUNG",sliced="Papua Barat")
# 确认crop,indictor,subsection
