from .data_processor import DataProcessor
import pandas as pd


class DiagnosisDataProcessor(DataProcessor):
    def __init__(self, json_file):
        df: pd.DataFrame = pd.read_json(json_file)
        df = df.join(df["data"].apply(pd.Series))
        df["YEAR"] = pd.DatetimeIndex(df["DIAG_DATE"]).year
        df = df.drop(columns=["data", "P_MRN_ID", "E_ID", "DIAG_DATE"])
        df.columns = ["dx_code", "year", "patient_id", "dx_name"]

        super().__init__(df)


