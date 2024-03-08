import pandas as pd
import infrastructure
from filter import state_filter, county_filter


class Crawler:
    def __init__(self) -> None:
        pass

class AreaCrawler(Crawler):
    def __init__(self) -> None:
        super().__init__()

    
    def fetch(self, dic: dict) -> list[pd.DataFrame]:
        data = infrastructure.fetch("area",dic)
        state = state_filter.filter(data)
        county = county_filter.filter(data)
        return [state,county]
    
class ProductionCrawler(Crawler):
    def __init__(self) -> None:
        super().__init__()


    def fetch(self, dic: dict) -> list[pd.DataFrame]:
        data =  infrastructure.fetch("production",dic)
        state = state_filter.filter(data)
        county = county_filter.filter(data)
        return [state,county]