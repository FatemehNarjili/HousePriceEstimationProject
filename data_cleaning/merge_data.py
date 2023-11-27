import pandas as pd

mrestate_cleaned_data = pd.read_csv("../data/mrestate_cleaned.csv")
divar_cleaned_data = pd.read_csv("../data/divar_cleaned.csv")

data_concat = pd.concat(
    [mrestate_cleaned_data, divar_cleaned_data], ignore_index=True)

data_drop = data_concat.drop_duplicates(ignore_index=True)

data_drop.to_csv("../data/data_final.csv", index=False)
