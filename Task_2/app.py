import pandas as pd
import json

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# -------------------------------
# 1. LOAD STRUCTURED DATA
# -------------------------------

# Employee master
emp_df = pd.read_csv("data/employee_master.csv")
emp_df.columns = emp_df.columns.str.strip().str.lower()

# detect join date column dynamically
join_col = None
for col in emp_df.columns:
    if "join" in col:
        join_col = col
        break

emp_df[join_col] = pd.to_datetime(emp_df[join_col], errors="coerce")
emp_df["tenure_years"] = (
    pd.Timestamp.today() - emp_df[join_col]
).dt.days / 365


# Leave data
xls = pd.ExcelFile("data/leave_intelligence.xlsx")
leave_history = pd.read_excel(xls, "Leave_History")
leave_balance = pd.read_excel(xls, "Available_Balances")


# Attendance data
with open("data/attendance_logs_detailed.json", "r") as f:
    attendance_raw = json.load(f)

attendance_logs = []
if isinstance(attendance_raw, dict):
    attendance_raw = attendance_raw.get("logs", [])

for r in attendance_raw:
    if isinstance(r, dict):
        attendance_logs.append({
            "emp_id": r.get("employeeId") or r.get("emp_id"),
            "date": r.get("date"),
            "status": r.get("attendanceStatus") or r.get("status")
        })

attendance_df = pd.DataFrame(attendance_logs)


# -------------------------------
# 2. LOAD POLICY VECTOR STORE (FAST LOAD)
# -------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

policy_db = FAISS.load_local(
    "policy_index",
    embeddings,
    allow_dangerous_deserialization=True
)


# -------------------------------
# 3. ANSWER FUNCTIONS
# -------------------------------

def answer_structured(question, emp_id):
    emp = emp_df[emp_df["emp_id"] == emp_id]

    if emp.empty:
        return "❌ Insufficient data: Employee ID not found."

    q = question.lower()

    if "tenure" in q:
        tenure = round(emp.iloc[0]["tenure_years"], 2)
        return f"✔ Employee tenure is {tenure} years (source: employee_master.csv)"

    if "leave" in q:
        bal = leave_balance[leave_balance["emp_id"] == emp_id]
        if bal.empty:
            return "❌ Leave balance data not available."
        return f"✔ Available leave balance:\n{bal.to_string(index=False)}"

    if "attendance" in q:
        att = attendance_df[attendance_df["emp_id"] == emp_id]
        if att.empty:
            return "❌ No attendance records found."
        return f"✔ Attendance records:\n{att.head().to_string(index=False)}"

    return "❌ Structured data found but unable to answer specifically."


def answer_policy(question):
    results = policy_db.similarity_search(question, k=2)

    if not results:
        return "❌ Policy information not found."

    response = "✔ Policy reference (Helix_Pro_Policy_v2.pdf):\n\n"
    for r in results:
        response += r.page_content[:300] + "\n---\n"

    return response


def answer_hybrid(question, emp_id):
    structured_part = answer_structured(question, emp_id)
    policy_part = answer_policy(question)

    return (
        "✔ Hybrid Answer:\n\n"
        f"{structured_part}\n\n"
        f"{policy_part}"
    )


# -------------------------------
# 4. TERMINAL ENTRY POINT ONLY
# -------------------------------

if __name__ == "__main__":
    from question_parser import extract_emp_id, detect_intent

    print("\n=== HELIX HR INTELLIGENCE BOT ===\n")

    question = input("Ask your HR question: ")
    emp_id = extract_emp_id(question)

    if not emp_id:
        print("❌ Unable to identify employee from the question.")
    else:
        intent = detect_intent(question)

        if intent in [
            "annual_leave",
            "sick_leave",
            "sabbatical",
            "location_leave"
        ]:
            answer = answer_hybrid(question, emp_id)

        elif intent == "attendance":
            answer = answer_policy(question)

        else:
            answer = answer_policy(question)

        print("\n--- ANSWER ---")
        print(answer)
        print("\n--- END ---")
