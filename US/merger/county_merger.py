import pandas as pd
import numpy as np

from merger.merger import Merger, EMPTY_DF




class CountyMerger(Merger):
    def __init__(self, input_dic) -> None:
        super().__init__(input_dic)
        self.level = "County"
        self.filename = f"County_{self.year}_{self.data_item}.csv"
    

    def merge(self, area_df: pd.DataFrame, prod_df: pd.DataFrame, yield_df: pd.DataFrame) -> None:
        area_prod_df = self.merge_area_prod(area_df, prod_df)
        area_prod_yield_df = self.merge_yield(area_prod_df, yield_df)

        if not area_prod_df.empty and not area_prod_yield_df.empty:
            self.save_file(area_prod_yield_df, self.filename, "County")


    def merge_area_prod(self, area_df: pd.DataFrame, prod_df: pd.DataFrame) -> pd.DataFrame:
        area_row = len(area_df)
        prod_row = len(prod_df)
        
        self.make_folder_structure()

        # census里面没有irr/non-irr production数据，直接返回
        if area_row != 0 and prod_row == 0:
            self.save_file(area_df, self.filename, self.level)
            return EMPTY_DF

        # guard clause, in case area_row is different from prod_row
        if area_row != prod_row:
            # should not save to file until finishing merge yield
            prod_header = ["Program", "State", "Ag District", "County", "Year", "Cropnm", "Area(Acre)"]
            gap_data = ["Program", "State", "Ag District", "County", "Year", "Cropnm", f"Production({self.prod_unit})"]
            gap = pd.DataFrame([gap_data], columns = prod_header)
            result_df = pd.concat([area_df, gap, prod_df], ignore_index=True)
            return result_df
        
        area_df[f"Production({self.prod_unit})"] = np.where((area_df.iloc[:, :-2] == prod_df.iloc[:, :-2]).all(axis=1), prod_df.iloc[:, -1], np.nan)

        return area_df


    def merge_yield(self, area_prod_df: pd.DataFrame, yield_df: pd.DataFrame) -> pd.DataFrame:
        area_prod_row = len(area_prod_df)
        yield_row = len(yield_df)


        # census里面没有irr/non-irr production数据，直接返回
        if area_prod_row != 0 and yield_row == 0:
            self.save_file(area_prod_df, self.filename, self.level)
            return EMPTY_DF
        

        # guard clause, in case area_row is different from prod_row
        if area_prod_row != yield_row:
            error_filename = f"error-{self.filename}"
            print(f"area, production, and yield have different rows, please check the file {error_filename} in the folder to fix the problem")
            
            # only data with same column header name will be aligned
            yield_header = ["Program", "State", "Ag District", "County", "Year", "Cropnm", "Area(Acre)"]
            gap_data = ["Program", "State", "Ag District", "County", "Year", "Cropnm", f"Yield({self.prod_unit} / Acre)"]
            gap = pd.DataFrame([gap_data], columns = yield_header)
            result_df = pd.concat([area_prod_df, gap, yield_df], ignore_index=True)

            result_df.to_csv(error_filename, index = False)
            return EMPTY_DF
        
        area_prod_df[f"Yield({self.prod_unit} / Acre)"] = np.where((area_prod_df.iloc[:, :-3] == yield_df.iloc[:, :-2]).all(axis=1), yield_df.iloc[:, -1], np.nan)

        return area_prod_df