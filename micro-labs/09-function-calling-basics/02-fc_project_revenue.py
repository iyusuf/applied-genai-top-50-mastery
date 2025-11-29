import json

from openai import OpenAI

client = OpenAI()

# Fake "database" of projects and their revenues

FAKE_PROJECT_DB = {
    "project_alpha": 150000,
    "project_beta": 250000,
    "project_gamma": 350000,
}



def get_project_revenue(project_id: str) -> float:
    """Return revenue for a given project ID, or raise KeyError if not found."""
    return FAKE_PROJECT_DB[project_id]

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_project_revenue",
            "description": "Get the revenue for a specific project.",
            "parameters": {
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "string",
                        "description": "The ID of the project to get the revenue for."
                    }
                },
                "required": ["project_id"]      
            },
        },
    }
]

def main():
    user_message = {
        "role": "user",
        "content": "Use the project revenue tool to tell me the revenue for project project_alpha."
    }

    first_response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[user_message],
        tools=tools,
        tool_choice={"type": "function", 
                     "function": {"name": "get_project_revenue"}
                    },
    )

    msg = first_response.choices[0].message

    if not msg.tool_calls:
        print("No tool call was made.")
        print("Response:", msg.content)
        return
    

    tool_call = msg.tool_calls[0]
    fn_name = tool_call.function.name
    fn_args = json.loads(tool_call.function.arguments)

    print("Tool call:")
    print("Function name:", fn_name)
    print("Function arguments:", fn_args)

    if fn_name != "get_project_revenue":
        raise ValueError(f"Unexpected function name: {fn_name}")
    
    project_id = fn_args["project_id"]

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
