from abc import ABC, abstractmethod
from typing import List

import pandas as pd


class DataProcessor(ABC):
    """
    Class that processes medical data.
    """
    def __init__(self, df):
        self.data = df

    @abstractmethod
    def get_processed_data(self, columns: List[str], suffix: str = "") -> pd.DataFrame:
        """
        Returns a new, processed DataFrame from the DataProcessor's data.

        :param columns: which columns to get values from
        :param suffix: string that is appended to the end of each new column
        """
        pass
