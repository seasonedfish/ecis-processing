import pandas as pd

file_location: str = "STC_dx.json"

df: pd.DataFrame = pd.read_json(file_location)

# Separate data into columns
df = df.join(df["diagnosis"].apply(pd.Series))
df = df.drop(columns=["diagnosis", "P_MRN_ID", "E_ID"])
df["DIAG_DATE"] = pd.to_datetime(df["DIAG_DATE"])

# Create rows, one for each patient
rows = []
patient_ids: list = df.P_ID.unique()
for patient_id in patient_ids:
    rows.append([patient_id])
print(rows)

# Get earliest year and latest year
earliest_year: int = int(min(df.DIAG_DATE).strftime("%Y"))
latest_year: int = int(max(df.DIAG_DATE).strftime("%Y"))
