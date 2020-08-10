import timeit

setup = """
import pandas as pd
from typing import List

file_input: str = "STC_dx.json"
file_output: str = "processed.csv"

# Read json and separate data into columns to create initial DataFrame
df: pd.DataFrame = pd.read_json(file_input)
df = df.join(df["data"].apply(pd.Series))
"""

print(
    min(
        timeit.Timer(
            'df["YEAR"] = pd.DatetimeIndex(df["DIAG_DATE"]).year', setup=setup
        ).repeat(7, 1000)
    )
)
