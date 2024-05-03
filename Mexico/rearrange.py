import pandas as pd

class rearrange:
    def __init__(self, input_path):
        self.input_path = input_path
        self.df = None

    def rearranging(self):
        self.df = pd.read_excel(self.input_path, header=2)
        