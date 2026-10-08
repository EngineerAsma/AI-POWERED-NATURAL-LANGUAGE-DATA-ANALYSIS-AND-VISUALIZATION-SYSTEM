import pandas as pd

from src.analysis_runner import run_analysis


# Load the dataset
df = pd.read_csv("data/superstore.csv")


print("\n" + "=" * 60)
print("AI DATA ANALYST")
print("=" * 60)

print("\nDataset loaded successfully!")
print(f"Rows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

print("\nYou can ask questions such as:")
print("- What are the sales by category?")
print("- Which region has the highest sales?")
print("- Show total profit by category")
print("- What is the average sales?")
print("- Show the top products by sales")
print("- Show the monthly sales trend")

print("\nType 'exit' to stop the program.")


while True:

    print("\n" + "-" * 60)

    question = input("Ask your question: ")

    if question.lower().strip() == "exit":
        print("\nAI Data Analyst stopped.")
        break

    plan, result, chart_type, explanation = run_analysis(df, question)

    print("\nAnalysis Plan:")
    print(plan)

    print("\nResult:")
    print(result)

    print("\nChart Type:")
    print(chart_type)

    print("\nAI Explanation:")
    print(explanation)