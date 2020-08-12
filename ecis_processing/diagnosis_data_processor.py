import pandas as pd

from .data_processor import DataProcessor


class DiagnosisDataProcessor(DataProcessor):
    """
    Class that processes diagnosis data.
    """

    def __init__(self, json_file):
        """
        Initializes a DiagnosisDataProcessor from json input

        :param json_file: path to json file containing diagnosis data
        """
        df: pd.DataFrame = pd.read_json(json_file)
        df = df.join(df["data"].apply(pd.Series))
        df["YEAR"] = pd.to_datetime(df["DIAG_DATE"], errors="coerce").dt.year
        df = df.drop(columns=["data", "P_MRN_ID", "E_ID", "DIAG_DATE"])
        df.columns = ["dx_code", "patient_id", "dx_name", "year"]

        super().__init__(df)
