import pandas as pd
import statsmodels.api as sm

df = pd.read_csv(r'C:\Projects\477\Multiple Regression\MRData.csv')

#get dummies
season_dummies = pd.get_dummies(df['season'], prefix ='season', drop_first=True)
df = pd.concat([df, season_dummies], axis = 1)

print(df.head())

#set up variables
outcome = df['EconContracts']
predictors = df[['CompPrice','flights','GasPrice','OwnPrice','session','season_Spring','season_Summer','season_Winter']]

#set up model
predictors = sm.add_constant(predictors)

model = sm.OLS(outcome,predictors).fit()

print(model.summary())

#r-square
r_squared = model.rsquared
print('R Square Value : ', r_squared)

#adjusted r-square
adjusted_r_square = model.rsquared_adj
print('Adjusted R Value :', adjusted_r_square)



#New model-fit

outcome_new = df['EconContracts']
predictors_new = df[['CompPrice','flights','GasPrice','OwnPrice']]

predictors_new = sm.add_constant(predictors_new)
model_new = sm.OLS(outcome_new,predictors_new).fit()

print(model_new.summary())

rsq_new = model_new.rsquared
rsqw_new_adj = model_new.rsquared_adj

print('R Square new value :', rsq_new, 'New Adjusted Value :', rsqw_new_adj)

preds = model_new.predict(predictors_new)

absolute_residuals = abs(outcome_new - preds)
print(absolute_residuals)


#4 other variables

outcome1 = df['Upgrades']
model1 = sm.OLS(outcome1, predictors_new).fit()
print(model1.summary())

outcome2 = df['TotalContracts']
model2 = sm.OLS(outcome2,predictors_new).fit()
print(model2.summary())

outcome3 = df['AvgContLength']
model3 = sm.OLS(outcome3,predictors_new).fit()
print(model3.summary())

outcome4 = df['ContractDays']
model4 = sm.OLS(outcome4,predictors_new).fit()
print(model4.summary())

