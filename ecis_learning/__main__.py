import pandas as pd

file_location: str = "STC_dx.json"

df = pd.read_json(file_location)

print(df)
