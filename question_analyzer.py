import re


def analyze_question(question):

    question = question.lower().strip()

    # --------------------------------------------------
    # 1. Detect the measure
    # --------------------------------------------------

    if "profit" in question or "profits" in question:
        measure = "Profit"

    elif "quantity" in question or "quantities" in question:
        measure = "Quantity"

    elif (
        "sales" in question
        or "sale" in question
        or "revenue" in question
    ):
        measure = "Sales"

    else:
        measure = "Sales"


    # --------------------------------------------------
    # 2. Detect grouping
    # --------------------------------------------------

    if "category" in question or "categories" in question:
        group_by = "Category"

    elif "region" in question or "regions" in question:
        group_by = "Region"

    elif "segment" in question or "segments" in question:
        group_by = "Segment"

    elif "product" in question or "products" in question:
        group_by = "Product Name"

    else:
        group_by = None


    # --------------------------------------------------
    # 3. Detect operation
    # --------------------------------------------------

    if (
        "highest" in question
        or "maximum" in question
        or "max" in question
        or "best" in question
    ):
        operation = "MAX"

    elif (
        "lowest" in question
        or "minimum" in question
        or "min" in question
        or "worst" in question
    ):
        operation = "MIN"

    elif "top" in question:
        operation = "TOP_N"

    elif (
        "average" in question
        or "mean" in question
        or "average value" in question
    ):
        operation = "AVERAGE"

    elif (
        "total" in question
        or "sum" in question
        or "how much" in question
    ):
        operation = "SUM"

    elif (
        "trend" in question
        or "monthly" in question
        or "over time" in question
    ):
        operation = "TREND"

    else:
        operation = "GROUP_BY"


    # --------------------------------------------------
    # 4. Detect TOP N number
    # --------------------------------------------------

    n = None

    if operation == "TOP_N":

        match = re.search(r"\btop\s+(\d+)", question)

        if match:
            n = int(match.group(1))

        else:
            n = 10


    # --------------------------------------------------
    # 5. Return analysis plan
    # --------------------------------------------------

    return {
        "operation": operation,
        "measure": measure,
        "group_by": group_by,
        "n": n
    }


# --------------------------------------------------
# TESTING
# --------------------------------------------------

if __name__ == "__main__":

    questions = [

        "What are the sales by category?",

        "How much revenue did each category generate?",

        "Give me sales for each region",

        "Which region has the highest sales?",

        "Which category performed best?",

        "What are the worst performing regions?",

        "Show the top 5 products by sales",

        "What is the average sales?",

        "Show total profit by category",

        "Show the monthly sales trend",

        "Show sales over time"

    ]

    print("\n" + "=" * 60)
    print("QUESTION ANALYZER")
    print("=" * 60)

    for question in questions:

        print("\nQuestion:")
        print(question)

        plan = analyze_question(question)

        print("Analysis Plan:")
        print(plan)