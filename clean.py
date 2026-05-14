import pandas as pd

df = pd.read_csv('Online_Retail.csv', encoding='latin1')

#1 Проверка датасета

print("До чистки:", df.shape)
print("Пустые строки:\n", df.isnull().sum())
print("Дубликаты:", df.duplicated().sum())

#2 Убираем дубликаты
df = df.drop_duplicates()

#3 Убираем пустые Customer ID
df = df.dropna(subset=['CustomerID'])

#4 Приводим столбцы к оптимальным типам данныз

df['CustomerID'] = df["CustomerID"].astype(int)
df['InvoiceDate'] = pd.to_datetime(df["InvoiceDate"])

#5 Удаляем возвраты, наличие и тип отображения указаны в описании к датасету

df = df[~df['InvoiceNo'].astype(str).str.startswith("C")]

#6 Проверяем наличие артефактов по цене и количсетву

print("Количество <= 0:", (df['Quantity'] < 0).sum())
print("Цена Единицы <= 0:", (df['UnitPrice'] < 0).sum())

#7 Убираем нулевые и минусовые значения 

df = df[df["Quantity"]>0]
df = df[df["UnitPrice"]>0]

#8 Результат чистки

print("После чистки:", df.shape)
print("Диапазон дат: от", df["InvoiceDate"].min(), " до ", df["InvoiceDate"].max())
print("Уникальных клиентов:", df["CustomerID"].nunique())
print("Уникальных стран:", df["Country"].nunique())

#9 Сохраняем результат в отдельный файл

df.to_csv("Online_Retail_clean.csv", index=False)
print("Чистый файл сохранен")