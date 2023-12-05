import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the CSV data
df = pd.read_csv("BTC-USD.csv")

## Set Seaborn style
sns.set(style="whitegrid")

# Create a line plot with Seaborn
plt.figure(figsize=(15, 6))
sns.lineplot(x='Date', y='Close', data=df, label='Closing Value')
sns.lineplot(x='Date', y='High', data=df, label='High Value', alpha=0.7)
sns.lineplot(x='Date', y='Low', data=df, label='Low Value', alpha=0.7)

# Customize the plot
plt.title('Bitcoin Price Over Time')
plt.xlabel('Date', rotation=45, ha='right')
plt.ylabel('Price')
plt.legend()
plt.show()