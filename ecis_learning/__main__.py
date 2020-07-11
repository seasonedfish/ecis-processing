import pandas as pd

file_location: str = "STC_dx.json"

df = pd.read_json(file_location)

# Separate data into columns
df = df.join(df["diagnosis"].apply(pd.Series))
df = df.drop(columns=["diagnosis", "P_MRN_ID", "E_ID"])
df["DIAG_DATE"] = pd.to_datetime(df["DIAG_DATE"])

print(df)
print(df.info(verbose=True))