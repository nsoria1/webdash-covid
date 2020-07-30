# Import required libraries
import dash
import dash_html_components as html
import dash_core_components as dcc
from data.covid_get_raw_data import timeline_raw_data
import plotly.graph_objects as go

# Load data
df_timeline = timeline_raw_data()

# Scatter plot for total cases
fig = go.Figure()

# Add traces
fig.add_trace(go.Scatter(x=df_timeline['date'], y=df_timeline['deaths'],
                    mode='markers',
                    name='deaths'))

fig.add_trace(go.Scatter(x=df_timeline['date'], y=df_timeline['active'],
                    mode='lines+markers',
                    name='active'))

fig.add_trace(go.Scatter(x=df_timeline['date'], y=df_timeline['recovered'],
                    mode='lines',
                    name='recovered'))

fig.update_layout(template="plotly_dark", title="Total World Covid Cases", width=1060, height=400)

# Scatter plot for new cases
fig2 = go.Figure()

# Add traces
fig2.add_trace(go.Scatter(x=df_timeline['date'], y=df_timeline['new_deaths'],
                    mode='markers',
                    name='new deaths'))

fig2.add_trace(go.Scatter(x=df_timeline['date'], y=df_timeline['new_recovered'],
                    mode='lines+markers',
                    name='new recovered'))

fig2.add_trace(go.Scatter(x=df_timeline['date'], y=df_timeline['new_confirmed'],
                    mode='lines',
                    name='new confirmed'))

fig2.update_layout(template="plotly_dark", title="New World Covid Cases", width=1060, height=400)

# Initialise the dash app
app = dash.Dash(__name__)

# Responsive dashboards
app = dash.Dash(
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)

# Define the app
app.layout = html.Div(children=[
                      html.Div(className='row',  # Define the row element
                               children=[
                                 html.Div(className='three columns div-user-controls',  # Define the left element
                                 children=[
                                      html.H2('Dash - STOCK PRICES'),
                                      html.P('''Visualising time series with Plotly - Dash'''),
                                      html.P('''Pick one or more stocks from the dropdown below.''')]),
                                  html.Div(className='nine columns div-for-charts bg-grey',  # Define the right element
                                  children=[
                                    dcc.Graph(id='timeseries1', config={'displayModeBar': False}, animate=True, figure=fig),
                                    dcc.Graph(id='timeseries2', config={'displayModeBar': False}, animate=True, figure=fig2),
                                  ])
                                ])
                                ]
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)