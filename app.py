# Import required libraries
import os
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from data.covid_get_raw_data import country_timeline_raw_data
from get_dashboards import get_timeline_dash, create_dropdown

#--------------------------------------------------------------

# Setup the app
app = dash.Dash(__name__)
server = app.server

#--------------------------------------------------------------

# Load data
df_timeline = country_timeline_raw_data()

#--------------------------------------------------------------

# Create country timeline dashboard
#fig1 = get_timeline_dash(df_timeline)

#--------------------------------------------------------------

# Define the app

app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                    html.Div(className='three columns div-user-controls',
                             children=[
                                 html.H2('DASH - STOCK PRICES'),
                                 html.P('Visualising time series with Plotly - Dash.'),
                                 html.P('Pick one or more stocks from the dropdown below.'),
                                 html.Div(
                                     className='div-for-dropdown',
                                     children=[
                                         dcc.Dropdown(id='my_dropdown', options=create_dropdown(list(df_timeline['name'].unique())),
                                                      multi=False, value='All countries', clearable=True,
                                                      style={'backgroundColor': '#1E1E1E'}
                                                      ),
                                     ],
                                     style={'color': '#1E1E1E'})
                                ]
                             ),
                    html.Div(className='nine columns div-for-charts bg-grey',
                             children=[
                                 #dcc.Graph(id='fig1',config={'displayModeBar': False}, animate=True)
                                 dcc.Graph(id='fig1', animate=True)
                             ])
                              ])
        ]

)


#--------------------------------------------------------------

@app.callback(
    Output(component_id='fig1', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
    )

def update_graph(my_dropdown):
  return get_timeline_dash(df_timeline, my_dropdown)

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)