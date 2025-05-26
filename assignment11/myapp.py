import plotly.data as pldata
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

df = px.data.gapminder()

# Get unique countries
countries = df["country"].drop_duplicates()


# Initialize Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div(
    [
        dcc.Dropdown(
            id="country-dropdown",
            options=[{"label": country, "value": country} for country in countries],
            value="Canada",  # Default county
        ),
        dcc.Graph(id="gdp-graph"),
    ]
)


# Callback for updating the graph based on selected country
@app.callback(Output("gdp-graph", "figure"), [Input("country-dropdown", "value")])
def update_graph(selected_country):
    filtered_df = df[df["country"] == selected_country]
    fig = px.line(
        filtered_df,
        x="year",
        y="gdpPercap",
        title=f"GDP per Capita Over Time: {selected_country}",
    )
    return fig


if __name__ == "__main__":
    app.run(debug=True)
    server = app.server
