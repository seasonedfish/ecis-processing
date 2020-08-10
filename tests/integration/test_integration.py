import filecmp
import os
import pytest


@pytest.fixture()
def stc_ehr_expected_output() -> str:
    return "tests/integration/fixtures/STC_EHR/processed.csv"


def test_integration(tmp_path, stc_ehr_expected_output):
    os.system(f"python -m ecis_processing tests/integration/fixtures/STC_EHR/ -o {tmp_path}/processed.csv")
    assert filecmp.cmp(f"{tmp_path}/processed.csv", stc_ehr_expected_output)
