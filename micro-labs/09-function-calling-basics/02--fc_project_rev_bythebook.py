import json

from openai import OpenAI

import json

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
    args = json.loads(tool_call.function.arguments)

    print("Tool call:")
    print("  name:", fn_name)
    print("  args:", args)

    if fn_name != "get_project_revenue":
        raise ValueError(f"Unexpected tool called: {fn_name}")

    project_id = args["project_id"]
    revenue = get_project_revenue(project_id)

    tool_message = {
        "role": "tool",
        "tool_call_id": tool_call.id,
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
