import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

df = pd.read_csv("C:/Users/izzyk/Documents/mdm_data/results.csv")
print(df.head())  # checking right file
print(df.columns)
# get numeric data from csv
numeric_df = df.select_dtypes(include=[np.number])
# selecting the different factors
difficulty_factors = ['roundabout_count', 'mini_roundabout_count', 'dual_carriageway_count', 'all_junction_count', 'all_mv']

# drop rows with missing values in the relevant columns
numeric_df = numeric_df.dropna(subset=['pass rates'] + difficulty_factors)

# calculates the absolute value for the Pearson's correlation coefficient between each difficulty factor and the pass
# rate for each test centre
correlations = numeric_df.corr().loc[difficulty_factors, 'pass rates'].abs()
# calculate weightings of each factor
weights = correlations/correlations.sum()
# standardise difficulty factors
zscore_scaler = StandardScaler()
df_zscore = df.copy()
df_zscore[difficulty_factors] = zscore_scaler.fit_transform(df_zscore[difficulty_factors])
# for each difficulty do the product of the respective weights and standardised values then sum all for difficulty score
df['Difficulty Score'] = sum(df_zscore[factor] * weights[factor] for factor in difficulty_factors)


# Display correlation results and the new difficulty scores
print("Pearson Correlations:")
print(correlations)
print("\nNormalized Weights:")
print(weights)
print("\nSample of Difficulty Scores:")
print(df[['Location', 'Difficulty Score']].head())

# saves an updated csv dataset file with difficulty score added
df.to_csv('updated_test_centers.csv', index=False)


# uses difficulty score and pass rates to fit a line of best fit
data = df[['pass rates', 'Difficulty Score']].dropna()
X = data[['Difficulty Score']]
y = data['pass rates']
model = LinearRegression()
model.fit(X, y)
predicted = model.predict(X)

# plotting line of best fit
plt.plot(X, predicted, color='red', label='Best Fit Line')
plt.xlabel('Difficulty Score')
plt.ylabel('Pass Rates (%)')
plt.title('Difficulty Score vs Pass Rates')
plt.legend()
# plotting test centres on scatter plot
plt.scatter(df['Difficulty Score'], df['pass rates'])
plt.show()


