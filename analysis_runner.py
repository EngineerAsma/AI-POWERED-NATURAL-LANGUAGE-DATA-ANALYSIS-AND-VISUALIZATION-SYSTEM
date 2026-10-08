
import pandas as pd
import matplotlib.pyplot as plt

from src.question_analyzer import analyze_question

from src.analysis_engine import (
    total_sales,
    average_sales,
    sales_by_category,
    sales_by_region,
    profit_by_category,
    top_products_by_sales,
    monthly_sales,
    plot_sales_by_category,
    plot_sales_by_region,
    plot_profit_by_category,
    plot_top_products_by_sales,
    plot_monthly_sales
)


def create_explanation(question, result, operation, measure, group_by):
    """
    Creates a reliable explanation directly from the Pandas result.

    Pandas is the source of truth for all numerical values.
    """

    if isinstance(result, str):
        return result

    # --------------------------------------------------
    # AVERAGE
    # --------------------------------------------------

    if operation == "AVERAGE":

        value = float(result)

        return (
            f"The average {measure.lower()} is "
            f"${value:,.2f}."
        )

    # --------------------------------------------------
    # TOTAL / SUM
    # --------------------------------------------------

    if operation == "SUM":

        # Total without grouping
        if group_by is None:

            value = float(result)

            return (
                f"The total {measure.lower()} is "
                f"${value:,.2f}."
            )

        # Total grouped by category/region/etc.
        else:

            lines = []

            for name, value in result.items():

                lines.append(
                    f"- {name}: ${float(value):,.2f}"
                )

            return (
                f"Total {measure.lower()} by "
                f"{group_by.lower()}:\n\n"
                + "\n".join(lines)
            )

    # --------------------------------------------------
    # HIGHEST
    # --------------------------------------------------

    if operation == "MAX":

        name = result.index[0]
        value = float(result.iloc[0])

        return (
            f"The {group_by.lower()} with the highest "
            f"{measure.lower()} is {name}, with "
            f"${value:,.2f}."
        )

    # --------------------------------------------------
    # LOWEST
    # --------------------------------------------------

    if operation == "MIN":

        name = result.index[0]
        value = float(result.iloc[0])

        return (
            f"The {group_by.lower()} with the lowest "
            f"{measure.lower()} is {name}, with "
            f"${value:,.2f}."
        )

    # --------------------------------------------------
    # GROUP BY
    # --------------------------------------------------

    if operation == "GROUP_BY":

        lines = []

        for name, value in result.items():

            lines.append(
                f"- {name}: ${float(value):,.2f}"
            )

        return (
            f"{measure} by {group_by}:\n\n"
            + "\n".join(lines)
        )

    # --------------------------------------------------
    # TOP N
    # --------------------------------------------------

    if operation == "TOP_N":

        lines = []

        for name, value in result.items():

            lines.append(
                f"- {name}: ${float(value):,.2f}"
            )

        return (
            f"Top {len(result)} products by "
            f"{measure.lower()}:\n\n"
            + "\n".join(lines)
        )

    # --------------------------------------------------
    # TREND
    # --------------------------------------------------

    if operation == "TREND":

        highest_month = result.idxmax()
        highest_value = float(result.max())

        lowest_month = result.idxmin()
        lowest_value = float(result.min())

        return (
            f"Monthly {measure.lower()} ranged from "
            f"${lowest_value:,.2f} in {lowest_month} "
            f"to ${highest_value:,.2f} in {highest_month}. "
            f"The highest monthly {measure.lower()} occurred "
            f"in {highest_month}."
        )

    # --------------------------------------------------
    # FALLBACK
    # --------------------------------------------------

    return "The analysis was completed successfully."


