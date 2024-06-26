import os
from constant import FIELD_TABLE_XPATH


class Config:
    def __init__(self, web_operator):
        self.web_operator = web_operator

    def set_up_everything(self):
        self.set_up_field_map()
        field_map = self.set_up_field_map()
        return field_map

    def set_up_field_map(self) -> dict:
        self.web_operator.reload_page_and_select_crop_type()

        table = self.web_operator.get_field_table()

        if len(table) == 3:
            data_field_xpath_map = {
                "sown_area": f"{FIELD_TABLE_XPATH}[2]/td/div",
                "production": f"{FIELD_TABLE_XPATH}[3]/td/div"
            }
        elif len(table) == 5:
            data_field_xpath_map = {
                "sown_area": f"{FIELD_TABLE_XPATH}[2]/td/div",
                "harvest_area": f"{FIELD_TABLE_XPATH}[3]/td/div",
                "yield": f"{FIELD_TABLE_XPATH}[4]/td/div",
                "production": f"{FIELD_TABLE_XPATH}[5]/td/div"
            }
        elif len(table) == 6:
            data_field_xpath_map = {
                "area_of_compact": f"{FIELD_TABLE_XPATH}[2]/td/div",
                "number_of_bearing": f"{FIELD_TABLE_XPATH}[3]/td/div",
                "number_of_non_bearing": f"{FIELD_TABLE_XPATH}[4]/td/div",
                "yield": f"{FIELD_TABLE_XPATH}[5]/td/div",
                "production": f"{FIELD_TABLE_XPATH}[6]/td/div"

            }

        return data_field_xpath_map

    def set_up_directory(self):
        cur_path = os.getcwd()
        download_path = os.path.join(cur_path, "/downloads")
        if not os.path.exists(download_path):
            os.mkdir(download_path)


