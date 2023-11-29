import yfinance as yf
import streamlit as st

st.write('''
# Приложение с ценами на акции
         

Здесь показана цена закрытия торгов и рыночная стоимость акций компании Apple 
         
         
''')
# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
#define the ticker symbol
tickerSymbol = 'AAPL'
#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)
#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start='2020-11-28', end='2023-11-28')
# Open	High	Low	Close	Volume	Dividends	Stock Splits

st.line_chart(tickerDf.Close)
st.line_chart(tickerDf.Volume)