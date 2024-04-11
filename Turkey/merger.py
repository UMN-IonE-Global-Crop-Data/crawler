import os
import pandas as pd

class Merger:

    def __init__(self):
        pass

    def merge(self, level, crop_type):
        path = os.path.join(os.getcwd(), "raw", level, crop_type)

        for item in os.listdir(path):
            self.merge_all_files(os.path.join(path, item), crop_type, level)

    def merge_all_files(self, target_dir, crop_type, level):
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)

            if os.path.isfile(item_path):
                self.generate_final_file(target_dir, crop_type, level)
                return

            elif os.path.isdir(item_path):
                self.merge_all_files(item_path, crop_type, level)

    def custom_sort(self, file_name, sequence):
        for index, item in enumerate(sequence):
            if item in file_name:
                return index
        return len(sequence)

    def generate_final_file(self, target_dir, crop_type, level):

        if crop_type == "fruits":
            self.generate_final_file_fruits(target_dir, crop_type, level)
            return

        file_names = os.listdir(target_dir)

        # 定义排序顺序
        sequence_order = ["Sown Area", "Harvest Area", "Production", "Yield"]

        # 按照自定义顺序对文件进行排序
        sorted_files = sorted(file_names, key=lambda x: self.custom_sort(x, sequence_order))

        column_header = ['Region Code', 'State', 'Year', 'Cropnm', 'Sown Area(Decare)', 'Harvest Area(Decare)',
                         'Prodution(Tonne)', 'Yield(Kilogramme/Decare)']

        res = None

        for i in range(len(sorted_files)):
            file = sorted_files[i]
            # 先读取sown area的file
            if i == 0:
                lines = []
                crop_name = file.split("_")[1].split(".")[0]

                print(os.path.join(target_dir, file))

                df = pd.read_excel(os.path.join(target_dir, file), header=None)

                # add values to the final result one by one
                col_num = df.shape[1]
                row_num = df.shape[0]

                # first round, we need sown_area
                for col in range(3, col_num):
                    for row in range(4, row_num):
                        new_line = [("", df.iloc[1, col], df.iloc[row, 2], crop_name, df.iloc[row, col], "", "", "")]
                        lines.append(pd.DataFrame(new_line, columns=column_header))

                res = pd.concat(lines, axis=0)

            else:
                df = pd.read_excel(os.path.join(target_dir, file), header=None)

                # add values to the final result one by one
                col_num = df.shape[1]
                row_num = df.shape[0]

                # first round, we need sown_area
                for col in range(3, col_num):
                    for row in range(4, row_num):
                        if i == 1:
                            res.loc[(res['Year'] == df.iloc[row, 2]) & (
                                        res['State'] == df.iloc[1, col]), "Prodution(Tonne)"] = df.iloc[row, col]
                        elif i == 2:
                            res.loc[(res['Year'] == df.iloc[row, 2]) & (
                                        res['State'] == df.iloc[1, col]), "Yield(Kilogramme/Decare)"] = df.iloc[
                                row, col]
                        elif i == 3:
                            res.loc[(res['Year'] == df.iloc[row, 2]) & (
                                        res['State'] == df.iloc[1, col]), "Harvest Area(Decare)"] = df.iloc[row, col]
        output_path = f".\\processed\\{level}\\{crop_type}"
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        res.to_csv(f"{output_path}\\{crop_name}.csv", index=False, encoding="utf-8-sig")

    def generate_final_file_fruits(self, target_dir, crop_type, level):
        file_names = os.listdir(target_dir)

        # 定义排序顺序
        sequence_order = ["Area Of Compact", "Number Of Bearing", "Number Of Non Bearing", 'Production', "Yield"]

        # 按照自定义顺序对文件进行排序
        sorted_files = sorted(file_names, key=lambda x: self.custom_sort(x, sequence_order))

        column_header = ['Region Code', 'State', 'Year', 'Cropnm', 'Area of Compact(Decare)',
                         "Number of Bearing Trees(Number)", "Number of Non Bearing Trees(Number)", 'Prodution(Tonne)',
                         'Yield(Kilogramme/Decare)']

        res = None

        for i in range(len(sorted_files)):
            file = sorted_files[i]
            # 先读取sown area的file
            if i == 0:
                lines = []
                crop_name = file.split("_")[1].split(".")[0]

                print(os.path.join(target_dir, file))

                df = pd.read_excel(os.path.join(target_dir, file), header=None)

                # add values to the final result one by one
                col_num = df.shape[1]
                row_num = df.shape[0]

                # first round, we need sown_area
                for col in range(3, col_num):
                    for row in range(4, row_num):
                        new_line = [
                            ("", df.iloc[1, col], df.iloc[row, 2], crop_name, df.iloc[row, col], "", "", "", "")]
                        lines.append(pd.DataFrame(new_line, columns=column_header))

                res = pd.concat(lines, axis=0)

            else:
                df = pd.read_excel(os.path.join(target_dir, file), header=None)

                # add values to the final result one by one
                col_num = df.shape[1]
                row_num = df.shape[0]

                # first round, we need sown_area
                for col in range(3, col_num):
                    for row in range(4, row_num):
                        if i == 1:
                            res.loc[(res['Year'] == df.iloc[row, 2]) & (
                                        res['State'] == df.iloc[1, col]), "Number of Bearing Trees(Number)"] = df.iloc[
                                row, col]
                        elif i == 2:
                            res.loc[(res['Year'] == df.iloc[row, 2]) & (
                                        res['State'] == df.iloc[1, col]), "Number of Non Bearing Trees(Number)"] = \
                            df.iloc[row, col]
                        elif i == 3:
                            res.loc[(res['Year'] == df.iloc[row, 2]) & (
                                        res['State'] == df.iloc[1, col]), "Prodution(Tonne)"] = df.iloc[row, col]
                        elif i == 4:
                            res.loc[(res['Year'] == df.iloc[row, 2]) & (
                                        res['State'] == df.iloc[1, col]), "Yield(Kilogramme/Decare)"] = df.iloc[
                                row, col]

        output_path = f".\\processed\\{level}\\{crop_type}"
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        res.to_csv(f"{output_path}\\{crop_name}.csv", index=False, encoding="utf-8-sig")


merger = Merger()