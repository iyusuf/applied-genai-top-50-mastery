Perfect place to pause and ask that. Since you’ve:

* Done **Lab-01** (basic function calling)
* Done **manual EVV**
* Seen how to **automate EVV with pytest**

…the “next” is:

> **Lab-02: Use Function Calling for a simple *business-style* query (SQL-ish), with EVV around it.**

Basically: move from toy `add(a,b)` → “mini-Unanet/finance-like tool”.

---

## 1️⃣ High-level roadmap (immediate next 3 steps)

1. **Micro-Lab 02 – “SQL-style tool” (no real DB yet)**

   * Tool: `get_project_revenue(project_id)` with an in-memory fake DB (Python dict).
   * Use function calling to answer questions like:

     > “What is the revenue for project P123?”
   * Add EVV tests:

     * correct tool called
     * correct project_id
     * correct numeric result in answer.

2. **Micro-Lab 03 – Multi-tool function calling**

   * Tools: `get_project_revenue`, `get_project_cost`, `compute_profit`.
   * Model decides which tools to call and in what order.
   * This is the bridge to multi-agent orchestration later.

3. **Micro-Lab 04 – RAG as a tool**

   * Simple “document lookup” tool for specs or data dictionary.
   * Wrap your local RAG into one tool and call it from the model.

Right now, you’re exactly at **step 1**: Micro-Lab 02.

---

## 2️⃣ Micro-Lab 02 – AIM–MAAP–EVV (spec)

You can save this as:

`micro-labs/02-sql-style-tool/02-aim-maap-evv.md`

```markdown
# Micro-Lab 02 — SQL-Style Tool (Function Calling on Fake Finance Data)

**Category:** B. Function Calling & Tooling  
**Skill focus:** Business-style tool use (mini “SQL/finance” pattern)  
**Duration:** ~60 minutes  

---

## AIM — Framing

### A — Actor
The practitioner is an applied AI engineer building **finance/Unanet-like tools** with function calling:

- Comfortable with Python
- Has completed Micro-Lab 01 (basic function calling)
- Wants to simulate SQL/PLM-style queries without real DB connectivity yet

### I — Input

Starting assets:

- Python + OpenAI client installed
- Working API key
- A simple **in-memory “fake DB”** of projects and revenues

### M — Mission

Implement a function-calling flow where:

1. A tool `get_project_revenue(project_id: string)` is defined.
2. The model is asked questions like:
   - “What is the revenue for project P1001?”
3. The model:
   - Calls the tool with the correct `project_id`
   - Receives the numeric revenue
   - Explains the result in natural language.

---

## MAAP — How It Fits

### M — Memory
This lab becomes the **first business-flavored tool example**, a stepping stone toward:

- Unanet PLM queries
- SQL-backed tools
- Finance report automation

### A — Assets

- `fake_db` (Python dict with project_id → revenue)
- `fc_project_revenue.py`
- EVV tests (`test_evv_fc_project_revenue.py`)

### A — Actions

- Run multiple prompts to query different project IDs
- Observe tool arguments and outputs
- Extend to multiple projects or different fields later

### P — Prompt

Canonical prompt example:

> “Use the project revenue tool to tell me the revenue for project P1001.”

---

## EVV — Evaluate · Validate · Verify

### E — Evaluate

- Did the model call the `get_project_revenue` tool?
- Was the `project_id` argument correct (e.g., `"P1001"`)?

### V — Validate

- Did the returned numeric value match the fake DB value?
- Did the final answer mention that correct revenue?

### V — Verify

- If the fake DB is changed (e.g., revenue for `P1001` updated), do tests fail until code and expectations are updated?
- This proves the flow is tied to data and not just hallucinated text.

Done when:

- Tool call behavior is consistent across several prompts.
- Tests fail when data or tool logic is corrupted.
- Practitioner can describe how to swap fake DB → real DB or SQL later.
```

---

## 3️⃣ Micro-Lab 02 – Lab Steps (code)

Save as:

`micro-labs/02-sql-style-tool/02-lab-steps.md`

````markdown
# Micro-Lab 02 — SQL-Style Tool (Lab Steps)

**Goal:**  
Simulate a simple finance/Unanet query using function calling with a **fake in-memory database**.

---

## 1. Folder Setup

From repo root:

```bash
mkdir -p micro-labs/02-sql-style-tool
cd micro-labs/02-sql-style-tool
````

Use the same virtualenv as Lab-01 or create a new one.

---

## 2. Create `fc_project_revenue.py`

```python
from openai import OpenAI

