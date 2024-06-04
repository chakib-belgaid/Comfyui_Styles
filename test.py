import pandas as pd

def csv_to_dict(filename):
    data = pd.read_csv(filename, quotechar='"')
    return data.to_dict('records')
from util import * 
x=csv_to_dict("styles/styles.csv")
print(x)