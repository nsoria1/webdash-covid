import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

#--------------------------------------------------------------

def create_dropdown(data_list):
    # Create dictionary to retrieve
    dropdown_dict = []

    for i in data_list:
        dropdown_dict.append(
            dict(
                {'label': i, 'value': i}
            )
        )

    return(dropdown_dict)

#--------------------------------------------------------------

def get_timeline_dash(df, menu):
    if not menu or menu=='All countries':
        dff = df
        dff = dff.groupby('timeline.date').agg({'timeline.deaths': 'sum',
                                                'timeline.confirmed': 'sum',
                                                'timeline.recovered': 'sum'})

        barchar = px.line(
            dff,
            x=dff.index,
            y=dff.columns,
            template='plotly_dark'
        )

        return(barchar)
    
    else:
        dff = df[df['name']==menu]
        barchar = px.line(
            dff,
            x=dff['timeline.date'],
            y=[
                dff['timeline.deaths'],
                dff['timeline.confirmed'],
                dff['timeline.recovered']
                ],
            template='plotly_dark')
        
        barchar.update_yaxes(range=[3, 9])
                
        return(barchar)

#--------------------------------------------------------------