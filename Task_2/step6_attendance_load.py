import json

with open("data/attendance_logs_detailed.json", "r") as f:
    raw = json.load(f)

print("Type of raw:", type(raw))

# If raw is dict, print keys
if isinstance(raw, dict):
    print("Top-level keys:", raw.keys())

# If raw is list, print first element
if isinstance(raw, list):
    print("First element type:", type(raw[0]))
    print("First element value:", raw[0])
