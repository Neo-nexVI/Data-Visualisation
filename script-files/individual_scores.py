import plotly.graph_objects as go
import pandas as pd
from datetime import timedelta

df = pd.read_csv('../data_sheets/operator_data.csv')

df['Date'] = pd.to_datetime( df['Date'], yearfirst=True)

df = df.sort_values(by='Date')

start_date = df['Date'].min() - pd.Timedelta(days=1)
end_date   = df['Date'].max() + pd.Timedelta(days=1)

df['random_jitter'] = df.groupby('Date').cumcount()
df['date_with_jitter'] = df['Date'] + pd.to_timedelta(df['random_jitter'] * 0.75, unit='h')
df_jittered = df[ (df['date_with_jitter'] >= start_date) & (df['date_with_jitter'] <= end_date) ]

df_1 = df.groupby('Date', as_index=False)['Score'].max()

departs = df['Operator_Name'].unique() #depart short for department

fig = go.Figure()

for depart in departs:
    depart_df = df[df['Operator_Name'] == depart]

    fig.add_trace(
        go.Scatter(
            x=depart_df['date_with_jitter'],
            y=depart_df['Score'],
            text=depart_df['Station'],
            textposition='top center',
            mode='lines+markers+text',
            name=depart,
            visible=False,
            connectgaps=True
        )
    )

fig.data[0].visible = True

dropdown_buttons = [
    dict(
        label=depart,
        method='update',
        args=[{'visible':[depart == trace.name for trace in fig.data] } ]
    )
    for depart in departs
]

fig.update_xaxes(
    rangeslider_visible=True
)

fig.update_layout(
    updatemenus=[
        dict(
            buttons=dropdown_buttons,
            direction='down',
            showactive=True,
        ),
    ],
    title="Individual Scores Over Time (2024/06/04 - 2025/03/10)",
    xaxis_title="Date",
    yaxis_title="Score",
)

fig.show()