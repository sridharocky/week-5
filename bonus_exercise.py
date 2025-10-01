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
