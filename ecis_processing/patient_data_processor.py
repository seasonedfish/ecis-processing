from typing import List

import pandas as pd

from .data_processor import DataProcessor


class PatientDataProcessor(DataProcessor):
    """
    Class that processes note data
    """

    def __init__(self, json_file):
        """
        Initializes a NoteDataProcessor from json input

        :param json_file: path to json file containing note data
        """
        df: pd.DataFrame = pd.read_json(json_file)
        df = df.join(df["data"].apply(pd.Series))
        df = df.filter(["Age", "P_ID", "P_GENDER", "P_RACE", "P_ETHNICITY"])

        df.columns = ["age", "patient_id", "gender", "race", "ethnicity"]

        super().__init__(df)

    def get_processed_data(self, columns: List[str], suffix: str = "") -> pd.DataFrame:
        pass


if __name__ == "__main__":
    my_pdp = PatientDataProcessor("tests/integration/fixtures/STC_EHR/Patients/patients.json")
    print(my_pdp.data)
