import logging
import shutil
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
        return pd.read_csv(path, dtype=str)
    elif path.suffix in (".xlsx", ".xls"):
        return pd.read_excel(path, dtype=str)
    else:
        raise ValueError("Unsupported file type. Please provide a CSV or Excel file.")


def rename_files(
    data: pd.DataFrame,
    account_col: str = "Account",
    reference_col: str = "Reference",
    company_col: str = "Company",
    memo_col: str = "Memo",
    dry_run: bool = False,
):
    """
    Copies files to an 'output' directory with new names based on the provided DataFrame.
    """
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    required_columns = [account_col, reference_col, memo_col, company_col]
    if not all(col in data.columns for col in required_columns):
        logging.error(f"Missing one or more required columns in the input file: {required_columns}")
        return

    for _, row in data.iterrows():
        try:
            current_filepath = Path(row[memo_col])

            if not current_filepath.is_file():
                logging.warning(f"File not found: {current_filepath}")
                continue

            account = row[account_col]
            reference = row[reference_col]
            company = row[company_col]

            new_filename = f"{account}-{company}_{reference}".upper() + current_filepath.suffix.upper()
            new_filepath = output_dir / new_filename

            if dry_run:
                logging.info(f"[DRY RUN] Would copy {current_filepath} to {new_filepath}")
            else:
                shutil.copy(current_filepath, new_filepath)
                logging.info(f"Copied {current_filepath} to {new_filepath}")

        except Exception as e:
            logging.error(f"An error occurred while processing {current_filepath}: {e}")
