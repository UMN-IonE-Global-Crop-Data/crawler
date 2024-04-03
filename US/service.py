from merger.state_merger import StateMerger
from merger.county_merger import CountyMerger
from crawler import AreaCrawler, ProductionCrawler, YieldCrawler


class Service:
    def __init__(self, input_dic) -> None:
        self.dic = self.clean_dic(input_dic)

        self.area_crawler = AreaCrawler(self.dic)
        self.prod_crawler = ProductionCrawler(self.dic)
        self.yield_crawler = YieldCrawler(self.dic)

        self.state_merger = StateMerger(self.dic)
        self.county_merger = CountyMerger(self.dic)


    def fetchData(self):
        # area data
        area_state, area_county = self.area_crawler.fetch()

        # production data
        prod_state, prod_county = self.prod_crawler.fetch()

        # yield data
        yield_state, yield_county = self.yield_crawler.fetch()

        # merge state
        if len(area_state) == 0 and len(prod_state) == 0:
            self.save_missing_data("State")
        else: 
            self.state_merger.merge(area_state, prod_state, yield_state)


        # merge county
        if len(area_county) == 0 and len(prod_county) == 0:
           self.save_missing_data("County")
        else:
            self.county_merger.merge(area_county, prod_county, yield_county)


    def clean_dic(self, input_dic) -> dict:
        crop = input_dic["Commodity"]
        year = int(input_dic["Year"])  # input will be set to float automatically
        source = input_dic["Program"]
        sector = input_dic["Sector"]
        group = input_dic["Group"]
        domain_desc = input_dic["Domain"]

        if input_dic["Data_item"] == "":
            data_item = crop
        else:
            data_item = crop + ", " + input_dic["Data_item"]

         # replace "&" with %26 so that it won't affect API url
        res_dic = {
            "Source" : source.replace("&", "%26"),
            "Sector" : sector.replace("&", "%26"),
            "Group" : group.replace("&", "%26"),
            "Commodity" : crop.replace("&", "%26"),
            "Domain" : domain_desc.replace("&", "%26"),
            "Year" : year,
            "Data_item": data_item.replace("&", "%26"),
            "Prod_unit" : input_dic["Prod_unit"].replace("&", "%26")
        }

        return res_dic
    

    def save_missing_data(self, level):
        with open("missing_data.txt", "a+") as file:
            file.write(f"{self.dic['Source']}_{level}_{self.dic['Year']}_{self.dic["Commodity"]}\n")