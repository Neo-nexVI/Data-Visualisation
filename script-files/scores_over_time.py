import plotly.graph_objects as go
import pandas as pd
from datetime import timedelta

# Load the data
df = pd.read_csv('../data_sheets/operator_data.csv')

df['Date'] = pd.to_datetime(df['Date'], yearfirst=True)

df = df.sort_values(by='Date')

start_date= df['Date'].min() - pd.Timedelta(days=1)
end_date=   df['Date'].max() + pd.Timedelta(days=1) 

df['Random_Jitter'] = df.groupby('Date').cumcount()
df['Date_with_jitter'] = df['Date'] + pd.to_timedelta(df['Random_Jitter'] * 0.75, unit='h')
df_jittered = df[(df['Date_with_jitter'] >= start_date) & (df['Date_with_jitter'] <= end_date)]

df_1 = df.groupby('Date', as_index=False)['Score'].mean()
df_2 = df.groupby('Date', as_index=False)['Score'].max()
df_3 = df.groupby('Date', as_index=False)['Score'].min()

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        #x=df["Date_with_offset"],
        x=df_jittered["Date_with_jitter"],
        y=df_jittered["Score"],
        mode='lines+markers',
        name='All Scores',
        # text=df["Operator"],
        #line=dict(dash='dash')
    )
)

fig.add_trace(
    go.Scatter(
        x=df_1["Date"],
        y=df_1["Score"],
        mode='lines+markers',
        name='Average Scores',
        connectgaps=True
    )
)

fig.add_trace(
    go.Scatter(
        x=df_2["Date"],
        y=df_2["Score"],
        mode='lines+markers',
        name='Max Scores',
        connectgaps=True
    )
)

fig.add_trace(
    go.Scatter(
        x=df_3["Date"],
        y=df_3["Score"],
        mode='lines+markers',
        name='Min Scores',
        connectgaps=True
    )
)

fig.update_xaxes(
    range=[start_date,end_date],
    tickangle=90,
    tickformat='%y-%m-%d',
    dtick='D1',
    tickmode='linear',
    rangeslider_visible=True
)

fig.update_layout(
    updatemenus=[
        dict(
            active=0,
            buttons=list([
                dict(#graph4
                    label="Scores",
                    method="update",
                    args=[{"visible": [True, False, False, False, False]}],
                ),
                dict(#graph1
                    label="Average Scores",
                    method="update",
                    args=[{"visible": [False, True, False, False, False]}],
                ),
                dict(#graph2
                    label="Max Scores",
                    method="update",
                    args=[{"visible": [False, False, True, False, False]}],
                ),
                dict(#graph3
                    label="Min Scores",
                    method="update",
                    args=[{"visible": [False, False, False, True, False]}],
                ),
                dict(#graph4
                    label="All Scores",
                    method="update",
                    args=[{"visible": [True, True, True, True, True]}],
                ),
            ]),
            direction="down",
            showactive=True,
        ),
    ],
    xaxis=dict(
        tickangle=90,
        tickformat='%y-%m-%d',
        dtick='D1',
        tickmode='linear'
    ),
    yaxis=dict(
        autorange=True,
    ),
    title="Duration of Scores Ordered by Dates (2024-2025)"
)

fig.show()