client = OpenAI()

# Fake "database" of project revenues
FAKE_PROJECT_DB = {
    "P1001": 150000.00,
    "P1002": 235500.50,
    "P2001": 98765.43,
}


def get_project_revenue(project_id: str) -> float:
    """Return revenue for a given project ID, or raise KeyError if not found."""
    return FAKE_PROJECT_DB[project_id]


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_project_revenue",
            "description": "Look up the revenue for a given project ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "The project ID, e.g. 'P1001'.",
                    }
                },
                "required": ["project_id"],
            },
        },
    }
]


def main():
    user_message = {
        "role": "user",
        "content": "Use the project revenue tool to tell me the revenue for project P1001."
    }

    first = client.chat.completions.create(
        model="gpt-4.1",
        messages=[user_message],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "get_project_revenue"}},
    )

    msg = first.choices[0].message

    if not msg.tool_calls:
        print("No tool call was made.")
        print("Response:", msg.content)
        return

    tool_call = msg.tool_calls[0]
    fn_name = tool_call.function.name
    args = tool_call.function.arguments

    print("Tool call:")
    print("  name:", fn_name)
    print("  args:", args)

    if fn_name != "get_project_revenue":
        raise ValueError(f"Unexpected tool called: {fn_name}")

    project_id = args["project_id"]
    revenue = get_project_revenue(project_id)

    tool_message = {
        "role": "tool",
        "tool_name": fn_name,
        "content": str(revenue),
    }

    final = client.chat.completions.create(
        model="gpt-4.1",
        messages=[user_message, msg, tool_message],
    )

    print("Final answer:")
    print(final.choices[0].message.content)


if __name__ == "__main__":
    main()
```

Run:

```bash
python fc_project_revenue.py
```

You should see:

* Tool call with `project_id: "P1001"`
* Final answer mentioning the correct revenue from `FAKE_PROJECT_DB`.

---

## 3. Add Automated EVV Tests

Create: `test_evv_fc_project_revenue.py`

```python
import re
from openai import OpenAI
from fc_project_revenue import (
    tools,
    get_project_revenue,
    FAKE_PROJECT_DB,
)

client = OpenAI()


def call_project_revenue(project_id: str):
    user_message = {
        "role": "user",
        "content": f"Use the project revenue tool to tell me the revenue for project {project_id}."
    }

    first = client.chat.completions.create(
        model="gpt-4.1",
        messages=[user_message],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "get_project_revenue"}},
    )

    msg = first.choices[0].message

    tool_call = msg.tool_calls[0]
    fn_name = tool_call.function.name
    args = tool_call.function.arguments

    revenue = get_project_revenue(args["project_id"])

    tool_message = {
        "role": "tool",
        "tool_name": fn_name,
        "content": str(revenue),
    }

    final = client.chat.completions.create(
        model="gpt-4.1",
        messages=[user_message, msg, tool_message],
    )

    return tool_call, final.choices[0].message


def test_e_evaluate_tool_called():
    tool_call, _ = call_project_revenue("P1001")
    assert tool_call.function.name == "get_project_revenue"
    assert tool_call.function.arguments["project_id"] == "P1001"


def test_v_validate_revenue_correct():
    project_id = "P1002"
    expected = FAKE_PROJECT_DB[project_id]
    _, final_msg = call_project_revenue(project_id)

    numbers = re.findall(r"[0-9]+(?:\.[0-9]+)?", final_msg.content)
    floats = [float(n) for n in numbers]

    assert expected in floats, f"Expected {expected} in answer, got: {final_msg.content}"
```

Run:

```bash
pytest micro-labs/02-sql-style-tool/test_evv_fc_project_revenue.py
```

Now EVV for this lab is **fully automated**.

---

## 4️⃣ What this unlocks

Once you’re done with Lab-02, you’ll have:

* Function calling on **business-like data**
* Automated EVV around a mini “SQL/PLM-style” query
* A direct mental bridge to:

  * Unanet PLM views
  * Real SQL-backed tools
  * Resume Sorter scoring tools
  * CSSWEB inventory compare tools

If you like this direction, next I can:

* Generate **Micro-Lab 03: multi-tool (revenue + cost + profit)** in the same 2-file style, or
* Create a **generic EVV YAML spec + runner** so you stop hand-writing test files for each flow.
