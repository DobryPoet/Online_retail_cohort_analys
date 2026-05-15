import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import rfm_segment_name as rsn

#1 Згружаю очищенный дф
df = pd.read_csv('Online_retail_clean.csv', parse_dates=['InvoiceDate'])

#2 Добавляю столбец с общей стоимостью товара
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

#3 Переменная крайней даты в дф
snapshot_date = df['InvoiceDate'].max()

#4 Расчитываем данные RFM анализа по каждому Посетителю
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: ((snapshot_date - x.max()).days), #Recency
    'InvoiceNo': 'nunique',                                    #Frequency
    'TotalPrice': 'sum'                                       #Monetary
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

#5 Добавляем столбцы с баллами по каждому полученному показателю

rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1], duplicates='drop')

rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5], duplicates='drop')

rfm['F_Score'] = 1
rfm.loc[(rfm['Frequency'] > 1) & (rfm['Frequency']<=5), 'F_Score'] = 2
rfm.loc[rfm['Frequency']>=6, 'F_Score'] = 3

rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

#6 Присваиваем удобные имена сегментам для визуализации

rfm['RFM_Name'] = rfm['RFM_Score'].apply(rsn.get_name)


#7. Сохранение результатов
rfm.to_csv('rfm_segments.csv', index=False)
print("RFM-таблица сохранена в rfm_segments.csv")
print(f"Всего клиентов: {len(rfm)}")
print(rfm['RFM_Name'].value_counts())

#8. Строим и сохраняем график 
plt.figure(figsize=(10, 6))
sns.countplot(data=rfm, y='RFM_Name', order=rfm['RFM_Name'].value_counts().index, palette='viridis')
plt.title('Распределение клиентов по RFM-сегментам')
plt.xlabel('Количество клиентов')
plt.ylabel('Название сегмента')
plt.tight_layout()
plt.savefig('rfm_segments_distribution.png')
plt.show()

