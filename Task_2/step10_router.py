def route_question(q: str) -> str:
    q = q.lower()
    if any(k in q for k in ["policy", "rule", "exception", "allowed"]):
        return "policy"
    if any(k in q for k in ["leave", "attendance", "balance", "tenure"]):
        return "structured"
    return "hybrid"

# tests
print(route_question("How many leaves do I have?"))
print(route_question("What does HR policy say about regional exceptions?"))
print(route_question("Am I eligible for maternity leave?"))
