import pandas as pd
import os

import infrastructure 

class Merger:
    def __init__(self) -> None:
        pass

    def merge(area_df: pd.DataFrame, prod_df: pd.DataFrame) -> None:
        pass

    
    def make_folder_structure(self):
        if not os.path.exists("CENSUS"):
            os.mkdir("CENSUS")
            os.mkdir("CENSUS/State_Level")
            os.mkdir("CENSUS/County_Level")
            os.mkdir("CENSUS/State_Level/total")
            os.mkdir("CENSUS/State_Level/irrigated")
            os.mkdir("CENSUS/State_Level/non-irrigated")

        if not os.path.exists("SURVEY"):
            os.mkdir("SURVEY")
            os.mkdir("SURVEY/State_Level")
            os.mkdir("SURVEY/County_Level")
            os.mkdir("SURVEY/State_Level/total")
            os.mkdir("SURVEY/State_Level/irrigated")
            os.mkdir("SURVEY/State_Level/non-irrigated")


class StateMerger(Merger):
    def __init__(self) -> None:
        pass
    
    def merge(self, area_df: pd.DataFrame, prod_df: pd.DataFrame) -> None:
        infrastructure.merge(area_df, prod_df, "State")


class CountyMerger(Merger):
    def __init__(self) -> None:
        pass
    
    def merge(self, area_df: pd.DataFrame, prod_df: pd.DataFrame) -> None:
        infrastructure.merge(area_df, prod_df, "County")

        # rowsA = len(area_df)
        # rowsB = len(prod_df)
        
        # length = area_df.shape[1]

        # self.make_folder_structure()

        # irr = ""
        # if "IRRIGATED" in data_item and "NON-IRRIGATED" not in data_item:
        #     irr = "-irr"
        # elif "NON-IRRIGATED" in data_item:
        #     irr = "-nonirr"


        # # census里面没有irr/non-irr production数据，直接返回
        # if rowsA != 0 and rowsB == 0:
        #     if level == "State":
        #         area.to_csv(f"{source}\\State_Level\\State_{area.iloc[0,2]}_{area.iloc[0,3]}{irr}.csv", index = False)
        #     elif level == "County":
        #         area.to_csv(f"{source}\\County_Level\\County_{area.iloc[0,4]}_{area.iloc[0,5]}{irr}.csv", index = False)
        #     return


        # # guard clause
        # if rowsA != rowsB:
        #     print(f"Producation and area have different rows, please check the file error{area.iloc[0,2]}_{area.iloc[0,3]}.csv in the folder to fix the problem")
        #     result_df = pd.concat([area, prod], ignore_index=True)
        #     result_df.to_csv(f"error{area.iloc[0,2]}_{area.iloc[0,3]}.csv", index = False)
        #     return
            

        # if rowsA == 0:
        #     print(f"{crop} in {year} at {level} not found")
        #     return

        # area[f"Production({prod_unit})"] = np.where((area.iloc[:, :-2] == prod.iloc[:, :-2]).all(axis=1), prod.iloc[:, -1], np.nan)
        # filename = ""
        # filepath = ""

        # # merge后length 变化了，需要重新计算
        # length = area.shape[1]

        # if length == 6:
        #     filename = f"State_{area.iloc[0,2]}_{area.iloc[0,3]}"
        #     filepath = os.path.join(f"{source}/State_Level", filename)
        
        # elif length == 8:
        #     filename = f"County_{area.iloc[0,4]}_{area.iloc[0,5]}"
        #     filepath = os.path.join(f"{source}/County_Level", filename)
        

        # filepath += f"{irr}.csv"
        # area.to_csv(filepath, index = False)