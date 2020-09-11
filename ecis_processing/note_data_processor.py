from typing import List

import pandas as pd

from .data_processor import DataProcessor


class NoteDataProcessor(DataProcessor):
    """
    Class that processes note data
    """

    def __init__(self, json_file, id_key: str, note_type_key: str, date_key: str, note_text_key: str):
        """
        Initializes a NoteDataProcessor from json input

        :param json_file: path to json file containing note data
        """
        df: pd.DataFrame = pd.read_json(json_file)
        df = df.join(df["data"].apply(pd.Series))

        if note_type_key is None:
            note_type_key = "note_type"
            df[note_type_key] = "radiology"

        df = df.filter([id_key, note_type_key, date_key, note_text_key])
        df[date_key] = pd.to_datetime(df[date_key], errors="coerce")

        df.columns = ["patient_id", "note_type", "date", "note_text"]

        super().__init__(df)

    def get_processed_data(self, columns: List[str], suffix: str = "") -> pd.DataFrame:
        processed = self.data.copy()
        processed["date"] = processed["date"].dt.strftime("%Y-%m-%d")
        processed["data"] = processed[columns].apply(lambda row: "#@@#".join(row.values.astype(str)), axis=1)
        processed = processed.groupby("patient_id")["data"].apply("@@@@".join)

        return pd.DataFrame({"patient_id": processed.index, suffix: processed.values})

