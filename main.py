import pandas as pd
import argparse
import pathlib
import os

from ecis_learning import diagnoses
from ecis_learning import medications


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Process diagnosis and medication data."
    )
    parser.add_argument(
        "DIRECTORY",
        type=dir_path,
        help="Path to input directory")
    parser.add_argument(
        "-o",
        "--output",
        help="Output file name, defaults to 'processed.csv'",
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

    diagnoses_input = args.DIRECTORY / "Diagnoses" / "STC_dx.json"
    diagnoses_column_names, diagnoses_rows = diagnoses.process_data(
        json_file=diagnoses_input
    )

    allscripts_input = args.DIRECTORY / "Medications_Allscripts" / "STC_meds_alls_180710.json"
    epic_input = args.DIRECTORY / "Medications_EPIC" / "STC_meds_e_180710.json"
    soarian_input = args.DIRECTORY / "Medications_Soarian" / "STC_meds_soarian_180710.json"
    medications.process_data(
        allscripts_input, epic_input, soarian_input
    )

    # Create new DataFrame from rows and save to csv
    # df_processed: pd.DataFrame = pd.DataFrame(rows, columns=column_names)
    # df_processed.to_csv(args.output, index=False)
    print(f"Done! Processed data saved to {args.output}")


if __name__ == "__main__":
    main()
