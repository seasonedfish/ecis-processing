import pandas as pd
import numpy as np
from typing import List


def get_initial_df(
    json_file, time_key: str, id_key: str, name_key: str, code_key: str, status_key: str, source: str
) -> pd.DataFrame:
    """
    Extract medication data from json into an initial, unprocessed DataFrame.

    :param json_file: the json file to read
    :param time_key: the key of the time key/value pair
    :param id_key: the key of the patient id key/value pair
    :param name_key: the key of the medication name key/value pair
    :param code_key: the key of the medication code key/value pair
    :param status_key: the key of the status key/value pair
    :param source: the source of the data
    :return: initial DataFrame containing only relevant information
    """
    df: pd.DataFrame = pd.read_json(json_file)
    df = df.join(df["data"].apply(pd.Series))
    df[time_key] = pd.DatetimeIndex(df[time_key]).year

    df_new: pd.DataFrame = df[[time_key, id_key, name_key]].copy()
    df_new["code"] = df[code_key] if code_key is not None else "N/A"
    if status_key == "Active":
        # Special case for Epic data
        df_new["status"] = np.where(
            df["Active"] == "Active Medication", "Active", df["Status"]
        )
    elif status_key is not None:
        df_new["status"] = df[status_key]
    else:
        df_new["status"] = "N/A"
    df_new["source"] = source
    df_new.columns = ["time", "id", "name", "code", "status", "source"]
    return df_new


def process_data(allscripts_json_file, epic_json_file, soarian_json_file):
    df_allscripts = get_initial_df(
        allscripts_json_file,
        "LastUpDate",
        "PAT_ID",
        "MedicationName",
        "NDC",
        "MedStatus",
        "AS",
    )
    df_epic = get_initial_df(
        epic_json_file,
        "start_date",
        "P_ID",
        "Name",
        None,
        "Active",
        "E"
    )
    df_soarian = get_initial_df(
        soarian_json_file,
        "StartDateTime",
        "PAT_ID",
        "GenericDrugName",
        "DrugCode",
        None,
        "S",
    )

    df_combined = pd.concat([df_allscripts, df_epic, df_soarian], ignore_index=True)
    print(df_combined)

    # Create rows for new DataFrame, one for each patient
    rows: List[list] = []
    patient_ids: List[str] = df_combined["id"].unique()
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

    print(rows)
