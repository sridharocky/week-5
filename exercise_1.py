import pandas as pd
import plotly.express as px

titanic_dataset = "train.csv"

titanic = pd.read_csv(titanic_dataset)

print(titanic.columns)


def survival_demographics():
    """
    Analyze Titanic survival patterns by Pclass, Sex, and AgeGroup.

    Parameters:
        titanic_dataset (str): Path to Titanic dataset.

    Returns:
        pd.DataFrame: Summary of passengers, survivors, and survival rate.
    """
    # Load dataset
    df = pd.read_csv(titanic_dataset)

    # Column with categories of ages
    bins = [0, 12, 19, 59, 120]
    labels = ["Child", "Teen", "Adult", "Senior"]

    # 1. Create a categorical column named AgeGroup
    df["AgeGroup"] = pd.cut(df["Age"], bins=bins, labels=labels, right=True)

    # 2, 3, 4, 5 creates a groups and is easy to interpret
    summary = (
        df.groupby(["Pclass", "Sex", "AgeGroup"])
        .agg(
            n_passengers=("PassengerId", "count"),
            n_survivors=("Survived", "sum"),
            survival_rate=("Survived", "mean"),
        )
        .reset_index()
        .sort_values(["Pclass", "Sex", "AgeGroup"])
    )
    print(summary)
    return summary


def visualize_demographic(summary):
    """
    Create a Plotly chart showing Titanic survival demographics.

    Parameters:
        summary_df (pd.DataFrame): Output of survival_demographics()

    Returns:
        plotly.graph_objs._figure.Figure: Plotly figure object
    """
    fig = px.bar(
        summary,
        x="AgeGroup",
        y="survival_rate",
        color="Sex",
        barmode="group",
        facet_col="Pclass",
        facet_col_wrap=1,
        text="n_survivors",
        category_orders={"AgeGroup": ["Child", "Teen", "Adult", "Senior"]},
        labels={
            "survival_rate": "Survival Rate",
            "n_survivors": "Survivors",
            "Pclass": "Passenger Class",
        },
        title="Titanic Survival Rates by Demographics",
    )

    # Improve readability
    fig.update_traces(texttemplate="%{text}", textposition="outside")
    fig.update_layout(
        yaxis=dict(tickformat=".0%"),
        uniformtext_minsize=8,
        uniformtext_mode="hide",
        height=800
    )

    return fig

