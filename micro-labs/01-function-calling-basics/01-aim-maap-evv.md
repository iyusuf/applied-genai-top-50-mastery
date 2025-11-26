# Micro-Lab 01 — Function Calling Basics (AIM–MAAP–EVV)

**Category:** B. Function Calling & Tooling  
**Skill focus:** OpenAI function calling / tool use hello-world  
**Duration:** ~45–60 minutes  
**Practitioner level:** Comfortable with Python, new to function calling

---

## AIM — Framing the Lab

### A — Actor

The practitioner is:

- A hands-on applied AI engineer (Python, backend, APIs).
- Learning function calling as the foundation for future agents and tool-using systems.
- Working in a controlled, local environment (no complex infrastructure required).

### I — Input

**Required starting assets:**

- Python 3.10+  
- An OpenAI API key set as `OPENAI_API_KEY` in the environment  
- A terminal + editor (VS Code recommended)  
- Network access to the OpenAI API

**This lab does NOT assume:**

- Prior experience with function calling / tool calling  
- Prior experience with LangGraph, Autogen, or any agent framework

### M — Mission

Build a **minimal, working function calling example** where:

1. A **Python function** is defined as a **tool**.  
2. The model decides to call the tool.  
3. The practitioner’s Python code **executes the function locally**.  
4. The result is sent back to the model, which then produces a final answer.

This is the “Hello World” of function calling — all future multi-tool and multi-agent patterns build on this.

---

## MAAP — How This Lab Fits the System

### M — Memory

- This lab becomes the canonical **Function Calling Hello World** for the repository.
- EVV notes and code are kept under `micro-labs/01-function-calling-basics/` and `notes/`.

### A — Assets

- `fc_basic_add.py` — main script for the lab  
- EVV notes (e.g., `fc_basic_add_evv.md`)  
- Terminal logs or screenshots (optional)

### A — Actions

- Run the script with different inputs.  
- Inspect the model’s `tool_call`.  
- Intentionally break the function to see how the system behaves.  
- Restore correctness and re-validate.

### P — Prompt

Canonical user prompt for this lab:

> “Please add 50 and 70.”

This prompt is intentionally simple so that cognitive load stays on **understanding tool calling**, not on complex language or business rules.

---

## EVV — Evaluate · Validate · Verify

### E — Evaluate

- Did the model actually request a `tool_call` for `add`?  
- Were the arguments correct (for example, `a=50`, `b=70`)?  
- Did the final answer use the tool result?

### V — Validate

Run multiple variants:

- Change numbers (for example, 10 + 20, 123 + 456).  
- Confirm that:
  - The tool call arguments match the new inputs.  
  - The final answer matches the function’s return.

### V — Verify

- Intentionally introduce a bug into the `add` function (for example, return `a - b`).  
- Observe that:
  - The model trusts the tool output.  
  - Logical correctness is the responsibility of the practitioner.

The lab is considered **verified** when:

- The practitioner can explain, in plain language:
  - What a tool is.  
  - How the model calls a tool.  
  - How Python executes the function.  
  - How the result returns to the conversation.
- EVV notes are written and saved (for example, `notes/fc_basic_add_evv.md`).

---
