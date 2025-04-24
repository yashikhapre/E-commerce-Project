
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

df = pd.read_csv("project//project1_df_cleaned.csv")

user = "root"
password = "root"
host = "localhost"
port = 3306
database = "codenera"

engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}")

query = """
WITH top_products AS (
    SELECT `Product Category`
    FROM ecommerce_data
    GROUP BY `Product Category`
    ORDER BY SUM(`Net Amount`) DESC
    LIMIT 5
)

SELECT 
    DATE_FORMAT(STR_TO_DATE(`Purchase_Date`, '%d/%m/%Y'), '%Y-%m') AS month,
    `Product Category` AS product,
    SUM(`Net Amount`) AS monthly_revenue
FROM ecommerce_data
WHERE `Product Category` IN (SELECT `Product Category` FROM top_products)
GROUP BY month, product
ORDER BY month, monthly_revenue DESC;
"""

top_monthly_df = pd.read_sql(query, con=engine)
print(top_monthly_df)

top_monthly_df['month'] = pd.to_datetime(top_monthly_df['month'])
top_monthly_df['Month Name'] = top_monthly_df['month'].dt.month_name()
top_monthly_df['Month Num'] = top_monthly_df['month'].dt.month
top_monthly_df = top_monthly_df.sort_values(['Month Num'])

plt.figure(figsize=(12, 6))
sns.lineplot(
    data=top_monthly_df,
    x='Month Name',
    y='monthly_revenue',
    hue='product',  
    marker='o'
)

plt.title(' Monthly Revenue Trend for Top 5 Products')
plt.xlabel('Month')
plt.ylabel('Revenue (INR)')
plt.xticks(rotation=45)
plt.legend(title='Product')
plt.tight_layout()
plt.show()



















