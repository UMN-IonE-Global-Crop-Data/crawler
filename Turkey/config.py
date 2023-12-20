


crop_type_map = {
        # "cereals" : "/html/body/div/div[1]/div/div[3]/div[2]/div[1]/div/div[3]/div[2]/table/tbody/tr/td/table/tbody/tr/td[1]/div/div[3]/table/tbody[1]/tr[2]/td[2]/div",
        # "vegetables" : "/html/body/div/div[1]/div/div[3]/div[2]/div[1]/div/div[3]/div[2]/table/tbody/tr/td/table/tbody/tr/td[1]/div/div[3]/table/tbody[1]/tr[3]/td[2]/div",
        "fruits" : "/html/body/div[1]/div[1]/div/div[3]/div[2]/div[1]/div/div[3]/div[2]/table/tbody/tr/td/table/tbody/tr/td[1]/div/div[3]/table/tbody[1]/tr[4]/td[2]/div",
        # "ornamentals" : "/html/body/div/div[1]/div/div[3]/div[2]/div[1]/div/div[3]/div[2]/table/tbody/tr/td/table/tbody/tr/td[1]/div/div[3]/table/tbody[1]/tr[5]/td[2]/div",
        # "irrigation" : "/html/body/div/div[1]/div/div[3]/div[2]/div[1]/div/div[3]/div[2]/table/tbody/tr/td/table/tbody/tr/td[1]/div/div[3]/table/tbody[1]/tr[10]/td[2]/div"
    }


table_xpath = "/html/body/div/div[1]/div/div[3]/div[2]/div[1]/div/div[4]/div[2]/div/div[1]/div[2]/div[3]/div[4]/table/tbody[1]/tr"

field_xpath_map = {
    "sown_area" : f"{table_xpath}[2]/td/div",
    "harvest_area" : "",
    "yield" : "",
    "production" : ""
    
}

levels = ["Turkey", "NUTS1", "NUTS2 (26 Regions)", "NUTS3 (Province Level)"]