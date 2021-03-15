import pandas as pd
from itertools import islice
import matplotlib.pyplot as plt


def pretty_print(KeyWord, Value):
    print("--------------------------------------------------------------------------------------------------------------------------------------------------")
    print(KeyWword)
    print(Value)
    print("__________________________________________________________________________________________________________________________________________________")

worldFootball = pd.read_csv("Es1_tabella.csv")