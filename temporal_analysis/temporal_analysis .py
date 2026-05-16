import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#1 загружаем и чистим датафрейм от артефактов

df = pd.read_csv('Online_Retail.csv', encoding='latin1', parse_dates=['InvoiceDate'])
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
df = df[(df['Quantity']>0) & (df['UnitPrice']>0)]
df['TotalPrice'] = df['Quantity']*df['UnitPrice']

#2 Добавляем столбцы по датам и времени

df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)
df['Month'] = df['InvoiceDate'].dt.month

day_mapping = {
    'Понедельник': 'Пн',
    'Вторник': 'Вт',
    'Среда': 'Ср',
    'Четверг': 'Чт',
    'Пятница': 'Пт',
    'Суббота': 'Сб',
    'Воскресенье': 'Вс'
}

df['Weekday'] = df['InvoiceDate'].dt.day_name(locale='ru_RU').map(day_mapping)
df['Hour'] = df['InvoiceDate'].dt.hour

#3 Динамика выручки по месяцам

monthly = df.groupby('YearMonth')['TotalPrice'].sum().reset_index()

#3.1 График динамики по месяцам

plt.figure(figsize=(12,5))
plt.plot(monthly['YearMonth'], monthly['TotalPrice'], marker='o')
plt.xticks(rotation=45)
plt.title('Динамика выручки по месяцам')
plt.xlabel('Месяц')
plt.ylabel('Выручка')
plt.tight_layout()
plt.savefig('monthly.png')
plt.show()


#4 Динамика продаж по дням

weekday = ['Пн','Вт','Ср','Чт','Пт','Сб','Вс']
weekday_sales = df.groupby('Weekday')['TotalPrice'].sum().reindex(weekday)

#4.1 График динамики по дням

plt.figure(figsize=(8,5))
sns.barplot(x=weekday_sales.index, y=weekday_sales.values, palette='viridis')
plt.title('Выручка по дням недели')
plt.xlabel('День недели')
plt.ylabel('Выручка')
plt.tight_layout()
plt.savefig('weekday.png')
plt.show()

#5 "Часы пик"

hourly = df.groupby('Hour')['TotalPrice'].sum()

#5.1 График "Часы пик"

hours_range = range(6, 21)
hourly_pct = (hourly / hourly.sum()) * 100
hourly_pct = hourly_pct.reindex(hours_range, fill_value=0)

plt.figure(figsize=(12,5))
bars = plt.bar(hourly_pct.index, hourly_pct.values, color='skyblue')
plt.title('Распределение выручки по часам (в % от общей выручки)')
plt.xlabel('Час')
plt.ylabel('Доля выручки, %')
plt.xticks(range(6,21))

for bar in bars:
    height = bar.get_height()
    if height > 1:
        plt.text(bar.get_x() + bar.get_width()/2., height/2, f'{height:.1f}%', 
                 ha='center', va='center', color='white', fontsize=8)
    elif height > 0:
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.2, f'{height:.1f}%', 
                 ha='center', va='bottom', fontsize=7)

plt.tight_layout()
plt.savefig('hourly.png')
plt.show()
