import pandas as pd
from typing import List

file_input: str = "STC_dx.json"
file_output: str = "processed.csv"

# Read json and separate data into columns to create initial DataFrame
df: pd.DataFrame = pd.read_json(file_input)
df = df.join(df["data"].apply(pd.Series))
df["YEAR"] = pd.DatetimeIndex(df["DIAG_DATE"]).year
df = df.drop(columns=["data", "P_MRN_ID", "E_ID", "DIAG_DATE"])

# Create rows for new DataFrame, one for each patient
rows: List[list] = []
patient_ids: List[str] = df.P_ID.unique()
for patient_id in patient_ids:
    rows.append([patient_id])

# Get earliest year and latest year
earliest_year: int = min(df.YEAR)
latest_year: int = max(df.YEAR)

# Iterate through year intervals and add data to rows
# Also get names of columns
column_names: List[str] = ["P_ID"]
for current_year in range(earliest_year, latest_year + 1, 2):
    column_names.append(
        f"{current_year}–{current_year + 1}"
        if current_year != latest_year
        else str(latest_year)
    )
    for row in rows:
        interval_diagnoses: pd.DataFrame = df.query(
            "P_ID == @row[0] and (YEAR == @current_year or YEAR == @current_year + 1)"
        )
        if interval_diagnoses.empty:
            row.append(None)
        else:
            result = [
                f"{code}⁠—{name}"
                for code, name in zip(
                    interval_diagnoses["DX_CODE"], interval_diagnoses["DX_NM"]
                )
            ]
            row.append(";".join(result))

# Create new DataFrame from rows and save to csv
df_processed: pd.DataFrame = pd.DataFrame(rows, columns=column_names)
print(f"Done! Processed data saved to {file_output}")
df_processed.to_csv(file_output, index=False)
