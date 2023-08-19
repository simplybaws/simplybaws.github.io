import pandas as pd
from scipy.stats import f_oneway
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv(r'C:\Projects\477\Multiple Regression\MRData.csv')

# Group the data
# Assuming "season" is a categorical column and "EconContracts" is the numerical column
groups = df['season'].unique()
grouped_data = [df[df['season'] == group]['EconContracts'] for group in groups]

f_statistic, p_value = f_oneway(*grouped_data)

print("F-statistic:", f_statistic)
print("P-value:", p_value)

plt.figure(figsize=(8, 6))
sns.barplot(x='season', y='EconContracts', data=df)  # Use the original DataFrame 'df'
plt.title('Average Demand by Season')
plt.xlabel('Season')
plt.ylabel('Average Demand')
plt.show()
