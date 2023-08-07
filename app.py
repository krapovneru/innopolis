import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

st.title('Визуализация датасета и гипотеза ')
uploaded_file = st.file_uploader("Выбор файла (CSV)", type="csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, encoding='ISO-8859-1')

    st.subheader('Выбор 2-х переменных для визуализации')
    var1 = st.selectbox('Первая переменная:', data.columns)
    var2 = st.selectbox('Вторая переменная:', data.columns)
    st.subheader('Графики:')
    for var in [var1, var2]:
        if data[var].dtype in ['int64', 'float64']:
            st.write(f'Распределение для {var}')
            fig, ax = plt.subplots()
            sns.histplot(data[var], bins=30, kde=True, ax=ax)
            plt.show()
            st.pyplot(fig)
        else:
            st.write(f'Pie chart для {var}')
            pie_chart_data = data[var].value_counts()
            plt.pie(pie_chart_data, labels=pie_chart_data.index, autopct='%1.1f%%')
            plt.axis('equal')
            st.pyplot()

    st.subheader('Выбор теста:')
    selected_test = st.selectbox('Выбор тест:', ['t-test', 'U-критерий Манна — Уитни'])

    if selected_test == 't-test' and data[var1].dtype in ['int64', 'float64'] and data[var2].dtype in ['int64', 'float64']:
        t_stat, p_val = stats.ttest_ind(data[var1], data[var2])
        st.write(f'Результат t-теста: t-statistic = {t_stat}, p-value = {p_val}')

    elif selected_test == 'U-критерий Манна — Уитни' and data[var1].dtype in ['int64', 'float64'] and data[var2].dtype in ['int64', 'float64']:
        stat, p_val = stats.mannwhitneyu(data[var1], data[var2])
        st.write(f'U-критерий Манна — Уитни: U-statistic = {stat}, p-value = {p_val}')

    else:
        st.write('Выбранный тест не может быть применен к выбранным переменным.')
else:
    st.write('CSV-файл не загружен.')
