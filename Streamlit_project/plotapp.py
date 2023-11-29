import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from random import randint
from streamlit_echarts import st_echarts
from plotly.tools import FigureFactory as ff
import plotly.express as px
from sklearn.preprocessing import LabelEncoder

st.write('''
# Приложение с невероятными графиками чаевых

## Dataframe

Данные получены из не проверенного источника от некого пользователя "mwaskom". 
Если Вы попробуете просто открыть сайт: [githubusercontent.com](githubusercontent.com), у Вас ничего на получится. Можете начинать переживать о безопасности своего устройства.
''')

st.sidebar.header('Данные для построения графиков')

st.sidebar.markdown("""
[Dataset CSV который используется для построения графиков](https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv)
""")

# # Блок кода позволяет подгрузить свой dataframe
# uploaded_file = st.sidebar.file_uploader('Вы также можете загрузить свой CSV file. Формат таблицы должен быть идентичен шаблону из ссылки выше.', type=["csv"])
# if uploaded_file is not None:
#     input_df = pd.read_csv(uploaded_file)
# else:

# Обработка данных
tips = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv')
tips['time_order'] = [datetime(2023, 1, randint(1, 31)) for i in range(len(tips))]

st.write('## График показывающий динамику чаевых во времени')

option = {
    "xAxis": {
        "type": "category",
        "boundaryGap": False,
        "data": tips['time_order'].sort_values().index.tolist(),
    },
    "yAxis": {"type": "value"},
    "series": [
        {
            "data": tips['tip'].tolist(),
            "type": "line",
            "areaStyle": {},
        }
    ],
}
st_echarts(options=option)
    # options=option, height="400px",

st.write('## Гистограмма размера общего счета')
st.bar_chart(data=tips, x='time_order', y='total_bill', color='#8b00ff', use_container_width=True)

st.write('## Гистограмма размера общего счета')
st.scatter_chart(data=tips, x='total_bill', y='tip', color='#fc0fc0', use_container_width=True)

st.write('## График, связывающий общий счет, размер чаевых и количество позиций в заказе')
st.scatter_chart(data=tips, x='total_bill', y='tip', color='size', use_container_width=True)

st.write('## Связь между днем недели и размером счета')
st.bar_chart(data=tips, x='day', y='total_bill', color='day', use_container_width=True)

st.write('## Зависимость дня недели, чаевых и пола гостя')
st.scatter_chart(data=tips, x='tip', y='day', color='sex', height=400, use_container_width=True)

st.write('## Box plot c суммой всех счетов за каждый день c разбивкой по времени (обед или ужин)')
option1 = {
    "title": [
        {
            "text": "0: Lunch \n1: Dinner",
            "borderColor": "#999",
            "borderWidth": 1,
            "textStyle": {"fontWeight": "normal", "fontSize": 14, "lineHeight": 20},
            "left": "10%",
            "top": "90%",
        },
    ],
    "dataset": [
        {
            "source": [tips[tips['time'] == 'Lunch']['total_bill'].tolist(),
                    tips[tips['time'] == 'Dinner']['total_bill'].tolist()]
        },
        {
            "transform": {
                "type": "boxplot",
                "config": ['Lunch', 'Dinner'],
            }
        },
        {"fromDatasetIndex": 1, "fromTransformResult": 1},
    ],
    "tooltip": {"trigger": "item", "axisPointer": {"type": "shadow"}},
    "grid": {"left": "10%", "right": "10%", "bottom": "15%"},
    "xAxis": {
        "type": "category",
        "boundaryGap": True,
        "nameGap": 30,
        "splitArea": {"show": False},
        "splitLine": {"show": False},
    },
    "yAxis": {
        "type": "value",
        "name": "USD",
        "splitArea": {"show": True},
    },
    "series": [
        {"name": "boxplot", "type": "boxplot", "datasetIndex": 1},
        {"name": "outlier", "type": "scatter", "datasetIndex": 2},
    ],
}
st_echarts(option1, height="500px")

st.write('## Гистограмма чаевых на обед и ланч')
hist_data = [tips[tips['time'] == 'Dinner']['tip'], tips[tips['time'] == 'Lunch']['tip']]
group_labels = ['Dinner', 'Lunch']
fig = ff.create_distplot(hist_data, group_labels, bin_size=[.1, .25, .5])
st.plotly_chart(fig, use_container_width=True)

st.write('## Scatterplot, показывающий связь размера счета и чаевых, дополнительно отсортированный по курящим и некурящим')
fig = px.scatter(
    tips,
    x="tip",
    y="total_bill",
    size="tip",
    color="smoker",
    hover_name="sex",
    log_x=True,
    size_max=60,
)
st.plotly_chart(fig, theme="streamlit", use_container_width=True)

st.write('## Тепловая карта корреляции')
for i in tips.select_dtypes(include = ['object', 'category', 'bool']).columns.tolist():
    tips[i] = LabelEncoder().fit_transform(tips[i])

fig1 = px.imshow(tips.corr(), text_auto=True)
st.plotly_chart(fig1, theme="streamlit", use_container_width=True)