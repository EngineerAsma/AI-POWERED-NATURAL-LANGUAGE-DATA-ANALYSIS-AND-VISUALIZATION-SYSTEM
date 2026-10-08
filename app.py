import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.profiler import profile_data
from src.analysis_runner import run_analysis


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📊 AI Data Analyst")

st.write(
    "Natural Language Data Analysis & Visualization System"
)


# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

st.header("📂 Upload Dataset")

uploaded_file = st.file_uploader(
    "Upload a CSV or Excel file",
    type=["csv", "xlsx"]
)


# --------------------------------------------------
# LOAD DATASET
# --------------------------------------------------

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):

        df = pd.read_csv(uploaded_file)

    else:

        df = pd.read_excel(uploaded_file)


    st.success("Dataset loaded successfully! 🎉")


    # --------------------------------------------------
    # DATASET OVERVIEW
    # --------------------------------------------------

    st.header("📋 Dataset Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Rows",
            df.shape[0]
        )

    with col2:
        st.metric(
            "Columns",
            df.shape[1]
        )


    # --------------------------------------------------
    # DATA PREVIEW
    # --------------------------------------------------

    st.subheader("First 5 Rows")

    st.dataframe(
        df.head(),
        use_container_width=True
    )


    # --------------------------------------------------
    # DATA PROFILE
    # --------------------------------------------------

    st.header("🔍 Dataset Profile")

    profile = profile_data(df)


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Numerical Columns",
            len(profile["numerical_columns"])
        )

    with col2:
        st.metric(
            "Date Columns",
            len(profile["date_columns"])
        )

    with col3:
        st.metric(
            "Categorical Columns",
            len(profile["categorical_columns"])
        )


    # --------------------------------------------------
    # MISSING VALUES
    # --------------------------------------------------

    st.subheader("Missing Values")

    st.dataframe(
        profile["missing_values"],
        use_container_width=True
    )


    # --------------------------------------------------
    # DUPLICATE ROWS
    # --------------------------------------------------

    st.subheader("Duplicate Rows")

    st.write(
        profile["duplicates"]
    )


    # ==================================================
    # NATURAL LANGUAGE DATA ANALYSIS
    # ==================================================

    st.header("💬 Ask Your Data")

    question = st.text_input(
        "Ask a question about your dataset:",
        placeholder="Example: Which region has the highest sales?"
    )


    # --------------------------------------------------
    # ANALYZE
    # --------------------------------------------------

    if st.button("🔎 Analyze"):

        if question.strip() == "":

            st.warning(
                "Please enter a question."
            )

        else:
            plan, result, chart_type, explanation = run_analysis(df,question)

            


            # --------------------------------------------------
            # ANALYSIS PLAN
            # --------------------------------------------------

            st.subheader("🧠 Analysis Plan")

            st.json(plan)


            # --------------------------------------------------
            # RESULT
            # --------------------------------------------------

            st.subheader("📊 Result")

            if isinstance(result, str):

                st.warning(result)

            elif isinstance(result, (int, float)):

                st.metric(
                    "Answer",
                    f"{result:,.2f}"
                )

            else:

                st.dataframe(
                    result,
                    use_container_width=True
                )

            st.subheader("🤖 AI Explanation")

            st.write(explanation)


            # --------------------------------------------------
            # CHART
            # --------------------------------------------------

            if chart_type is not None:

                st.subheader("📈 Visualization")

                st.pyplot(plt.gcf(), clear_figure=False)