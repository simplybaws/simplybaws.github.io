import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'C:\Projects\477\Logistic Regression\Log.csv')

print(df.head())

# Calculate the count of each choice (0 or 1) and create a new DataFrame with custom index labels
choice_counts = df['Choice (0/1)'].value_counts()
total_customers = choice_counts.sum()  # Total customers irrespective of choice
choice_counts_df = pd.DataFrame({'Count': [total_customers, choice_counts[1]]})
choice_counts_df.index = ['Total Customers', 'Customers who purchased']  # Labels

# Create the bar plot
plt.figure(figsize=(10, 6))
bar_plot = sns.barplot(x=choice_counts_df.index, y='Count', data=choice_counts_df)
plt.title('Customers who purchased vs. Total Customers')
plt.ylabel('Count')

# Annotate bars with numeric labels
for index, value in enumerate(choice_counts_df['Count']):
    plt.text(index, value, str(value), ha='center', va='bottom')

plt.show()