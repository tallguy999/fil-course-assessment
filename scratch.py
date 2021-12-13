from sklearn import datasets
import pandas as pd
pd.options.display.max_columns = 50
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

plt.style.use('ggplot')

df = pd.read_csv('dump.csv')

# Creating feature and target arrays
X = df.drop('Crime Count', axis=1).values
y = df['Crime Count'].values

# Slice out the Population column, which is column 3
X_Population = X[:,3]
# X_Pop_Density = X[:,6]
# X_Pop_Young = X[:,7]
# X_Unemployment_Rate = X[:,13]
# X_Rented_Local_Authority = X[:,15]


X_Population = X_Population.reshape(-1, 1)
# X_Pop_Density = X_Pop_Density.reshape(-1, 1)
# X_Pop_Young = X_Pop_Young.reshape(-1, 1)
# X_Rented_Local_Authority = X_Rented_Local_Authority.reshape(-1, 1)
# X_Unemployment_Rate = X_Unemployment_Rate.reshape(-1, 1)

y = y.reshape(-1, 1)

# Plot the correlation between Population and Crime Count
# plt.scatter(X_Population, y)
# plt.ylabel('Drugs Offences (October 2021)')
# plt.xlabel('Population')
# plt.show()


# Fitting a Regression Model
reg = LinearRegression()
reg.fit(X_Population, y)
prediction_space = np.linspace(min(X_Population), max(X_Population)).reshape(-1, 1)
plt.scatter(X_Population, y, color='blue')
plt.plot(prediction_space, reg.predict(prediction_space), color='black', linewidth=3)
plt.show()


















