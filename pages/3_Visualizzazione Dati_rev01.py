import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Path to the dataset
file_path = "data/1_Input_Dati_updated.csv"  # Update this to the actual path

# Load the data
@st.cache
def load_data():
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        st.error("File not found!")
        return pd.DataFrame()

df = load_data()

# Analytics Dashboard
st.title("Advanced Analytics Dashboard")

if df.empty:
    st.warning("No data available for analysis.")
else:
    # Menu for analytics
    menu = st.sidebar.radio(
        "Select an Analysis Type",
        [
            "Summary Statistics",
            "Correlations",
            "Group-Level Analysis",
            "Time-Based Trends",
            "Custom Metrics",
        ],
    )

    # 1. Summary Statistics
    if menu == "Summary Statistics":
        st.header("Summary Statistics")
        st.write(df.describe(include="all").T)
        st.write("**Missing Values:**")
        st.write(df.isnull().sum())

    # 2. Correlations
    elif menu == "Correlations":
        st.header("Correlations Between Numeric Columns")
        numeric_df = df.select_dtypes(include=["number"])
        if not numeric_df.empty:
            correlation_matrix = numeric_df.corr()
            st.write(correlation_matrix)

            fig = px.imshow(
                correlation_matrix,
                title="Correlation Heatmap",
                labels=dict(x="Features", y="Features", color="Correlation"),
                text_auto=True,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("No numeric data available for correlation analysis.")

    # 3. Group-Level Analysis
    elif menu == "Group-Level Analysis":
        st.header("Group-Level Analysis")
        group_column = st.selectbox("Select a Grouping Column", df.columns)
        value_column = st.selectbox("Select a Numeric Column for Aggregation", df.select_dtypes(include=["number"]).columns)

        group_stats = df.groupby(group_column)[value_column].agg(["mean", "sum", "count"]).reset_index()
        st.write(group_stats)

        fig = px.bar(
            group_stats,
            x=group_column,
            y="mean",
            title=f"Mean of {value_column} by {group_column}",
            labels={group_column: "Group", "mean": f"Mean {value_column}"},
        )
        st.plotly_chart(fig, use_container_width=True)

    # 4. Time-Based Trends
    elif menu == "Time-Based Trends":
        st.header("Time-Based Trends")

        # Ensure "Giorno" is in datetime format
        if "Giorno" in df.columns:
            df["Giorno"] = pd.to_datetime(df["Giorno"], errors="coerce")

            time_metric = st.selectbox(
                "Select a Metric for Time Analysis", df.select_dtypes(include=["number"]).columns
            )
            time_data = df.groupby("Giorno")[time_metric].mean().reset_index()

            fig = px.line(
                time_data,
                x="Giorno",
                y=time_metric,
                title=f"{time_metric} Over Time",
                labels={"Giorno": "Date", time_metric: "Metric Value"},
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("The dataset does not contain a 'Giorno' column.")

    # 5. Custom Metrics
    elif menu == "Custom Metrics":
        st.header("Custom Metrics")

        # Example: Calculate normalized satisfaction score
        if "Soddisfazione" in df.columns:
            df["Normalized Soddisfazione"] = (
                (df["Soddisfazione"] - df["Soddisfazione"].mean()) / df["Soddisfazione"].std()
            )
            st.write("Normalized Satisfaction Scores:")
            st.write(df[["Nome", "Soddisfazione", "Normalized Soddisfazione"]])

        # Example: Hobby diversity score
        if "Hobby" in df.columns:
            df["Hobby Count"] = df["Hobby"].apply(lambda x: len(x.split(" -- ")) if isinstance(x, str) else 0)
            st.write("Hobby Diversity Score:")
            st.write(df[["Nome", "Hobby", "Hobby Count"]])

        # Visualization of custom metrics
        fig = px.histogram(
            df,
            x="Normalized Soddisfazione" if "Normalized Soddisfazione" in df.columns else None,
            title="Distribution of Normalized Satisfaction",
        )
        st.plotly_chart(fig, use_container_width=True)

