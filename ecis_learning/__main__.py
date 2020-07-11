import pandas as pd

file_location: str = "STC_dx.json"

df: pd.DataFrame = pd.read_json(file_location)

# Separate data into columns
df = df.join(df["diagnosis"].apply(pd.Series))
df = df.drop(columns=["diagnosis", "P_MRN_ID", "E_ID"])
df["DIAG_DATE"] = pd.to_datetime(df["DIAG_DATE"])

# Get earliest year and latest year
earliest_year = int(min(df.DIAG_DATE).strftime("%Y"))
latest_year = int(max(df.DIAG_DATE).strftime("%Y"))


