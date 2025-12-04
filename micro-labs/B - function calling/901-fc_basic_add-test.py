import re
from openai import OpenAI

client = OpenAI()

# Same tool + function definition you used in fc_basic_add.py

def add(a: int, b: int) -> int:
    return a + b


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


def call_add_via_tool(a: int, b: int):
    """Helper: run the whole tool-calling flow and return (tool_call, final_message)."""
    user_message = {
        "role": "user",
        # "content": f"Use the add tool to add {a} and {b}, then tell me the result."
        "content": "What is the capital of France?"
    }

    first = client.chat.completions.create(
        model="gpt-4.1",
        messages=[user_message],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "add"}},
    )

    msg = first.choices[0].message
    tool_call = msg.tool_calls[0]
    fn_name = tool_call.function.name
    args = tool_call.function.arguments

    # Execute tool
    result = add(**args)

    tool_message = {
        "role": "tool",
        "tool_name": fn_name,
        "content": str(result),
    }

    final = client.chat.completions.create(
        model="gpt-4.1",
        messages=[user_message, msg, tool_message],
    )

    return tool_call, final.choices[0].message


# ---------- EVV TESTS ----------

def test_e_evaluate_tool_called_correctly():
    """E: Evaluate – did the model call the right tool with correct args?"""
    a, b = 40, 30
    tool_call, _ = call_add_via_tool(a, b)

    assert tool_call.function.name == "add"
    args = tool_call.function.arguments
    assert args["a"] == a
    assert args["b"] == b


def test_v_validate_result_correct():
    """V: Validate – is the numeric result correct end-to-end?"""
    a, b = 123, 456
    _, final_msg = call_add_via_tool(a, b)

    # Very simple extraction: look for the first integer in the final message
    numbers = list(map(int, re.findall(r"-?\d+", final_msg.content)))
    assert (a + b) in numbers, f"Expected {a + b} in final answer, got: {final_msg.content}"


def test_v_verify_wrong_implementation_would_be_caught():
    """
    V: Verify – thought experiment level:
    If add() was wrong, these tests would fail,
    proving we are not blindly trusting the model.
    """
    # Here we don't actually break add(); this test just documents the idea.
    # If you temporarily change add() to return a-b, the tests above will start failing.
    assert add(2, 3) == 5
