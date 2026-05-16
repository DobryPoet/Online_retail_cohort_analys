import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загружаем исходные данные (не очищенные от гостей)
df = pd.read_csv('Online_Retail.csv', encoding='latin1', parse_dates=['InvoiceDate'])

# Удаляем возвраты (кредит-ноты)
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]

# Убираем некорректные количества и цены
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

# Рассчитываем общую стоимость
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# Группируем по товару
product_sales = df.groupby(['StockCode', 'Description']).agg({
    'TotalPrice': 'sum'
}).reset_index().sort_values('TotalPrice', ascending=False)

# Накопленный процент
product_sales['CumulativePercent'] = product_sales['TotalPrice'].cumsum() / product_sales['TotalPrice'].sum() * 100

# Категории A, B, C
def abc_category(percent):
    if percent <= 80:
        return 'A'
    elif percent <= 95:
        return 'B'
    else:
        return 'C'

product_sales['Category'] = product_sales['CumulativePercent'].apply(abc_category)

# Сохраняем
product_sales.to_csv('abc_products_all.csv', index=False)
print(product_sales['Category'].value_counts())

# График: топ-20
plt.figure(figsize=(10, 6))
sns.barplot(data=product_sales.head(20), x='TotalPrice', y='Description', hue='Category', dodge=False)
plt.title('Топ-20 товаров по выручке (все продажи, включая гостей)')
plt.tight_layout()
plt.savefig('abc_top20_all.png')
plt.show()