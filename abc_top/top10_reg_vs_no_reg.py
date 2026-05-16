import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#1 Загружаем датафрейм
df = pd.read_csv('Online_Retail.csv', encoding='latin1', parse_dates=['InvoiceDate'])

#2 Убираем артефакты 

df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
df = df[(df['Quantity']>0) & df['UnitPrice']>0]

#2.1 После создания отчета было обнаружено, что топ-позиции занимают не товарные позиции добавил дополнительную очистку в дф

exclude_keywords = ['POSTAGE', 'FEE', 'Manual', 'Discount', 'Shipping']
df = df[~df['Description'].str.contains('|'.join(exclude_keywords), case=False, na=False)]

#3 Добавляем строку общей стоимости

df['TotalPrice'] = df['Quantity']*df['UnitPrice']

#4 Создаем два датафрейма для сравнения по зарегистрированным пользователям и незарегистрированным

reg_sales = df[~df['CustomerID'].isna()]
noreg_sale = df[df['CustomerID'].isna()]

#5 Топ 10 товаров среди зарегистрированных пользователей

reg_sum = reg_sales.groupby('Description')['TotalPrice'].sum().reset_index()
reg_sum.columns = ['Description', 'RegTSum']
reg_top10 = reg_sum.sort_values('RegTSum', ascending = False).head(10)


#6 Топ 10 товаров среди незарегистрированных пользователей

noreg_sum = noreg_sale.groupby('Description')['TotalPrice'].sum().reset_index()
noreg_sum.columns = ['Description','NoRegTSum']
noreg_top10 = noreg_sum.sort_values('NoRegTSum', ascending = False).head(10)

#7 Добавляем столбец гостевых покупок в топ-10 покупок зарегистрированных пользователей

reg_top10 = reg_top10.merge(noreg_sum, on='Description', how='left').fillna(0)

#8 Добавляем столбец покупок зарегистрированных клиентов в топ-10 покупок незарегистрированных пользователей

noreg_top10 = noreg_top10.merge(reg_sum, on='Description', how= 'left').fillna(0)

#9 График для reg_top10
fig, ax = plt.subplots(figsize=(10, 6))
y = np.arange(len(reg_top10))
width = 0.35

ax.barh(y - width/2, reg_top10['RegTSum'], width, label='Зарегистрированные', color='steelblue')
ax.barh(y + width/2, reg_top10['NoRegTSum'], width, label='Гости', color='darkorange')
ax.set_yticks(y)
ax.set_yticklabels(reg_top10['Description'])
ax.invert_yaxis()
ax.set_title('Топ-10 товаров зарегистрированных: вклад гостей')
ax.legend()
plt.tight_layout()
plt.savefig('reg_top10_cross.png')
plt.show()

#10 График для noreg_top10
fig, ax = plt.subplots(figsize=(10, 6))
y = np.arange(len(noreg_top10))
ax.barh(y - width/2, noreg_top10['NoRegTSum'], width, label='Гости', color='darkorange')
ax.barh(y + width/2, noreg_top10['RegTSum'], width, label='Зарегистрированные', color='steelblue')
ax.set_yticks(y)
ax.set_yticklabels(noreg_top10['Description'])
ax.invert_yaxis()
ax.set_title('Топ-10 товаров гостей: вклад зарегистрированных')
ax.legend()
plt.tight_layout()
plt.savefig('noreg_top10_cross.png')
plt.show()