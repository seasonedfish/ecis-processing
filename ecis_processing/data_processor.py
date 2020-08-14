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
        Returns a new, processed DataFrame from the DataProcessor's data.

        :param columns: which columns to get values from
        :param suffix: string that is appended to the end of year ranges
        """
        return (self.data.groupby(["patient_id", pd.Grouper(freq="2Y", key="date")])
                .agg(lambda column: "#".join(column))
                .sum()
                .unstack(fill_value=""))

    @staticmethod
    def combine(df):
        df["value"] = "#".join([df["dx_code"], df["dx_name"]])
        return df

    def append_values(self, rows: List[list], query: str, columns: List[str]) -> None:
        """
        Queries the data with a boolean expression and appends the column values to every row.

        :param rows: rows to append to
        :param query: boolean expression to query the data
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
