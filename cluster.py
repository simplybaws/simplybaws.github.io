import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import statsmodels.api as sm

#read in file check for nulls
df = pd.read_csv(r'C:\Projects\477\Cluster\Clust.csv')
print(df.head())
print(df.isnull().sum())

#set dataset into array
X = df[['Fashion','Price','BuyConvenience','BrandName','StoreDisplay','variety','Material','Fit','Colors','MatchingProds']]

#run various clusters
cluster_range = range(1, 8)  

explained_variances = []

# calculate variance
for num_clusters in cluster_range:
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(X)
    inertia = kmeans.inertia_
    total_variance = ((X - X.mean()) ** 2).sum().sum()  
    explained_variance = 1 - (inertia / total_variance)
    explained_variances.append(explained_variance)

# plot the explained variance to use elbow method
plt.plot(cluster_range, explained_variances, marker='o')
plt.xlabel('Number of Clusters')
plt.ylabel('Explained Variance')
plt.title('Elbow Method for Optimal Number of Clusters')
plt.show()

#set up cluster model using only 2 clusters

optimal_num_clusters = 2

# Fit K-means with the optimal number of clusters
kmeans = KMeans(n_clusters=optimal_num_clusters)
kmeans.fit(X)
cluster_labels = kmeans.labels_

# Attach cluster labels to the original DataFrame
X['Cluster'] = cluster_labels
df['Cluster'] = cluster_labels
# Calculate mean values for each feature within each cluster
mean_values = X.groupby('Cluster').mean()

# Calculate mean values for each feature within each cluster

# Plotting a grouped bar chart to compare clusters against each feature
mean_values_transposed = mean_values.T

# Plotting a grouped bar chart with clusters as bars and features as x labels
mean_values_transposed.plot(kind='bar', figsize=(12, 6))
plt.xlabel('Features')
plt.ylabel('Average Value')
plt.title('Average Values of Clusters Across Features')
plt.xticks(rotation=45)
plt.legend(title='Cluster')
plt.tight_layout()
plt.show()


cluster_centers = kmeans.cluster_centers_

# Plotting a line chart with cluster centers as data points
plt.figure(figsize=(12, 6))
for cluster_idx, center in enumerate(cluster_centers):
    plt.plot(center, marker='o', label=f'Cluster {cluster_idx + 1}')

plt.xlabel('Features')
plt.ylabel('Cluster Center Value')
plt.title('Cluster Centers for Each Feature')
plt.xticks(np.arange(len(X.columns)), X.columns, rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

#logistic Regression

x = df[['InfoNet','InfoFriends','InfoMags','InfoCat','InfoSocial','ImThrifty','ImAthletic','ImCool','ImRational','ImFun','PplAskMe','Age','Income','Edu']]
y = df['Cluster']

X_train, X_test, y_train,y_test = train_test_split(x, y, test_size = 0.2, random_state = 42)

skmodel = LogisticRegression()
skmodel.fit(X_train, y_train)
y_pred = skmodel.predict(X_test)
y_pred = (y_pred > 0.5).astype(int)

print(confusion_matrix(y_pred,y_test))
print(classification_report(y_pred,y_test))

X_train = sm.add_constant(X_train)
model = sm.Logit(y_train, X_train).fit()
print(model.summary())