import pandas as pd

df = pd.read_csv("data/employee_master.csv")

# standardize column names
df.columns = df.columns.str.strip().str.lower()

# 👇 CHANGE THIS to match YOUR actual column name
date_col = "joining_date"   # example – update if different

# convert to datetime
df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

# fill missing department
if "department" in df.columns:
    df["department"] = df["department"].fillna("Unknown")

# calculate tenure
df["tenure_years"] = (pd.Timestamp.today() - df[date_col]).dt.days / 365

print(df[["emp_id", "tenure_years"]].head())
