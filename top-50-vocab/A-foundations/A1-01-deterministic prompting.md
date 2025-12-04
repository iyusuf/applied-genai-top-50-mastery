Below is your **Micro-Lab A1-01 — Deterministic Prompting (AIM → MAAP → EVV)**
**designed for the OpenAI API Platform**, **not ChatGPT Web**, and fully runnable from Python.

This lab is structured exactly like your Function Calling labs:

* **Mini Theory (10 min)**
* **Mini Coding Lab (20–30 min)**
* **Hands-on deterministic runs with OpenAI API**
* **EVV validation inside your Python client**
* **AIM → MAAP → EVV turned into a reusable function**

This is **Skill 01** from your Top-50 mastery list (Foundations → Deterministic Prompting).
This lab is tuned for **production-grade CAIO workflows** (Unanet PLM, CSSWEB, Resume Sorter, CAIO-OS).

---

# 🧪 **MICRO-LAB A1-01 — Deterministic Prompting with AIM → MAAP → EVV**

**Category:** A. Foundations
**Skill focus:** Deterministic prompting implemented inside the **OpenAI API Platform**
**Difficulty:** Beginner → Intermediate
**Duration:** 30–45 minutes
**Prerequisites:**

* Python 3.10+
* OpenAI Python SDK
* Basic familiarity with structured prompting

---

# 1. 🎯 **AIM — Lab Framing**

### **A — Actor**

CAIO / Applied AI Engineer writing deterministic prompts for reproducible automation.

### **I — Input**

You want to apply AIM→MAAP→EVV **through the OpenAI API**, not ChatGPT Web.

### **M — Mission**

Implement a **deterministic prompt wrapper** in Python and run repeatable experiments:

1. Build a reusable AIM→MAAP→EVV template.
2. Wrap prompts automatically.
3. Send them to `client.responses.create()` using deterministic settings.
4. Verify reproducibility by running multiple times.
5. Add EVV self-validation inside your wrapper.

---

# 2. 🧠 **MINI THEORY (10 minutes)**

Deterministic prompting means:

### ✔ Same input → same structure → same reasoning → same output style

You eliminate:

* Hallucinations
* Format drift
* Creative variability
* Unstable outputs

### Why AIM → MAAP → EVV works

| Layer    | Purpose                                 | Result               |
| -------- | --------------------------------------- | -------------------- |
| **AIM**  | Identify Actor, Input, Mission          | Stable context       |
| **MAAP** | Provide Memory, Assets, Actions, Prompt | Bounded behavior     |
| **EVV**  | Built-in LLM self-validation            | Deterministic output |

### Why API environment is better for determinism

* You control **temperature**, **top_p**, **seed**, **frequency penalties**, etc.
* You can wrap prompts cleanly in code.
* You can enforce a fixed structure.
* You can version the wrappers.

---

# 3. 🧪 **MINI CODING LAB (20–30 minutes)**

You will do three things:

1. Build a **deterministic wrapper** function.
2. Call OpenAI API with **deterministic response settings**.
3. Compare results from multiple runs.

---

# ✅ **STEP 1 — Install and configure OpenAI SDK**

```bash
pip install openai
```

```python
from openai import OpenAI
client = OpenAI()
```

---

# ✅ **STEP 2 — Create deterministic_prompt.py**

Create this file in your repo:

```python
# deterministic_prompt.py

TEMPLATE = """
AIM
A — {actor}
I — {input}
M — {mission}

MAAP
Memory:
{memory}

Assets:
{assets}

Actions:
{actions}

PROMPT:
{prompt}

EVV — Deterministic Self-Check
1. Evaluate input completeness.
2. Validate assumptions against provided assets.
3. Verify the final answer strictly follows the requested structure.
"""

def build_prompt(
    actor,
    input,
    mission,
    memory="None",
    assets="None",
    actions="Follow deterministic structure. No hallucinations.",
    prompt="Provide output."
):
    return TEMPLATE.format(
        actor=actor,
        input=input,
        mission=mission,
        memory=memory,
        assets=assets,
        actions=actions,
        prompt=prompt,
    )
```

