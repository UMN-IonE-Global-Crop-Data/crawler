import pandas as pd
import requests

from filter import state_filter, county_filter


class Crawler:
    def __init__(self, input_dic) -> None:
        self.api_key = "789AAD3D-2872-3A4D-87F5-59CB6B246889"
        self.source = input_dic["Source"]
        self.sector = input_dic["Sector"]
        self.group = input_dic["Group"]
        self.crop = input_dic["Commodity"]
        self.domain_desc = input_dic["Domain"]
        self.year = input_dic["Year"]
        self.data_item = input_dic["Data_item"]
        self.prod_unit = input_dic["Prod_unit"]


    def create_url(self):
        pass

    def query_API(self) -> list:
        url = self.create_url()
        response = requests.get(url)

        if response.status_code == 200:
            # convert the returned data to json
            data = response.json()['data']  
            return data
        elif response.status_code == 400:
            # no such data, query failed
            print(f"{url} not found")
            return []
        else:
            raise RuntimeError(f"This request for {self.crop} in {self.year} is incorrect, please go to the website to check all fields")

    def fetch(self) -> list[pd.DataFrame]:
        data =  self.query_API()
        state = state_filter.filter(data)
        county = county_filter.filter(data)
        return [state,county]


class AreaCrawler(Crawler):
    def __init__(self, input_dic) -> None:
         super().__init__(input_dic)

    def create_url(self) -> str:
        url = f"https://quickstats.nass.usda.gov/api/api_GET/?key={self.api_key}" \
        f"&source_desc={self.source}&sector_desc={self.sector}&group_desc={self.group}" \
        f"&commodity_desc={self.crop}&domain_desc={self.domain_desc}" \
        f"&year={self.year}&reference_period_desc=YEAR&format=JSON" \
        f"&short_desc={self.data_item} - ACRES HARVESTED"

        return url


class ProductionCrawler(Crawler):
    def __init__(self, input_dic) -> None:
        super().__init__(input_dic)

    def create_url(self) -> str:
        url = f"https://quickstats.nass.usda.gov/api/api_GET/?key={self.api_key}" \
        f"&source_desc={self.source}&sector_desc={self.sector}&group_desc={self.group}" \
        f"&commodity_desc={self.crop}&domain_desc={self.domain_desc}" \
        f"&year={self.year}&reference_period_desc=YEAR&format=JSON" \
        f"&short_desc={self.data_item} - PRODUCTION, MEASURED IN {self.prod_unit}"

        return url


class YieldCrawler(Crawler):
    def __init__(self, input_dic) -> None:
        super().__init__(input_dic)

    def create_url(self) -> str:
        url = f"https://quickstats.nass.usda.gov/api/api_GET/?key={self.api_key}" \
        f"&source_desc={self.source}&sector_desc={self.sector}&group_desc={self.group}" \
        f"&commodity_desc={self.crop}&domain_desc={self.domain_desc}" \
        f"&year={self.year}&reference_period_desc=YEAR&format=JSON" \
        f"&short_desc={self.data_item} - YIELD, MEASURED IN {self.prod_unit} / ACRE"

        return url