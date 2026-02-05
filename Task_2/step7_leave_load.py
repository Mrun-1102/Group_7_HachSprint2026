import pandas as pd

# Load Excel file
xls = pd.ExcelFile("data/leave_intelligence.xlsx")

print("Available sheets:")
print(xls.sheet_names)

# Load only required sheets
leave_history = pd.read_excel(xls, "Leave_History")
leave_balance = pd.read_excel(xls, "Available_Balances")

print("\nLeave History (sample):")
print(leave_history.head())

print("\nLeave Balances (sample):")
print(leave_balance.head())
