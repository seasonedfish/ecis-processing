import pandas as pd
from typing import List


def get_initial_diagnoses_df(json_file):
    """
    Read json and separate data into columns to create initial DataFrame
    :param json_file: input json file containing diagnoses data
    :return:
    """
    df: pd.DataFrame = pd.read_json(json_file)
    df = df.join(df["data"].apply(pd.Series))
    df["YEAR"] = pd.DatetimeIndex(df["DIAG_DATE"]).year
    return df.drop(columns=["data", "P_MRN_ID", "E_ID", "DIAG_DATE"])


def process_data(json_file):
    df_initial = get_initial_diagnoses_df(json_file)

    # Create rows for new DataFrame, one for each patient
    rows: List[list] = []
    patient_ids: List[str] = df_initial["P_ID"].unique()
    for patient_id in patient_ids:
        rows.append([patient_id])

    # Get earliest year and latest year
    earliest_year: int = min(df_initial["YEAR"])
    latest_year: int = max(df_initial["YEAR"])

    # Iterate through year intervals and add data to rows
    # Also get names of columns
    column_names: List[str] = ["P_ID"]
    for current_year in range(earliest_year, latest_year + 1, 2):
        column_names.append(
            f"DX{current_year}–{current_year + 1}"
            if current_year != latest_year
            else str(latest_year)
        )
        for row in rows:
            interval_diagnoses: pd.DataFrame = df_initial.query(
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

    return column_names, rows
