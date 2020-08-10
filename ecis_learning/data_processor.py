import pandas as pd
from typing import List


class DataProcessor:
    def __init__(self, df):
        self.Data = df

    def process_data(self, columns: List[str], suffix: str = ""):
        # Create rows for new DataFrame, one for each patient
        rows: List[list] = []
        patient_ids: List[str] = self.Data["patient_id"].unique()
        for patient_id in patient_ids:
            rows.append([patient_id])

        # Get earliest year and latest year
        earliest_year: int = int(min(self.Data["year"]))
        latest_year: int = int(max(self.Data["year"]))

        # Iterate through year intervals and add data to rows
        # Also get names of columns
        column_names: List[str] = ["patient_id"]
        for current_year in range(earliest_year, latest_year + 1, 2):
            column_names.append(
                f"{current_year}–{current_year + 1}_{suffix}"
                if current_year != latest_year
                else f"{latest_year}_{suffix}"
            )
            for row in rows:
                interval_df: pd.DataFrame = self.Data.query(
                    "patient_id == @row[0] and (year == @current_year or year == @current_year + 1)"
                )
                self.append_values(row, interval_df, columns)

        # NaN year case
        column_names.append(f"unknown_time_{suffix}")
        for row in rows:
            interval_df: pd.DataFrame = self.Data.query(
                "patient_id == @row[0] and year.isnull()"
            )
            self.append_values(row, interval_df, columns)
        return pd.DataFrame(rows, columns=column_names)

    @staticmethod
    def append_values(row, df, columns):
        if df.empty:
            row.append(None)
        else:
            result = (
                "#".join(map(str, values))
                for values in zip(
                    *(df[column] for column in columns)
                )
            )
            row.append("; ".join(result))
