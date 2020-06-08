#%%
import requests
import pandas as pd
import plotly.graph_objects as go

# URL Link construction
timeline_url = "https://corona-api.com/timeline"

# API call
raw_timeline = requests.request("GET", timeline_url)
raw_timeline = raw_timeline.json()

# Transform data into pandas dataframe
df_timeline = pd.DataFrame(raw_timeline['data'])
df_timeline['updated_at'] = df_timeline['updated_at'].astype('datetime64')

# Plot timeline dashboard
fig = px.line(
    df, 
    x='Date', 
    y='AAPL.High', 
    title='Time Series with Range Slider and Selectors')

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)
fig.show()