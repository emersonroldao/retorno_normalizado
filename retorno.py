import pandas as pd 
import yfinance as yf
import plotly.graph_objs as go 
import plotly.io as pio 

pio.templates.default = 'plotly_dark'

ibovespa = yf.download('^BVSP', start='2022-01-01', end='2023-05-31')['Adj Close']

ibovespa.name = 'IBOV'

ibovespa_retorno = ibovespa.pct_change()

ibovespa_retorno.dropna(inplace=True)

retorno_normalizado = (1 + ibovespa_retorno).cumprod()

ativos = ['SANB11.SA', 'BBAS3.SA', 'BBDC4.SA', 'ITUB4.SA']

df = yf.download(ativos, start='2022-01-01', end='2023-05-31')['Adj Close']

df.rename(columns={'SANB11.SA':'SANB11', 'BBAS3.SA':'BBAS3', 'BBDC4.SA':'BBDC4', 'ITUB4.SA':'ITUB4'}, inplace=True)

ativos_retorno = df.pct_change()

ativos_retorno.dropna(inplace=True)

ativos_retorno_normalizado = (1 + ativos_retorno).cumprod()

df_geral = pd.merge(retorno_normalizado, ativos_retorno_normalizado, how='inner', on='Date')

fig = go.Figure()
for col in df_geral.columns:
    fig.add_trace(go.Scatter(x=df_geral.index, y=df_geral[col], name=col))
fig.update_layout(title='Bancos vs Ibovespa',
                  xaxis_title='Data',
                  yaxis_title='Retorno Normalizado',
                  xaxis=dict(showgrid=False),
                  yaxis=dict(showgrid=True))
fig.show()
