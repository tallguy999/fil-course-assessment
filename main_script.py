import functions_script as mf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

# Uncommment one of the following lines to target a specific crime
# target_crime = "Anti-social behaviour"
# target_crime = "Bicycle theft"
# target_crime = "Burglary"
# target_crime = "Criminal damage and arson"
# target_crime = "Drugs"
# target_crime = "Other crime" # Pick
# target_crime = "Other theft"
# target_crime = "Possession of weapons"
target_crime = "Public order"
# target_crime = "Robbery"
# target_crime = "Shoplifting"
# target_crime = "Theft from the person"
# target_crime = "Vehicle crime"
# target_crime = "Violence and sexual offences"

# Create a dataframe from the London Borough Profiles data (Remote XLSX)
profiles_url = 'https://data.london.gov.uk/download/london-borough-profiles/80647ce7-14f3-4e31-b1cd-d5f7ea3553be/london-borough-profiles.xlsx'
df_profiles, boroughs = mf.Get_Profiles(profiles_url)

# Create a dataframe from the crimes data (CSV)
# Note: This relies on the Boroughs list generated by the previous function, mf.Get_Profiles()
# Pass the name of the CSV file plus the boroughs list to filter out non-London regions
# Pass the Crime types as a list to filter specific crimes
df_crimes = mf.Get_Crimes('data/2019-10-metropolitan-street.csv', boroughs, [target_crime])

# Create a dataframe from the Key Indicators data (Remote SQL)
df_keyindicators = mf.Get_Key_Indicators()

# Merge the three dataframes based on the 'Borough' column; df_crimes, df_profiles, df_keyindicators)
df = pd.merge(df_crimes, df_profiles, on="Borough",how="left")
df = pd.merge(df, df_keyindicators, on="Borough",how="left")

# LINEAR REGRESSION
print("\nStarting Linear Regression Functions..")
# Drop the Borough column as it is non-numeric and will cause errors
df.drop(df.columns[0], axis = 1, inplace = True)
# Export the final, merged dataframe to an Excel spreadsheet for easy checking
mf.ExportExcel(df, 'df_final')

# Creating the feature and target arrays
X = df.drop(['Crime Count'], axis=1).values
y = df['Crime Count'].values
y = y.reshape(-1, 1)

# 1. Linear Regression using Train_Test_Split
print("\nLinear Regression / Train Test Split: All Features")
print("test_size = 0.3, random_state = 42")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)
reg_all = LinearRegression()
reg_all.fit(X_train, y_train)
y_pred = reg_all.predict(X_test)
print("Score: ", reg_all.score(X_test, y_test))
print("------------------------------------------------------\n")

# 2. Linear Regression Using Cross Validation
print("Linear Regression with Cross Validation")
reg_cross = LinearRegression()
cv_results = cross_val_score(reg_cross, X, y, cv = 5)
print(cv_results)
print("Average 5-Fold CV Score: {}".format(np.mean(cv_results)))
print("------------------------------------------------------\n")

# 3. Ridge Regression
print("Ridge Regression / alpha = 15")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)
# ridge = Ridge(alpha = 15, normalize = True) # Using "normalise = True" works BUT generates a 'FutureWarning' error
ridge = Ridge(alpha = 15)
ridge.fit(X_train, y_train)
ridge_pred = ridge.predict(X_test)
print("Ridge Regression: ", ridge.score(X_test, y_test))
print("------------------------------------------------------\n")

# 4. Lasso Regression
print("Lasso Regression / alpha = 15")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)
# lasso = Lasso(alpha = 15, normalize = True) # Using "normalise = True" works BUT generates a 'FutureWarning' error
lasso = Lasso(alpha = 15)
lasso.fit(X_train, y_train)
lasso_pred = lasso.predict(X_test)
print("Lasso Regression: ", lasso.score(X_test, y_test))
print("------------------------------------------------------\n")

# 5. HyperParameter Tuning - Grid Search CV with Ridge Regression
print("HyperParameter Tuning (alpha) / Ridge Regression")
param_grid = {'alpha': np.arange(1, 100)}
ridge_grid = Ridge()
ridge_grid_cv = GridSearchCV(ridge_grid, param_grid, cv=15)
ridge_grid_cv.fit(X, y)
print("GridSearch / Best Params: ", ridge_grid_cv.best_params_)
print("GridSearch / Best Score: ", ridge_grid_cv.best_score_)
print("------------------------------------------------------\n")

# 6. Use Lasso for feature selection. Plot coefficients to determine the best features for prediction
plot_title = 'Lasso for Feature Selection: ' + target_crime
names = df.drop(['Crime Count'], axis = 1).columns
lasso = Lasso(alpha=5)
lasso_coef = lasso.fit(X, y).coef_
plt.rcParams["figure.figsize"] = [10, 20]
plt.grid(True)
plt.plot (range(len(names)),lasso_coef)
plt.xticks(range(len (names)), names, rotation=90)
plt.ylabel('Coefficients')
plt.title(plot_title)
plt.show()

# Using Lasso for feature selection indicates Rented Local Authority is the most important feature for predicting
# Public Order offences. Show this by plotting a linear regression on that feature.
# Rented_Local_Authority is column 14
plot_title = 'Linear Regression: Total ' + target_crime + " / " + " Rented Local Authority"
X_Plot = X[:,14]
X_Plot = X_Plot.reshape(-1, 1)
reg = LinearRegression()
reg.fit(X_Plot, y)
prediction_space = np.linspace(min(X_Plot), max(X_Plot)).reshape(-1, 1)
plt.rcParams["figure.figsize"] = [10, 10]
plt.scatter(X_Plot, y, color='blue')
plt.ylabel(target_crime)
plt.xlabel('Rented Local Authority')
plt.title(plot_title)
plt.plot(prediction_space, reg.predict(prediction_space), color='black', linewidth=3)
plt.show()