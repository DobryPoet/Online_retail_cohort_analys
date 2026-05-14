import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#1 Загружаю данные
df = pd.read_csv("Online_Retail_clean.csv", parse_dates=['InvoiceDate'])


#2 Формируем временные когорты по месяцам первой покупки
cohort_date = df.groupby('CustomerID')['InvoiceDate'].min().reset_index()
cohort_date.columns = ['CustomerID', 'CohortDate']
cohort_date['CohortMonth'] = cohort_date['CohortDate'].dt.to_period('M')

#3 Добавляем столбец месяц покупки в основной датафрейм
df['InvoiceMonth'] = df['InvoiceDate'].dt.to_period('M')


#4 Соединяем датафреймы для определения когорты покупателя

df = df.merge(cohort_date[['CustomerID', 'CohortMonth']], on='CustomerID', how='left')

#5 Добавляем столбец числа прошедших месяцев с начала первой покупки(когорты) от текущей транзакции

df['CohortIndex'] = (df['InvoiceMonth'].dt.year - df['CohortMonth'].dt.year)*12 + (df['InvoiceMonth'].dt.month-df['CohortMonth'].dt.month)
cohort_counts = df.groupby(['CohortMonth', 'CohortIndex'])['CustomerID'].nunique().reset_index()
cohort_counts.columns = ['CohortMonth', 'CohortIndex', 'CustomerCount']

#6 Получаем количество клиентов в каждой когорте в месяце 0
cohort_sizes = cohort_counts[cohort_counts['CohortIndex'] == 0].set_index('CohortMonth')['CustomerCount']

#7 Считаем retention rate (делим каждое значение на размер соответствующей когорты)
retention = cohort_counts.pivot(index='CohortMonth', columns='CohortIndex', values='CustomerCount')
retention = retention.divide(cohort_sizes, axis=0) * 100

#8 Визуализация (тепловая карта)
plt.figure(figsize=(12, 8))
sns.heatmap(retention, annot=True, fmt='.1f', cmap='YlGnBu', 
            cbar_kws={'label': 'Retention Rate (%)'})
plt.title('Когортный анализ удержания клиентов (Retention)')
plt.xlabel('Месяцы после первой покупки')
plt.ylabel('Когорта (месяц первой покупки)')
plt.tight_layout()
plt.savefig('retention_heatmap.png', dpi=150)
plt.show()

#9 Сохраняем таблицу retention в CSV
retention.to_csv('retention_matrix.csv')
print("Retention матрица сохранена в retention_matrix.csv")
print("График сохранён как retention_heatmap.png")
