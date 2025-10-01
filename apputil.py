import pandas as pd
import plotly.express as px

# Dataset URL
titanic_dataset = "https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv"

# Load dataset once
titanic = pd.read_csv(titanic_dataset)

# Standardize column names
titanic.columns = titanic.columns.str.lower()


def survival_demographics(df=None):
    """
    Summarize Titanic survival by class, sex, and age group.
    If df is not provided, use default Titanic dataset.
    """
    if df is None:
        df = titanic.copy()
    else:
        df = df.copy()

    # Age groups
    bins = [0, 12, 19, 59, 120]
    labels = ["Child", "Teen", "Adult", "Senior"]
    df["agegroup"] = pd.cut(df["age"], bins=bins, labels=labels, right=True)

    # Group by pclass, sex, agegroup
    summary = (
        df.groupby(["pclass", "sex", "agegroup"], dropna=False)
        .agg(
            n_passengers=("passengerid", "count"),
            n_survivors=("survived", "sum")
        )
        .reset_index()
    )

    # Survival rate
    summary["survival_rate"] = summary["n_survivors"] / summary["n_passengers"]
    summary["survival_rate"] = summary["survival_rate"].fillna(0)

    # Make agegroup categorical
    summary["agegroup"] = pd.Categorical(summary["agegroup"], categories=labels, ordered=True)

    return summary


def visualize_demographic(summary):
    fig = px.bar(
        summary,
        x="agegroup",
        y="survival_rate",
        color="sex",
        barmode="group",
        facet_col="pclass",
        facet_col_wrap=1,
        text="n_survivors",
        category_orders={"agegroup": ["Child", "Teen", "Adult", "Senior"]},
        labels={
            "survival_rate": "Survival Rate",
            "n_survivors": "Survivors",
            "pclass": "Passenger Class",
        },
        title="Titanic Survival Rates by Demographics",
    )
    fig.update_traces(texttemplate="%{text}", textposition="outside")
    fig.update_layout(yaxis=dict(tickformat=".0%"), uniformtext_minsize=8, uniformtext_mode="hide", height=800)
    return fig


def family_groups(df=None):
    if df is None:
        df = titanic.copy()
    else:
        df = df.copy()

    df["family_size"] = df["sibsp"] + df["parch"] + 1

    summary = (
        df.groupby(["family_size", "pclass"])
        .agg(
            n_passengers=("passengerid", "count"),
            avg_fare=("fare", "mean"),
            min_fare=("fare", "min"),
            max_fare=("fare", "max"),
        )
        .reset_index()
        .sort_values(["pclass", "family_size"])
    )
    return summary


def last_names(df=None):
    if df is None:
        df = titanic.copy()
    else:
        df = df.copy()

    df["lastname"] = df["name"].str.split(",").str[0].str.strip()
    counts = df["lastname"].value_counts()
    return counts


def visualize_families(summary):
    fig = px.bar(
        summary,
        x="family_size",
        y="avg_fare",
        color="pclass",
        barmode="group",
        title="Average Fare by Family Size and Passenger Class"
    )
    return fig


def determine_age_division(df=None):
    if df is None:
        df = titanic.copy()
    else:
        df = df.copy()

    medians = df.groupby("pclass")["age"].median()
    df["class_median_age"] = df["pclass"].map(medians)
    df["older_passenger"] = df["age"] > df["class_median_age"]
    return df


def visualize_age_division(df=None):
    if df is None:
        df = titanic.copy()

    fig = px.histogram(
        df,
        x="pclass",
        color="older_passenger",
        barmode="group",
        title="Age Division by Passenger Class"
    )
    return fig
