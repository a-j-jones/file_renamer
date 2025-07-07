import argparse
from pathlib import Path

from renamer.renamer import read_data, rename_files


def main():
    """
    Main function to run the file renamer.
    """
    parser = argparse.ArgumentParser(description="Copy and rename files based on a CSV or Excel file.")
    parser.add_argument(
        "filepath", type=Path, help="Path to the CSV or Excel file containing the file renaming information."
    )
    parser.add_argument(
        "--account-col", default="Account", help="Name of the column containing the account information."
    )
    parser.add_argument(
        "--reference-col", default="Reference", help="Name of the column containing the reference information."
    )
    parser.add_argument(
        "--memo-col", default="Memo", help="Name of the column containing the memo (current file path)."
    )
    parser.add_argument(
        "--company-col", default="Company", help="Name of the column containing the memo (current file path)."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Simulate the renaming process without actually modifying any files."
    )
    args = parser.parse_args()

    data = read_data(str(args.filepath))
    rename_files(data, args.account_col, args.reference_col, args.memo_col, args.dry_run)


if __name__ == "__main__":
    main()
