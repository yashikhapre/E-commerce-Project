
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

import matplotlib.pyplot as plt
import seaborn as sns

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





"""
# Ensure month column is datetime format
top_monthly_df['month'] = pd.to_datetime(top_monthly_df['month'])

# Add a readable month name column for seasonal trends
top_monthly_df['Month Name'] = top_monthly_df['month'].dt.month_name()
# Total revenue per month across all top products
seasonal_trends = top_monthly_df.groupby('Month Name')['monthly_revenue'].sum()

# Optional: reorder months for better chart visuals
seasonal_trends = seasonal_trends.reindex([
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
])

plt.figure(figsize=(10, 6))
sns.barplot(x=seasonal_trends.index, y=seasonal_trends.values, palette="Blues_d")
plt.title(' Seasonal Sales Trend (Top 5 Products)')
plt.xlabel('Month')
plt.ylabel('Revenue (INR)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

"""












