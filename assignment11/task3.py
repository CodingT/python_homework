
import plotly.express as px
import plotly.data as pldata
import re

df = pldata.wind(return_type='pandas')

#print(f"First 10 lines: \n{df.head(10)}")
#print(f"\nLast 10 Lines: \n{df.tail(10)}")

df['strength_clean'] = df['strength'].str.replace(
    r'(\d+)-(\d+)', 
    lambda m: str((int(m.group(1)) + int(m.group(2))) / 2), 
    regex=True
)

df['strength_clean'] = df['strength_clean'].str.replace(
    r'(\d+)\+',
    lambda m: str(int(m.group(1)) + 0.5),
    regex=True
)

df['strength_clean'] = df['strength_clean'].astype(float)

#cleaned data
print(f"First 10 lines: \n{df.head(10)}")
print(f"\nLast 10 Lines: \n{df.tail(10)}")


# Create interactive scatter plot
fig = px.scatter(
    df,
    x='strength_clean',
    y='frequency',
    color='direction',
    title='Wind Strength vs Frequency by Direction',
    labels={'strength_clean': 'Wind Strength', 'frequency': 'Frequency'},
    hover_data=['direction', 'strength']
)

fig.show()