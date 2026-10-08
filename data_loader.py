import pandas as pd


def load_data(file_path):
    df = pd.read_csv(file_path)

    print("\n" + "=" * 60)
    print("DATASET LOADED SUCCESSFULLY")
    print("=" * 60)

    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    return df


if __name__ == "__main__":
    file_path = "data/superstore.csv"

    df = load_data(file_path)