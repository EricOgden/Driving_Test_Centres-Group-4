import pandas as pd

# reads dataset of test centres and pass rates
df = pd.read_csv("test_centres_extra.csv")

# randomly samples 10 test centres
random_10 = df.sample(n=10, random_state=42)  # random_state=42 for reproducibility

# create new data set with the 10 chosen centres
random_10.to_csv("random_centres.csv", index=False)

print(random_10)