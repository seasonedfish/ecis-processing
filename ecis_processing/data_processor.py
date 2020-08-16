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
        df_new = self.data.copy()
        df_new["data"] = self.data[columns].apply(lambda row: "#".join(row.values.astype(str)), axis=1)

        nat_df = df_new.query("date.isnull()")
        nat_df = nat_df.groupby("patient_id")["data"].apply("; ".join)

        df_new = (df_new.groupby(["patient_id", pd.Grouper(freq="2Y", key="date")])
                  ["data"]
                  .apply("; ".join)
                  .unstack(fill_value=""))
        df_new.rename(columns=lambda date: f"{date.year - 1}-{date.year}_{suffix}", inplace=True)

        df_new[f"unknown_time_{suffix}"] = nat_df
        return df_new