def run_analysis(df, question):

    # --------------------------------------------------
    # UNDERSTAND USER QUESTION
    # --------------------------------------------------

    plan = analyze_question(question)

    operation = plan["operation"]
    measure = plan["measure"]
    group_by = plan["group_by"]
    n = plan["n"]

    result = None
    chart_type = None

    # --------------------------------------------------
    # 1. SALES BY CATEGORY
    # --------------------------------------------------

    if (
        operation == "GROUP_BY"
        and measure == "Sales"
        and group_by == "Category"
    ):

        result = sales_by_category(df)
        chart_type = "bar"

        plot_sales_by_category(df)

    # --------------------------------------------------
    # 2. SALES BY REGION
    # --------------------------------------------------

    elif (
        operation == "GROUP_BY"
        and measure == "Sales"
        and group_by == "Region"
    ):

        result = sales_by_region(df)
        chart_type = "bar"

        plot_sales_by_region(df)

    # --------------------------------------------------
    # 3. PROFIT BY CATEGORY
    # --------------------------------------------------

    elif (
        operation == "SUM"
        and measure == "Profit"
        and group_by == "Category"
    ):

        result = profit_by_category(df)
        chart_type = "bar"

        plot_profit_by_category(df)

    # --------------------------------------------------
    # 4. AVERAGE SALES
    # --------------------------------------------------

    elif (
        operation == "AVERAGE"
        and measure == "Sales"
    ):

        result = average_sales(df)
        chart_type = None

    # --------------------------------------------------
    # 5. TOTAL SALES
    # --------------------------------------------------

    elif (
        operation == "SUM"
        and measure == "Sales"
        and group_by is None
    ):

        result = total_sales(df)
        chart_type = None

    # --------------------------------------------------
    # 6. HIGHEST VALUE
    # --------------------------------------------------

    elif (
        operation == "MAX"
        and group_by is not None
        and measure is not None
    ):

        result = (
            df.groupby(group_by)[measure]
            .sum()
            .sort_values(ascending=False)
            .head(1)
        )

        chart_type = "bar"

        result.plot(kind="bar")

        plt.title(
            f"Highest {measure} by {group_by}"
        )

        plt.xlabel(group_by)
        plt.ylabel(measure)
        plt.tight_layout()

    # --------------------------------------------------
    # 7. LOWEST VALUE
    # --------------------------------------------------

    elif (
        operation == "MIN"
        and group_by is not None
        and measure is not None
    ):

        result = (
            df.groupby(group_by)[measure]
            .sum()
            .sort_values(ascending=True)
            .head(1)
        )

        chart_type = "bar"

        result.plot(kind="bar")

        plt.title(
            f"Lowest {measure} by {group_by}"
        )

        plt.xlabel(group_by)
        plt.ylabel(measure)
        plt.tight_layout()

    # --------------------------------------------------
    # 8. TOP N PRODUCTS
    # --------------------------------------------------

    elif (
        operation == "TOP_N"
        and measure == "Sales"
        and group_by == "Product Name"
    ):

        result = top_products_by_sales(
            df,
            n=n
        )

        chart_type = "barh"

        plot_top_products_by_sales(
            df,
            n=n
        )

    # --------------------------------------------------
    # 9. MONTHLY SALES TREND
    # --------------------------------------------------

    elif (
        operation == "TREND"
        and measure == "Sales"
    ):

        result = monthly_sales(df)
        chart_type = "line"

        plot_monthly_sales(df)

    # --------------------------------------------------
    # 10. UNSUPPORTED QUESTION
    # --------------------------------------------------

    else:

        result = (
            "Sorry, I cannot handle this question yet."
        )

        chart_type = None

    # --------------------------------------------------
    # CREATE RELIABLE EXPLANATION
    # --------------------------------------------------

    explanation = create_explanation(
        question,
        result,
        operation,
        measure,
        group_by
    )

    return (
        plan,
        result,
        chart_type,
        explanation
    )


# --------------------------------------------------
# TESTING
# --------------------------------------------------

if __name__ == "__main__":

    df = pd.read_csv(
        "data/superstore.csv"
    )

    questions = [
        "What are the sales by category?",
        "Which region has the highest sales?",
        "Which region has the lowest sales?",
        "Show total profit by category",
        "What is the average sales?",
        "Show the top 5 products by sales",
        "Show the monthly sales trend"
    ]

    print("\n" + "=" * 60)
    print("AI DATA ANALYST - ANALYSIS RUNNER")
    print("=" * 60)

    for question in questions:

        print("\nQuestion:")
        print(question)

        plan, result, chart_type, explanation = run_analysis(
            df,
            question
        )

        print("\nAnalysis Plan:")
        print(plan)

        print("\nResult:")
        print(result)

        print("\nChart Type:")
        print(chart_type)

        print("\nExplanation:")
        print(explanation)

        if chart_type is not None:
            plt.show()