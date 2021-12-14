from sklearn import datasets
import pandas as pd
pd.options.display.max_columns = 50
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
import functions_script as mf

plt.style.use('ggplot')

df = pd.read_csv('dump.csv')
# Drop the Borough column as this is non-numeric
df.drop(df.columns[1], axis = 1, inplace = True)

# Creating feature and target arrays
X = df.drop(['Unnamed: 0','Crime Count'], axis=1).values
y = df['Crime Count'].values

# Slice out the Population column, which is column 3
X_Population = X[:,2]
X_Pop_Density = X[:,5]
X_Pop_Young = X[:,6]
X_Unemployment_Rate = X[:,12]
X_Rented_Local_Authority = X[:,14]


X_Population = X_Population.reshape(-1, 1)
X_Pop_Density = X_Pop_Density.reshape(-1, 1)
X_Pop_Young = X_Pop_Young.reshape(-1, 1)
X_Rented_Local_Authority = X_Rented_Local_Authority.reshape(-1, 1)
X_Unemployment_Rate = X_Unemployment_Rate.reshape(-1, 1)

y = y.reshape(-1, 1)

# Plotting Linear Regression on a Single Feature; Population
# reg = LinearRegression()
# reg.fit(X_Population, y)
# prediction_space = np.linspace(min(X_Population), max(X_Population)).reshape(-1, 1)
# plt.scatter(X_Population, y, color='blue')
# plt.plot(prediction_space, reg.predict(prediction_space), color='black', linewidth=3)
# plt.show()

# Plotting Linear Regression on ALL features
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.5, random_state = 42)
# reg_all = LinearRegression()
# reg_all.fit(X_train, y_train)
# y_pred = reg_all.predict(X_test)
# print("Linear Regression / Train Test Split: ", reg_all.score(X_test, y_test), "\n\n")

# Cross Validation
# reg_cross = LinearRegression()
# cv_results = cross_val_score(reg_cross, X, y, cv = 3)
# print("Linear Regression / Cross Validation: ", cv_results)
# print("Linear Regression / Cross Validation / Mean: ", np.mean(cv_results))

# Ridge Regression
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)
# ridge = Ridge(alpha = 0.1, normalize = True)
# ridge.fit(X_train, y_train)
# ridge_pred = ridge.predict(X_test)
# print("Ridge Regression: ", ridge.score(X_test, y_test))

# Lasso Regression
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)
# lasso = Lasso(alpha = 5)
# lasso.fit(X_train, y_train)
# lasso_pred = lasso.predict(X_test)
# print("Lasso Regression: ", lasso.score(X_test, y_test))

names = df.drop(['Unnamed: 0', 'Crime Count'], axis = 1).columns
print(names)
print(X.shape, y.shape)
lasso = Lasso(alpha=5)
lasso_coef = lasso.fit(X, y).coef_
_ = plt.plot (range(len(names)),lasso_coef)
_ = plt.xticks(range(len (names)), names, rotation=60)
_ = plt.ylabel ('Coefficients')
plt. show()









