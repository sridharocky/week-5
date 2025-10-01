import pandas as pd

# Load the Titanic dataset (adjust path if needed)
df = pd.read_csv("train.csv")

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
