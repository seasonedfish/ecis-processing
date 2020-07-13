import pandas as pd

file_input: str = "STC_dx.json"
file_output: str = "processed.csv"

df: pd.DataFrame = pd.read_json(file_input)

# Separate data into columns
df = df.join(df["data"].apply(pd.Series))
df["YEAR"] = pd.to_numeric(df["DIAG_DATE"].str.slice(0, 4))
df = df.drop(columns=["data", "P_MRN_ID", "E_ID", "DIAG_DATE"])

# Create rows for new DataFrame, one for each patient
rows = []
patient_ids: list = df.P_ID.unique()
for patient_id in patient_ids:
    rows.append([patient_id])

# Get earliest year and latest year
earliest_year: int = min(df.YEAR)
latest_year: int = max(df.YEAR)

column_names = ["P_ID"]
# Iterate through year intervals
current_year: int = earliest_year
while current_year <= latest_year:
    column_names.append(str(current_year) + "–" + str(current_year + 1)
                        if current_year != latest_year
                        else str(latest_year))
    for row in rows:
        interval_diagnoses: pd.DataFrame = df.query("P_ID == @row[0]"
                                                    "and (YEAR == @current_year or YEAR == @current_year + 1)")
        if interval_diagnoses.empty:
            row.append(None)
        else:
            result = [str(code) + "⁠—" + str(name)
                      for code, name
                      in zip(interval_diagnoses["DX_CODE"], interval_diagnoses["DX_NM"])]
            row.append(";".join(result))
    current_year += 2

df_processed = pd.DataFrame(rows, columns=column_names)
print("Done! Processed data saved to " + file_output)
df_processed.to_csv(file_output, index=False)
