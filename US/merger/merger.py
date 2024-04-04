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
            self.irr = "-non-irr"

    def merge(self, area_df: pd.DataFrame, prod_df: pd.DataFrame, yield_df: pd.DataFrame) -> None:
        pass

    def merge_area_prod(self, area_df: pd.DataFrame, prod_df: pd.DataFrame) -> pd.DataFrame:
        pass

    def merge_yield(self, area_prod_df: pd.DataFrame, yield_df: pd.DataFrame) -> pd.DataFrame:
        pass


    def make_folder_structure(self):
        if not os.path.exists("CENSUS"):
            os.mkdir("CENSUS")

            os.mkdir("CENSUS/total")
            os.mkdir("CENSUS/irrigated")
            os.mkdir("CENSUS/non-irrigated")

            os.mkdir("CENSUS/total/State_Level")
            os.mkdir("CENSUS/irrigated/State_Level")
            os.mkdir("CENSUS/non-irrigated/State_Level")

            os.mkdir("CENSUS/total/County_Level")
            os.mkdir("CENSUS/irrigated/County_Level")
            os.mkdir("CENSUS/non-irrigated/County_Level")


        if not os.path.exists("SURVEY"):
            os.mkdir("SURVEY")

            os.mkdir("SURVEY/total")
            os.mkdir("SURVEY/irrigated")
            os.mkdir("SURVEY/non-irrigated")

            os.mkdir("SURVEY/total/State_Level")
            os.mkdir("SURVEY/irrigated/State_Level")
            os.mkdir("SURVEY/non-irrigated/State_Level")

            os.mkdir("SURVEY/total/County_Level")
            os.mkdir("SURVEY/irrigated/County_Level")
            os.mkdir("SURVEY/non-irrigated/County_Level")


    def save_file(self, df, filename, level):


        if self.irr != "":
            filepath = f"{self.source}/{self.irr[1:]}igated/{level}_Level/{self.data_item}"
        else:
            filepath = f"{self.source}/total/{level}_Level/{self.data_item}"
        
        filename = filename.replace("%26", "&")
        filepath = filepath.replace("%26", "&")

        if not os.path.exists(filepath):
            os.mkdir(filepath)

        # the cropnm is default value, cannot distinguish one with another
        # df['Cropnm'] = self.data_item

        df.to_csv(f"{filepath}/{filename}", index = False)