import pandas as pd
import os


EMPTY_DF = pd.DataFrame()

class Merger:
    def __init__(self, input_dic) -> None:
        self.source = input_dic["Source"]
        self.sector = input_dic["Sector"]
        self.group = input_dic["Group"]
        self.crop = input_dic["Commodity"]
        self.domain_desc = input_dic["Domain"]
        self.year = input_dic["Year"]
        self.data_item = input_dic["Data_item"]
        self.prod_unit = input_dic["Prod_unit"]

        self.irr = ""
        if "IRRIGATED" in self.data_item and "NON-IRRIGATED" not in self.data_item:
            self.irr = "-irr"
        elif "NON-IRRIGATED" in self.data_item:
            self.irr = "-nonirr"

    def merge(self, area_df: pd.DataFrame, prod_df: pd.DataFrame, yield_df: pd.DataFrame) -> None:
        pass

    def merge_area_prod(area_df: pd.DataFrame, prod_df: pd.DataFrame) -> pd.DataFrame:
        pass

    def merge_yield(self, area_prod_df: pd.DataFrame, yield_df: pd.DataFrame) -> pd.DataFrame:
        pass

    
    def make_folder_structure(self):
        if not os.path.exists("CENSUS"):
            os.mkdir("CENSUS")
            os.mkdir("CENSUS/State_Level")
            os.mkdir("CENSUS/County_Level")
            os.mkdir("CENSUS/State_Level/total")
            os.mkdir("CENSUS/State_Level/irrigated")
            os.mkdir("CENSUS/State_Level/non-irrigated")
            os.mkdir("CENSUS/County_Level/total")
            os.mkdir("CENSUS/County_Level/irrigated")
            os.mkdir("CENSUS/County_Level/non-irrigated")


        if not os.path.exists("SURVEY"):
            os.mkdir("SURVEY")
            os.mkdir("SURVEY/State_Level")
            os.mkdir("SURVEY/County_Level")
            os.mkdir("SURVEY/State_Level/total")
            os.mkdir("SURVEY/State_Level/irrigated")
            os.mkdir("SURVEY/State_Level/non-irrigated")
            os.mkdir("SURVEY/County_Level/total")
            os.mkdir("SURVEY/County_Level/irrigated")
            os.mkdir("SURVEY/County_Level/non-irrigated")

    def save_file(self, df, filename, level):
        if self.irr != "":
            filepath = f"{self.source}/{level}_Level/{self.irr[1:]}igated/{self.data_item}"
        else:
            filepath = f"{self.source}/{level}_Level/total/{self.data_item}"
        
        if not os.path.exists(filepath):
            os.mkdir(filepath)

        df.to_csv(f"{filepath}/{filename}", index = False)