from deterministic_prompt import build_prompt
from deterministic_call import run_deterministic    


p = build_prompt(
    actor="SQL Analyst",
    input="SELECT TOP 5 * FROM Employees;",
    mission="Explain this SQL query step-by-step.",
    memory="You know SQL at expert level.",
    assets="Tables: Employees",
    actions="Do not invent columns.",
    prompt="Explain the SQL clearly"
)

output = run_deterministic(p)
print("Deterministic Output:\n", output)
