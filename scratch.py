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
# Drop the Borough column as it is non-numeric and will cause errors
df.drop(df.columns[1], axis = 1, inplace = True)

# Creating feature and target arrays
X = df.drop(['Unnamed: 0','Crime Count'], axis=1).values
y = df['Crime Count'].values
y = y.reshape(-1, 1)

# Plotting Linear Regression on ALL features
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.5, random_state = 42)
reg_all = LinearRegression()
reg_all.fit(X_train, y_train)
y_pred = reg_all.predict(X_test)
print("Linear Regression / Using Train Test Split: ", reg_all.score(X_test, y_test))

# Use Cross Validation
reg_cross = LinearRegression()
cv_results = cross_val_score(reg_cross, X, y, cv = 5)
print("Linear Regression / Using Cross Validation: ", cv_results)
print("Linear Regression / Using Cross Validation / Mean: ", np.mean(cv_results))

# Use Ridge Regression
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)
# ridge = Ridge(alpha = 15, normalize = True)
ridge = Ridge(alpha = 15)
ridge.fit(X_train, y_train)
ridge_pred = ridge.predict(X_test)
print("Ridge Regression: ", ridge.score(X_test, y_test))

# Use Lasso Regression
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)
lasso = Lasso(alpha = 20)
lasso.fit(X_train, y_train)
lasso_pred = lasso.predict(X_test)
print("Lasso Regression: ", lasso.score(X_test, y_test))

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









