# Import required libraries
import dash
import dash_html_components as html

# Initialise the app
app = dash.Dash(__name__)

# Define the app
app.layout = html.Div(children=[
                      html.Div(className='row',  # Define the row element
                               children=[
                                  html.Div(className='three columns div-user-controls'),  # Define the left element
                                  html.Div(className='nine columns div-for-charts bg-grey')  # Define the right element
                                  ])
                                ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)