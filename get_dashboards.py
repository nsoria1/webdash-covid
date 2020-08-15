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
# Plot scatter line related to info per country

def get_timeline_dash(df, menu):
    # Rename data frame columns
    df.rename(
        {"timeline.deaths": "deaths", 
        "timeline.confirmed": "confirmed", 
        "timeline.recovered": "recovered", 
        "timeline.date": "date"},
        axis='columns',
        inplace=True)

    if not menu or menu=='All countries':
        dff = df
        dff = dff.groupby('date').agg({'deaths': 'sum',
                                                'confirmed': 'sum',
                                                'recovered': 'sum'})

        barchar = px.line(
            dff,
            x=dff.index,
            y=dff.columns,
            template='plotly_dark'
        )

        barchar.update_yaxes(range=[dff['confirmed'].min(), dff['confirmed'].max()])

        return(barchar)
    
    else:
        dff = df[df['name']==menu]
        #dff = df[(df['name'].isin(menu))] Line required for list selection in dropdown
        barchar = px.line(
            dff,
            x=dff['date'],
            y=[
                dff['deaths'],
                dff['confirmed'],
                dff['recovered']
                ],
            template='plotly_dark')
        
        barchar.update_yaxes(range=[dff['confirmed'].min(), dff['confirmed'].max()])
                
        return(barchar)

#--------------------------------------------------------------
# Plot indicators
def create_indicators(df, dropdown):
    fig = go.Figure()
    loop = 0

    # Dictionary example to generate the indicators
    if not dropdown:
        data = {
            'fig1': ['Critical Patients', 0],
            'fig2': ['Death Rate', 0],
            'fig3': ['Recovery Rate', 0],
            'fig4': ['Cases per Million Population', 0]
            }
    else:
        df2 = df[df['name']==dropdown]

        df2 = df2.get(
            ['latest_data.critical',
            'latest_data.calculated.death_rate', 
            'latest_data.calculated.recovery_rate', 
            'latest_data.calculated.cases_per_million_population']
            )
        
        df2.rename(
            {"latest_data.critical": "critical", 
            "latest_data.calculated.death_rate": "death_rate", 
            "latest_data.calculated.recovery_rate": "recovery_rate", 
            "latest_data.calculated.cases_per_million_population": "cases_per_million"},
            axis='columns',
            inplace=True)

        data = {
            'ind1': ['Critical Patients', df2['critical'].astype(int)],
            'ind2': ['Death Rate', df2['death_rate'].astype(int)],
            'ind3': ['Recovery Rate', df2['recovery_rate'].astype(int)],
            'ind4': ['Cases per Million Population', df2['cases_per_million'].astype(int)]
            }


    domain_dict = {
        0: {'x': [0, 0.5], 'y': [0, 0.20]},
        1: {'x': [0, 0.5], 'y': [0.40, 0.60]},
        2: {'x': [0.4, 0], 'y': [0, 0.20]},
        3: {'x': [0.4, 0], 'y': [0.40, 0.60]}
        }
    
    for i in data:
        fig.add_trace(go.Indicator(
            mode = "gauge+number",
            value = data[i][1],
            title = {'text': data[i][0]},
            domain = domain_dict[loop]
        ))
        loop = loop + 1
    
    return(fig)