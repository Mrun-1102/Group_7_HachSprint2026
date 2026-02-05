import pandas as pd

df = pd.read_csv("data/employee_master.csv")
  # use your exact filename

print("First 5 rows:")
print(df.head())

print("\nColumns:")
print(df.columns)

print("\nShape:")
print(df.shape)
