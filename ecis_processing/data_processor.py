import pandas as pd
from typing import List


class DataProcessor:
    """
    Class that processes medical data.
    """

    def __init__(self, df):
        self.data = df

    def get_processed_data(self, columns: List[str], suffix: str = "") -> pd.DataFrame:
        """
        Returns a new, processed DataFrame from the DataProcessor's Data.

        :param columns: which columns to get values from
        :param suffix: string that is appended to the end of year ranges
        """
        # Create rows for new DataFrame, one for each patient
        rows: List[list] = []
        patient_ids: List[str] = self.data["patient_id"].unique()
        for patient_id in patient_ids:
            rows.append([patient_id])

        # Get earliest year and latest year
        earliest_year: int = int(min(self.data["year"]))
        latest_year: int = int(max(self.data["year"]))

        # Iterate through year intervals and add data to rows
        # Also get names of columns
        column_names: List[str] = ["patient_id"]
        for current_year in range(earliest_year, latest_year + 1, 2):
            column_names.append(
                f"{current_year}–{current_year + 1}_{suffix}"
                if current_year != latest_year
                else f"{latest_year}_{suffix}"
            )
            self.append_values(
                rows,
                f"patient_id == @row[0] and (year == {current_year} or year == {current_year} + 1)",
                columns,
            )

        # NaN year case
        column_names.append(f"unknown_time_{suffix}")
        self.append_values(rows, "patient_id == @row[0] and year.isnull()", columns)

        return pd.DataFrame(rows, columns=column_names)

    def append_values(self, rows: List[list], query: str, columns: List[str]) -> None:
        """
        Queries the Data with a boolean expression and appends the column values to every row.

        :param rows: rows to append to
        :param query: boolean expression to query the Data
        :param columns: which columns to get values from
        """
        for row in rows:
            interval_df: pd.DataFrame = self.data.query(query)

            if interval_df.empty:
                row.append(None)
            else:
                result = (
                    "#".join(map(str, values))
                    for values in zip(*(interval_df[column] for column in columns))
                )
                row.append("; ".join(result))
