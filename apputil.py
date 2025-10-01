import plotly.express as px
import pandas as pd


#titanic_dataset = "train.csv"

titanic_dataset = "https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv"

titanic = pd.read_csv(titanic_dataset)

df = titanic

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


def family_groups(df):
    # 1. Create new column: family_size
    df["family_size"] = df["SibSp"] + df["Parch"] + 1

    # 2. Group by family_size and Pclass
    famgroup = (
        df.groupby(["family_size", "Pclass"])
          .agg(
              n_passengers=("PassengerId", "count"),
              avg_fare=("Fare", "mean"),
              min_fare=("Fare", "min"),
              max_fare=("Fare", "max"),
          )
          .reset_index()
          .sort_values(["Pclass", "family_size"])
    )
    print(famgroup)
    return famgroup #returns a table with results


# 4. last_names()retuens passenger name and count
def last_names(df):
    # Extract last name from Name column
    df["LastName"] = df["Name"].str.split(",").str[0].str.strip()
    # Count occurrences of each last name
    counts = df["LastName"].value_counts()
    return counts


# 5. plot addressing the questions
def visualize_families(summary):
    import plotly.express as px
    # Example: plot average fare by family size and class
    fig = px.bar(
        summary,
        x="family_size",
        y="avg_fare",
        color="Pclass",
        barmode="group",
        title="Average Fare by Family Size and Passenger Class"
    )
    return fig

# Added Older_passenger column
def determine_age_division(df):
    # Median age per class
    medians = df.groupby("Pclass")["Age"].median()

    # Map median ages back to passengers
    df["class_median_age"] = df["Pclass"].map(medians)

    # Boolean column
    df["Older_passenger"] = df["Age"] > df["class_median_age"]

    return df

# age division plot
def visualize_age_division(df):
    import plotly.express as px
    fig = px.histogram(
        df,
        x="Pclass",
        color="Older_passenger",
        barmode="group",
        title="Age Division by Passenger Class"
    )
    return fig
