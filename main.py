import pandas as pd
import argparse
import pathlib
import os

from ecis_learning.diagnosis_data_processor import DiagnosisDataProcessor
from ecis_learning.medication_data_processor import MedicationDataProcessor


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Process diagnosis and medication data."
    )
    parser.add_argument(
        "DIRECTORY",
        type=dir_path,
        help="path to input directory")
    parser.add_argument(
        "-o",
        "--output",
        help="output file name, defaults to 'processed.csv'",
        default="processed.csv",
    )
    return parser.parse_args()


def dir_path(path):
    if os.path.isdir(path):
        return pathlib.Path(path)
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid path")


def main():
    args = parse_arguments()
    diagnosis_input = args.DIRECTORY / "Diagnoses" / "STC_dx.json"
    my_diagnosis_data_processor = DiagnosisDataProcessor(diagnosis_input)
    diagnoses_df = my_diagnosis_data_processor.process_data()

    allscripts_input = args.DIRECTORY / "Medications_Allscripts" / "STC_meds_alls_180710.json"
    epic_input = args.DIRECTORY / "Medications_EPIC" / "STC_meds_e_180710.json"
    soarian_input = args.DIRECTORY / "Medications_Soarian" / "STC_meds_soarian_180710.json"
    my_medication_data_processor = MedicationDataProcessor(allscripts_input, epic_input, soarian_input)
    medications_df = my_diagnosis_data_processor.process_data()

    # Create new DataFrame from rows and save to csv
    # df_processed: pd.DataFrame = pd.DataFrame(rows, columns=column_names)
    # df_processed.to_csv(args.output, index=False)
    print(f"Done! Processed data saved to {args.output}")


if __name__ == "__main__":
    main()