This is your “AIM→MAAP→EVV wrapper generator”.

---

# ✅ **STEP 3 — Deterministic API Call Function**

Create a separate file: **deterministic_call.py**

```python
from openai import OpenAI
from deterministic_prompt import build_prompt

client = OpenAI()

def run_deterministic(prompt):
    response = client.responses.create(
        model="gpt-4.1-mini",     # or gpt-4.1/gpt-5.1/gpt-5.1-preview
        input=prompt,
        temperature=0,            # deterministic
        top_p=1,
        seed=123,                 # ensures reproducibility
        max_output_tokens=300,
    )
    return response.output_text
```

Key settings:

* `temperature=0`
* `seed=123`
* `top_p=1.0`
* fixed token limits

This is optimal for deterministic workflows.

---

# ✅ **STEP 4 — Run Your First Deterministic Prompt**

Create **lab01_test.py**:

```python
from deterministic_prompt import build_prompt
from deterministic_call import run_deterministic

p = build_prompt(
    actor="SQL Analyst",
    input="SELECT TOP 5 * FROM Employees;",
    mission="Explain this SQL step-by-step.",
    memory="You know SQL at expert level.",
    assets="Tables: Employees",
    actions="Do not invent columns.",
    prompt="Explain the SQL clearly."
)

output = run_deterministic(p)
print(output)
```

Run it **twice**:

```bash
python lab01_test.py
python lab01_test.py
```

**Expected:**
Outputs should be **identical byte-for-byte**.

This confirms deterministic behavior.

---

# 4. 🔍 **STEP 5 — The Real Test: Drift Detection**

Modify the prompt (but not the wrapper) slightly:

```python
p = build_prompt(
    actor="SQL Analyst",
    input="SELECT COUNT(*) FROM Employees;",
    mission="Explain the SQL deterministically.",
    memory="Employees table exists.",
    assets="Columns: EmployeeID",
    actions="No hallucination. Stay within schema.",
    prompt="Explain this SQL."
)
```

Run again twice.

Verify that:

* format ALWAYS matches
* EVV section is always applied
* no hallucinated columns appear

---

# 5. 🧩 **STEP 6 — Add EVV inside the model output (advanced)**

This is optional but powerful:

### Add this to the bottom of TEMPLATE:

```text
Before final answer:
- If any uncertainty exists, explicitly mark TODO.
- If any missing fields exist, request clarification.
- If forced to assume anything, list assumptions.
```

This makes the LLM self-police.

---

# 6. 🧠 **STEP 7 — Apply to a Real Enterprise Use Case**

Try any of these:

### **A. Explain an Unanet SQL view**

Paste a row from your PLM Excel, or an SQL view.

### **B. Explain a messy meeting transcript**

Give a random Teams .vtt snippet.

### **C. Break down a Data Dictionary section**

Feed the SQL metadata.

### **D. Explain a workflow for Resume Sorter AI**

Give the JD + one resume.

### **E. Explain a CSSWEB download function**

Paste your Python snippet.

Each of these will produce:

* Deterministic explanation
* Structured breakdown
* Zero hallucination
* Repeatable output

This is the entire purpose of Skill #1.

---

# 🎉 **LAB COMPLETE**

You now have:

✔ A deterministic Python wrapper for AIM→MAAP→EVV
✔ Deterministic API call function
✔ Repeatable outputs using seeds
✔ No reliance on ChatGPT Web
✔ Ready to embed this into MCP tools, RAG workflows, or Unanet pipelines

---

# 🚀 **NEXT OPTIONS (choose one)**

1. **Micro-Lab 02 — Policy Prompting & Guardrails**
2. **Micro-Lab 03 — Deterministic SQL Generation (with EVV)**
3. **Micro-Lab 04 — Deterministic Data Pipeline Design (Unanet PLM example)**
4. **Micro-Lab 05 — Deterministic Reasoning for Multi-Agent Systems**

Which one do you want next?
