import plotly.express as px
import pandas as pd

df = pd.read_csv('../data_sheets/operator_data.csv')

fig = px.histogram(
    df,
    title='Distibution of Scores',
    x='Score',
    color='Score',
    nbins=200,
    hover_data=df.columns,
    text_auto=True
    
)

fig.update_xaxes(
    rangeslider_visible=True
)

fig.show() 
