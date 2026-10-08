
import pandas as pd
import matplotlib.pyplot as plt


def total_sales(df):
    return df["Sales"].sum()


def average_sales(df):
    return df["Sales"].mean()


def sales_by_category(df):
    result = (
        df.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    return result


def sales_by_region(df):
    result = (
        df.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    return result

def profit_by_category(df):

    result = (
        df.groupby("Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    return result

def top_products_by_sales(df, n=10):

    result = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )

    return result

def monthly_sales(df):

    df = df.copy()

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        format="%d-%m-%y"
    )

    result = (
        df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
        .sum()
    )

    result.index = result.index.astype(str)

    return result

def plot_sales_by_category(df):

    result = sales_by_category(df)

    plt.figure(figsize=(8, 5))

    result.plot(kind="bar")

    plt.title("Sales by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Sales")

    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.show()


def plot_sales_by_region(df):

    result = sales_by_region(df)

    plt.figure(figsize=(8, 5))

    result.plot(kind="bar")

    plt.title("Sales by Region")
    plt.xlabel("Region")
    plt.ylabel("Total Sales")

    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.show()

def plot_profit_by_category(df):

    result = profit_by_category(df)

    plt.figure(figsize=(8, 5))

    result.plot(kind="bar")

    plt.title("Profit by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Profit")

    plt.xticks(rotation=0)
    plt.tight_layout()

    plt.show()


def plot_top_products_by_sales(df, n=10):

    result = top_products_by_sales(df, n)

    plt.figure(figsize=(10, 6))

    result.sort_values().plot(kind="barh")

    plt.title(f"Top {n} Products by Sales")
    plt.xlabel("Total Sales")
    plt.ylabel("Product")

    plt.tight_layout()

    plt.show()

def plot_monthly_sales(df):

    result = monthly_sales(df)

    plt.figure(figsize=(12, 5))

    result.plot(kind="line", marker="o")

    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Sales")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":

    file_path = "data/superstore.csv"

    df = pd.read_csv(file_path)

    print("\n" + "=" * 60)
    print("ANALYSIS ENGINE")
    print("=" * 60)

    print(f"\nTotal Sales: {total_sales(df):,.2f}")

    print(f"Average Sales: {average_sales(df):,.2f}")

    print("\nSales by Category:")
    print("-" * 40)
    print(sales_by_category(df))

    print("\nSales by Region:")
    print("-" * 40)
    print(sales_by_region(df))

    print("\nDisplaying Sales by Category chart...")
    plot_sales_by_category(df)

    print("\nDisplaying Sales by Region chart...")
    plot_sales_by_region(df)

    print("\nProfit by Category:")
    print("-" * 40)
    print(profit_by_category(df))

    print("\nDisplaying Profit by Category chart...")
    plot_profit_by_category(df)

    print("\nTop 10 Products by Sales:")
    print("-" * 40)
    print(top_products_by_sales(df))

    print("\nDisplaying Top 10 Products by Sales chart...")
    plot_top_products_by_sales(df)

    print("\nMonthly Sales:")
    print("-" * 40)
    print(monthly_sales(df))

    print("\nDisplaying Monthly Sales Trend chart...")
    plot_monthly_sales(df)      

