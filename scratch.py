import pandas as pd
pd.options.display.max_columns = 50
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

import functions_script as mf

plt.style.use('ggplot')

df = pd.read_csv('dump.csv') # For testing, just use a dump of the main dataset created by the main script.
# Drop the Borough column as it is non-numeric and will cause errors
df.drop(df.columns[1], axis = 1, inplace = True)

# Creating feature and target arrays
X = df.drop(['Unnamed: 0','Crime Count'], axis=1).values
y = df['Crime Count'].values
y = y.reshape(-1, 1)
print("-----------------------------")

# Plotting Linear Regression on ALL features
print("Linear Regression / Train Test Split: All Features")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.5, random_state = 42)
reg_all = LinearRegression()
reg_all.fit(X_train, y_train)
y_pred = reg_all.predict(X_test)
print(reg_all.score(X_test, y_test))
print("-----------------------------")

# Use Cross Validation
print("Linear Regression / Cross Validation")
reg_cross = LinearRegression()
cv_results = cross_val_score(reg_cross, X, y, cv = 5)
print(cv_results)
print("Average 5-Fold CV Score: {}".format(np.mean(cv_results)))
print("-----------------------------")

# Use Ridge Regression with a fixed alpha
print("Ridge Regression / Fixed Alpha: All Features")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)
# ridge = Ridge(alpha = 15, normalize = True)
ridge = Ridge(alpha = 15)
ridge.fit(X_train, y_train)
ridge_pred = ridge.predict(X_test)
print("Ridge Regression: ", ridge.score(X_test, y_test))
print("-----------------------------")

# Use Lasso Regression with a fixed alpha
print("Lasso Regression / Fixed Alpha: All Features")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)
lasso = Lasso(alpha = 15)
lasso.fit(X_train, y_train)
lasso_pred = lasso.predict(X_test)
print("Lasso Regression: ", lasso.score(X_test, y_test))
print("-----------------------------")

# Use Grid Search CV with Ridge Regression
print("HyperParameter Tuning / Ridge Regression")
param_grid = {'alpha': np.arange(1, 50)}
ridge_grid = Ridge()
ridge_grid_cv = GridSearchCV(ridge_grid, param_grid, cv=5)
ridge_grid_cv.fit(X, y)
print("GridSearch / Best Params: ", ridge_grid_cv.best_params_)
print("GridSearch / Best Score: ", ridge_grid_cv.best_score_)
print("-----------------------------")

# Use Lasso for feature selection. Plot coefficients to determine the best features for prediction
names = df.drop(['Unnamed: 0', 'Crime Count'], axis = 1).columns
lasso = Lasso(alpha=10)
lasso_coef = lasso.fit(X, y).coef_
_ = plt.rcParams["figure.figsize"] = [15, 15]
_ = plt.plot (range(len(names)),lasso_coef)
_ = plt.xticks(range(len (names)), names, rotation=90)
_ = plt.ylabel ('Coefficients')
plt.show()

# Using Lasso for feature selection indicates Child Poverty is the most important feature for prediction, with
# Rented_Local_Authority the second most important. Show this by plotting a linear regression on just that feature.
X_Child_Poverty = X[:,16] # Child_Poverty is column 16
X_Child_Poverty = X_Child_Poverty.reshape(-1, 1)
reg = LinearRegression()
reg.fit(X_Child_Poverty, y)
prediction_space = np.linspace(min(X_Child_Poverty), max(X_Child_Poverty)).reshape(-1, 1)
plt.scatter(X_Child_Poverty, y, color='blue')
plt.ylabel ('Crime Count')
plt.xlabel ('Child Poverty')
plt.plot(prediction_space, reg.predict(prediction_space), color='black', linewidth=3)
plt.show()









