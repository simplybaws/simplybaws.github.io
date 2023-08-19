import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from scipy import stats


df = pd.read_csv(r'C:\Projects\477\Logistic Regression\Log.csv')

outcome = df['Choice (0/1)']
predictors = df[['Gender', 'Amount purchased', 'Frequency', 'Last purchase', 'First purchase', 'P_History', 'P_Science', 'P_Business', 'P_Educ', 'P_Health']]

predictors = sm.add_constant(predictors)
model = sm.Logit(outcome,predictors).fit()
print(model.summary())

#New model without First Purchase
outcome = df['Choice (0/1)']
predictors = df[['Gender', 'Amount purchased', 'Frequency', 'Last purchase', 'P_History', 'P_Science', 'P_Business', 'P_Educ', 'P_Health']]

predictors = sm.add_constant(predictors)
model = sm.Logit(outcome,predictors).fit()
print(model.summary())


#Splitting the data to check accuracy

x_train, x_test, y_train,y_test = train_test_split(predictors, outcome, test_size=0.3, random_state=42)

x_train = sm.add_constant(x_train)
model = sm.Logit(y_train, x_train).fit()
print(model.summary())

y_pred = model.predict(x_test)
y_pred = (y_pred > 0.5).astype(int)

print(confusion_matrix(y_pred,y_test))
print(classification_report(y_pred,y_test))

#Using untested dataset
df = pd.read_csv(r'C:\Projects\477\Logistic Regression\Log.csv')
untested = pd.read_csv(r'C:\Projects\477\Logistic Regression\Pred.csv')

#drop target
X_train = df.drop('Choice (0/1)', axis=1)
y_train = df['Choice (0/1)']

#split data
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

#fit log model
sk_model = LogisticRegression()
sk_model.fit(X_train, y_train)
y_pred = sk_model.predict(X_val)

#reports
print("Scikit-Learn Model:")
print(confusion_matrix(y_val, y_pred))
print(classification_report(y_val, y_pred))

# statsmodel for p-values
X_train_sm = sm.add_constant(X_train)
sm_model = sm.Logit(y_train, X_train_sm).fit()
print("Statsmodels Model:")
print(sm_model.summary())