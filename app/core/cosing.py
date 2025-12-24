import csv
import pandas as pd


def load_cosing():
    return pd.read_csv("data/COSING_Ingredients-Fragrance Inventory_v2.csv",
                       encoding='utf-8',
                       engine='python',
                       on_bad_lines='skip',
                       quoting=csv.QUOTE_ALL,
                       sep=';',
                       dtype=str)


def find_ingredient(name, df):
    matches = df[df['INCI name'].str.contains(name, case=False, na=False)]

    # для дебага
    print(matches)

    if matches.empty:
        return None

    row = matches.iloc[0]
    return {
        "inci": row['INCI name'],
        "function": row['Function'],
        "desc": row['Chem/IUPAC Name / Description'],
        "restriction": row['Restriction']
    }