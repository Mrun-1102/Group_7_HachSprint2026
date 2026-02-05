import re

def extract_emp_id(question):
    match = re.search(r"(emp\d+)", question.lower())
    if match:
        return match.group(1).upper()
    return None


def detect_intent(question):
    q = question.lower()

    if "annual leave" in q or "leave entitlement" in q:
        return "annual_leave"

    if "sick" in q and "medical" in q:
        return "sick_leave"

    if "check-out" in q or "attendance" in q:
        return "attendance"

    if "sabbatical" in q:
        return "sabbatical"

    if "bank holiday" in q or "london" in q:
        return "location_leave"

    return "policy"
