import pandas as pd




class Filter:
    def __init__(self) -> None:
        pass

    def myFilter(self, arr, level):
        result = []
        for ele in arr:
            if ele["agg_level_desc"] == level:
                result.append(ele)
        return result

    def filter(self, data: list) -> pd.DataFrame:
        pass


class StateFilter(Filter):
    def __init__(self) -> None:
        super().__init__()
        self.level = "STATE"

    def filter(self, data: list) -> pd.DataFrame:
        filteredData = self.myFilter(data, self.level)

        header = ["Program", "State", "Year", "Cropnm", "Area(Acre)"]
        df = pd.DataFrame(columns= header)
        for dp in filteredData:
            new_row = [dp['source_desc'], dp['state_name'], dp['year'], dp['commodity_desc'], dp['Value']]
            df.loc[len(df)] = new_row

        return df 
    
class CountyFilter(Filter):
    def __init__(self) -> None:
        super().__init__()
        self.level = "COUNTY"


    def filter(self, data: list) -> pd.DataFrame:
        filteredData = self.myFilter(data, self.level)
        
        header = ["Program", "State", "Ag District", "County", "Year", "Cropnm", "Area(Acre)"]
        df = pd.DataFrame(columns= header)
        for dp in filteredData:
            new_row = [dp['source_desc'], dp['state_name'], dp['asd_desc'], dp['county_name'], dp['year'], dp['commodity_desc'], dp['Value']]
            df.loc[len(df)] = new_row

        return df 
    

state_filter = StateFilter()
county_filter = CountyFilter()