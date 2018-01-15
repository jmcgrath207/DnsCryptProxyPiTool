import pandas as pd



class PandasServiceClass (object):

    def __init__(self):
        pass


    def DownloadCsvToPandasDF(self):
        url = "https://raw.githubusercontent.com/cs109/2014_data/master/countries.csv"
        c = pd.read_csv(url)