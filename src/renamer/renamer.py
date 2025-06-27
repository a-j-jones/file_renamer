import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def read_data(filepath: str) -> pd.DataFrame:
    """
    Reads data from a CSV or Excel file into a pandas DataFrame.
    """
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {filepath}")

    if path.suffix == ".csv":
        return pd.read_csv(path)
    elif path.suffix in (".xlsx", ".xls"):
        return pd.read_excel(path)
    else:
        raise ValueError("Unsupported file type. Please provide a CSV or Excel file.")


def rename_files(
    data: pd.DataFrame,
    account_col: str = "Account",
    reference_col: str = "Reference",
    memo_col: str = "Memo",
    dry_run: bool = False,
):
    """
    Renames files based on the provided DataFrame.
    """
    required_columns = [account_col, reference_col, memo_col]
    if not all(col in data.columns for col in required_columns):
        logging.error(f"Missing one or more required columns in the input file: {required_columns}")
        return

    for _, row in data.iterrows():
        try:
            current_filepath = Path(row[memo_col])

            if not current_filepath.is_file():
                logging.warning(f"File not found: {current_filepath}")
                continue

            new_filename = f"{row[account_col]}-{row[reference_col]}".upper() + current_filepath.suffix.upper()
            new_filepath = current_filepath.with_name(new_filename)

            if dry_run:
                logging.info(f"[DRY RUN] Would rename {current_filepath} to {new_filepath}")
            else:
                current_filepath.rename(new_filepath)
                logging.info(f"Renamed {current_filepath} to {new_filepath}")

        except Exception as e:
            logging.error(f"An error occurred while processing {current_filepath}: {e}")
