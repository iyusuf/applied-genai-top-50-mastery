# Micro-Lab 01 — Function Calling Basics (Lab Steps)

**Goal:**
Implement and run a minimal Python script that demonstrates **OpenAI function calling** with a single tool: `add(a, b)`.

This file contains only the **how-to steps and code**, separated from the AIM–MAAP–EVV framing.

---

## 1. Create the Lab Folder

From the repository root:

```bash
mkdir -p micro-labs/01-function-calling-basics
cd micro-labs/01-function-calling-basics
```

(Optional) Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

Install dependencies:

```bash
pip install openai
```

Set the API key (example for Unix shells):

```bash
export OPENAI_API_KEY="sk-..."  # Windows: set OPENAI_API_KEY=sk-...
```

---

## 2. Create `fc_basic_add.py`

Create a new file: `fc_basic_add.py`

```python
from openai import OpenAI

client = OpenAI()


# 1. Define the concrete Python function
def add(a: int, b: int) -> int:
    return a + b


# 2. Describe the function as a tool for the model
tools = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two integers and return the sum.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "integer", "description": "First integer"},
                    "b": {"type": "integer", "description": "Second integer"},
                },
                "required": ["a", "b"],
            },
        },
    }
]


def main():
    # 3. Initial request from the practitioner
    user_message = {"role": "user", "content": "Please add 50 and 70."}

    # 4. Ask the model, giving it the tool definition
    first_response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[user_message],
        tools=tools,
    )

    message = first_response.choices[0].message

    # 5. Inspect tool call
    if not message.tool_calls:
        print("Model did not request any tool call.")
        print("Response:", message.content)
        return

    tool_call = message.tool_calls[0]
    fn_name = tool_call.function.name
    args = tool_call.function.arguments  # this is a dict

    print("Tool call requested by model:")
    print("  name:", fn_name)
    print("  args:", args)

    # 6. Execute the tool locally
    if fn_name == "add":
        result = add(**args)
    else:
        raise ValueError(f"Unknown tool: {fn_name}")

    # 7. Send result back to the model as a 'tool' message
    tool_message = {
        "role": "tool",
        "tool_name": fn_name,
        "content": str(result),
    }

    final_response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            user_message,
            message,
            tool_message,
        ],
    )

    print("Final model answer:")
    print(final_response.choices[0].message.content)


if __name__ == "__main__":
    main()
```

---

## 3. Run the Lab

From `micro-labs/01-function-calling-basics`:

```bash
python fc_basic_add.py
```

Expected behavior:

* The script prints the tool call requested by the model, including arguments.
* Then it prints a final natural language answer that uses the result of `add(50, 70)`.

---

## 4. Variations and Experiments

### 4.1 Change Inputs

Modify the user message:

```python
user_message = {"role": "user", "content": "Please add 123 and 456."}
```

Run the script again:

* Observe the new `args` in the tool call.
* Confirm that the final answer reflects `123 + 456`.

### 4.2 Intentionally Break the Tool

Temporarily modify `add`:

```python
def add(a: int, b: int) -> int:
    return a - b  # incorrect on purpose
```

Run again and observe:

* The model trusts the tool result.
* This shows that **application correctness is enforced in code**, not by the model.

Restore the correct implementation afterward.

---

## 5. Optional Extension — Second Tool

As an optional deeper step:

1. Add a second function, for example:

   ```python
   def multiply(a: int, b: int) -> int:
       return a * b
   ```

2. Extend the `tools` list with a new tool definition for `multiply`.

3. Change the prompt:

   ```python
   user_message = {
       "role": "user",
       "content": "Add 10 and 20, then multiply the result by 3."
   }
   ```

4. Inspect how the model responds:

   * Does it request multiple tool calls?
   * Does it choose the right tool?

This prepares the ground for **multi-tool** and later **multi-agent** orchestration.

---

## 6. Link Back to AIM–MAAP–EVV

After completing the steps in this file:

* Open `01-aim-maap-evv.md`.
* Fill in or update EVV notes based on what actually happened:

  * What worked
  * What failed
  * Key lessons about tool design and correctness

This keeps the separation:

* `01-aim-maap-evv.md` → framing + EVV
* `01-lab-steps.md` → hands-on execution

---
