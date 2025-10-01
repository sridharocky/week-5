import streamlit as st
import pandas as pd
from apputil import survival_demographics, visualize_demographic, family_groups 
from apputil import last_names, visualize_families, determine_age_division, visualize_age_division

##------------------------------------
## Exercise 1
##------------------------------------

summary = survival_demographics()
st.write("Exercise 1\n")

# Pose your research question
st.write("Did women in first class have a higher survival rate than men in other classes?")

# Show the table
st.dataframe(summary)

# Show the chart
fig = visualize_demographic(summary)
st.plotly_chart(fig)
print(type(fig))

##------------------------------------
## Exercise 2
##------------------------------------

# Load data
titanic_dataset = "https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv"

df = pd.read_csv(titanic_dataset)




# Family groups summary
summary = family_groups(df)
st.write("\nExercise 2\n")
st.write("Table with Passenger fare info\n")
st.dataframe(summary)

st.write("1. Who is the single highest paying passenger? Was their fare unusually high for their class?\n"
         "2. Did large wealthy families still pay less per person than single wealthy travelers?")

# Plot families
fig = visualize_families(summary)
st.plotly_chart(fig)

# Last names analysis
st.write("Counts of last names:")
st.write(last_names(df))

##------------------------------------
## Bonus Question
##------------------------------------
st.write("\nBonus Question\n")
st.write("Age division table\n")
df = determine_age_division(df)
st.dataframe(df[["Pclass", "Age", "Older_passenger"]].head())

fig2 = visualize_age_division(df)
st.plotly_chart(fig2)


#To execute: run below command in cmd in the directory with aap.py
# streamlit run app.py