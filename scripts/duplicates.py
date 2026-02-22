import pandas as pd

INPUT_FILE = "quickcart_data/clean_transactions.csv"
OUTPUT_FILE = "quickcart_data/duplicate_transactions.csv"


def find_duplicates():
    """
    Reads the clean transactions CSV and identifies all duplicate rows based on order_id.
    Outputs all occurrences of duplicates (including the first).
    """
    df = pd.read_csv(INPUT_FILE)
    
    # Find rows that are duplicated based on order_id
    duplicated_mask = df.duplicated(subset=['order_id'], keep=False)
    
    # Get all duplicate rows (including first occurrences)
    duplicates_df = df[duplicated_mask].sort_values(by=['order_id'])
    
    # Output results
    duplicates_df.to_csv(OUTPUT_FILE, index=False)
    
    print(f"Total rows in clean data: {len(df)}")
    print(f"Duplicate rows found: {len(duplicates_df)}")
    print(f"Unique duplicate groups: {len(duplicates_df) - duplicates_df.duplicated().sum()}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    find_duplicates()
