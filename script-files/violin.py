import plotly.express as px
import pandas as pd

df = pd.read_csv('../data_sheets/operator_data.csv')

fig = px.violin(
    df,
    title='Viloin Graph',
    x='Operator_Name',
    y='Score',
    box=True,
    points='all',
    color='Operator_Name',
    hover_data=['Date'],
    violinmode='overlay'
)

fig.update_xaxes(
    rangeslider_visible=True
)

fig.show() 