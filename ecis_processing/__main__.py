import argparse
import functools
import os
import pathlib
from typing import List

import pandas as pd

from .diagnosis_data_processor import DiagnosisDataProcessor
from .medication_data_processor import MedicationDataProcessor
from .note_data_processor import NoteDataProcessor
from .patient_data_processor import PatientDataProcessor


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="ecis-processing",
        description="Process diagnosis and medication data."
    )
    parser.add_argument(
        "DIRECTORY",
        type=dir_path,
        help="path to input directory"
    )
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
    diagnoses_df = my_diagnosis_data_processor.get_processed_data(
        ["dx_code", "dx_name"], "dx"
    )

    medications_inputs = [
        args.DIRECTORY / "Medications_Allscripts" / "STC_meds_alls_180710.json",
        args.DIRECTORY / "Medications_EPIC" / "STC_meds_e_180710.json",
        args.DIRECTORY / "Medications_Soarian" / "STC_meds_soarian_180710.json",
    ]
    my_medication_data_processor = MedicationDataProcessor(*medications_inputs)
    medications_df = my_medication_data_processor.get_processed_data(
        ["rx_name", "rx_code", "source", "rx_status"], "rx"
    )

    patients_input = args.DIRECTORY / "Patients" / "patients.json"
    my_patient_data_processor = PatientDataProcessor(patients_input)
    patients_df = my_patient_data_processor.data

    my_clinical_ndp = NoteDataProcessor(
        args.DIRECTORY / "Notes" / "stc_notes.json",
        "P_ID",
        "N_TYPE2",
        "DATE_OF_SERVIC",
        "NOTE_TEXTS",
    )
    notes_df = my_clinical_ndp.get_processed_data(
        ["note_type", "date", "note_text"], suffix="clinical_note"
    )

    my_radiology_ndp = NoteDataProcessor(
        args.DIRECTORY / "Radiology" / "radiology_notes.json",
        "PATID",
        None,
        "NOTE_ENC_DATE",
        "NOTE_FULL_TEXT",
    )
    radiology_df = my_radiology_ndp.get_processed_data(
        ["note_type", "date", "note_text"], suffix="radiology_note"
    )

    # Create new DataFrame from rows and save to csv
    dfs: List[pd.DataFrame] = [
        diagnoses_df,
        medications_df,
        patients_df,
        notes_df,
        radiology_df,
    ]
    df_processed: pd.DataFrame = functools.reduce(
        lambda left, right: pd.merge(left, right, how="outer", on="patient_id"), dfs
    )
    df_processed = df_processed.set_index("patient_id")

    df_processed.to_csv(args.output)
    print(f"Done! Processed data saved to {args.output}")


if __name__ == "__main__":
    main()
