from merger import StateMerger, CountyMerger
from crawler import AreaCrawler, ProductionCrawler


def fetchData(dic):
    # area data
    area_crawler = AreaCrawler()
    area_state, area_county = area_crawler.fetch(dic)

    # production data
    prod_crawler = ProductionCrawler()
    prod_state, prod_county = prod_crawler.fetch(dic)

    # merge state
    if len(area_state) == 0 and len(prod_state) == 0:
        # no area and prod level data
        with open("missing_data.txt", "a+") as file:
            file.write(f"{dic['Program']}_State_{dic['Year']}_{dic["Commodity"]}\n")
    else:  
        state_merger = StateMerger()
        state_merger.merge(area_state, prod_state)

    # merge county
    if len(area_county) == 0 and len(prod_county) == 0:
        # no area and prod level data
        with open("missing_data.txt", "a+") as file:
            file.write(f"{dic['Program']}_County_{dic['Year']}_{dic["Commodity"]}")
    else:
        # merge county
        county_merger = CountyMerger()
        county_merger.merge(area_county, prod_county)
    