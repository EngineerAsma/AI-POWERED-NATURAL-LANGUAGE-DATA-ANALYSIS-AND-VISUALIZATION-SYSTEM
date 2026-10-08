import pandas as pd


def detect_date_columns(df):

    date_columns = []

    for column in df.columns:

        if df[column].dtype == "object":
            converted = pd.to_datetime(df[column], format="%d-%m-%y", errors="coerce")

    

            valid_ratio = converted.notna().mean()

            if valid_ratio >= 0.8:
                date_columns.append(column)

    return date_columns


def profile_data(df):

    print("\n" + "=" * 60)
    print("DATASET PROFILE")
    print("=" * 60)

    # --------------------------------------------------
    # 1. DATASET SIZE
    # --------------------------------------------------

    print("\n1. DATASET SIZE")
    print("-" * 40)

    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    # --------------------------------------------------
    # 2. NUMERICAL COLUMNS
    # --------------------------------------------------

    numerical_columns = df.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    print("\n2. NUMERICAL COLUMNS")
    print("-" * 40)

    print(numerical_columns)

    # --------------------------------------------------
    # 3. DATE COLUMNS
    # --------------------------------------------------

    date_columns = detect_date_columns(df)

    print("\n3. DATE COLUMNS")
    print("-" * 40)

    print(date_columns)

    # --------------------------------------------------
    # 4. CATEGORICAL COLUMNS
    # --------------------------------------------------

    categorical_columns = [
        column
        for column in df.select_dtypes(include=["object"]).columns
        if column not in date_columns
    ]

    print("\n4. CATEGORICAL COLUMNS")
    print("-" * 40)

    print(categorical_columns)

    # --------------------------------------------------
    # 5. MISSING VALUES
    # --------------------------------------------------

    print("\n5. MISSING VALUES")
    print("-" * 40)

    print(df.isnull().sum())

    # --------------------------------------------------
    # 6. DUPLICATES
    # --------------------------------------------------

    print("\n6. DUPLICATE ROWS")
    print("-" * 40)

    print(f"Duplicate rows: {df.duplicated().sum()}")

    # --------------------------------------------------
    # 7. NUMERICAL STATISTICS
    # --------------------------------------------------

    print("\n7. NUMERICAL STATISTICS")
    print("-" * 40)

    print(df[numerical_columns].describe())

    # --------------------------------------------------
    # 8. UNIQUE VALUES
    # --------------------------------------------------

    print("\n8. UNIQUE VALUES")
    print("-" * 40)

    for column in categorical_columns:

        print(
            f"{column}: "
            f"{df[column].nunique()} unique values"
        )

    # --------------------------------------------------
    # RETURN PROFILE
    # --------------------------------------------------

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "numerical_columns": numerical_columns,
        "date_columns": date_columns,
        "categorical_columns": categorical_columns,
        "missing_values": df.isnull().sum(),
        "duplicates": df.duplicated().sum()
    }


if __name__ == "__main__":

    file_path = "data/superstore.csv"

    df = pd.read_csv(file_path)

    profile_data(df)