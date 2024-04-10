import os
import pandas as pd
import shutil

class FileSaver:

    def __init__(self):
        pass

    def rename_and_move_file(self, level, crop_type):
        """This function renames and moves the downloaded file to the specified folder"""
        src_dir = os.path.join("C:", "Users", "wucha", "Downloads")
        for file in os.listdir(src_dir):
            if file.endswith(".xls"):
                df = pd.read_excel(os.path.join(src_dir, file), header=None)
                text = df.iloc[4, 1].split(" and ")

                data_type = text[0].replace('\xa0', ' ')

                crop_name_text = text[1]
                start_idx = crop_name_text.find('(') + 1
                end_idx = crop_name_text.rfind(')')

                crop_name = crop_name_text[start_idx:end_idx].replace("/", "_")

                print(f"rename file, original text {text[1]}, get crop name: {crop_name}")

                file_name = f"{data_type}_{crop_name}.xls"

                target_dir = os.path.join("raw", level, crop_type, crop_name)

                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                if os.path.exists(os.path.join(target_dir, file_name)):
                    print(f"{text} already exists")

                shutil.move(os.path.join(src_dir, file), os.path.join(target_dir, file_name))

    def save_missing_crop_data(self, level, content):
        file = open("missing_data.txt", "a", encoding="utf-8")
        file.write(f"{level},{content}\n")
        file.close()


file_saver = FileSaver()