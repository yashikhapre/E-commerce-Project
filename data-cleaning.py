
import pandas as pd
import numpy as np

df = pd.read_csv("C:\\Users\\SHREE\\Downloads\\ecommerce_data1.csv")
print(df.head())

print(df.info())

print(df.describe())

print(df.isna().sum())

print(df.duplicated().sum())

df.drop_duplicates(inplace=True)

df['Discount Name'] = df['Discount Name'].fillna('No Discount')

df['Gender'].fillna(df['Gender'].mode()[0], inplace=True)

df.replace([-999, -1], 0, inplace=True)

df['Purchase Date'] = pd.to_datetime(df['Purchase Date'], format="%d/%m/%Y %H:%M:%S")

df['Purchase_Date'] = df['Purchase Date'].dt.strftime("%d/%m/%Y")  
df['Purchase_Time'] = df['Purchase Date'].dt.strftime("%H:%M:%S")

df.drop(['Purchase Date'], axis=1, inplace=True)

print(df.to_string())

df.to_csv("project1_df_cleaned.csv", index=False)




































