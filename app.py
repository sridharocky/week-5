import streamlit as st
import pandas as pd
from apputil import (
    survival_demographics,
    visualize_demographic,
    family_groups,
    last_names,
    visualize_families,
    determine_age_division,
    visualize_age_division
)

# Load Titanic dataset once (optional, can also let functions use default)
titanic_dataset = "https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv"
df = pd.read_csv(titanic_dataset)
df.columns = df.columns.str.lower()  # standardize column names

##------------------------------------
## Exercise 1: Survival Demographics
##------------------------------------
summary = survival_demographics(df)
st.write("Exercise 1\n")
st.write("Did women in first class have a higher survival rate than men in other classes?")

# Show the summary table
st.dataframe(summary)

# Show the bar chart
fig = visualize_demographic(summary)
st.plotly_chart(fig)

##------------------------------------
## Exercise 2: Family Groups
##------------------------------------
summary_family = family_groups(df)
st.write("\nExercise 2\n")
st.write("Table with Passenger fare info")
st.dataframe(summary_family)

st.write(
    "1. Who is the single highest paying passenger? Was their fare unusually high for their class?\n"
    "2. Did large wealthy families still pay less per person than single wealthy travelers?"
)

# Plot families
fig_family = visualize_families(summary_family)
st.plotly_chart(fig_family)

# Last names analysis
st.write("Counts of last names:")
st.write(last_names(df))

##------------------------------------
## Bonus Question: Age Division
##------------------------------------
st.write("\nBonus Question\n")
st.write("Age division table")
df_age = determine_age_division(df)
st.dataframe(df_age[["pclass", "age", "older_passenger"]].head())

fig_age = visualize_age_division(df_age)
st.plotly_chart(fig_age)

# To run this app:
# streamlit run app.py
