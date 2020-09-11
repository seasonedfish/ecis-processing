import pandas as pd

from .interval_data_processor import IntervalDataProcessor


class DiagnosisDataProcessor(IntervalDataProcessor):
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
        df["date"] = pd.to_datetime(df["DIAG_DATE"], errors="coerce")
        df = df.drop(columns=["data", "P_MRN_ID", "E_ID", "DIAG_DATE"])
        df.columns = ["dx_code", "patient_id", "dx_name", "date"]

        super().__init__(df)
