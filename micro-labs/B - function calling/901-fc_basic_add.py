import json

from openai import OpenAI

client = OpenAI()

def add(a: int, b:int) -> int:
    return a + b

tools = [
    {
        "type": "function",
        "function": {
            "name": "add",
            "description": "Add two integers and return the sum",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "integer",
                        "description": "The first integer to add"
                    },
                    "b": {
                        "type": "integer",
                        "description": "The second integer to add"
                    }
                },
                "required": ["a", "b"],
            },
        },
    }
    
]



def main():
    # user_message = {"role": "user", "content": "Add 3 and 5"}
    user_message = {"role": "user", "content": "Use the add tool that I (Iqbal) described in tools=[...]. with 40 and 30"}

    first_response = client.chat.completions.create(
        model="gpt-4.1",
        messages = [user_message],
        tools=tools
    )
    
    message = first_response.choices[0].message

    if not message.tool_calls:
        print("No tool call was made.")
        print("Response:", message.content)
        return
    
    tool_call = message.tool_calls[0]
    fn_name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)  # arguments arrive as a JSON string

    print("Tool call requested by model:")
    print("  name:", fn_name)
    print("  args:", args)

    # 6 Execute the requested function
    if fn_name == "add":
        result = add(**args) # unpack args dict into function call
    else:
        raise ValueError(f"Unknown function requested: {fn_name}")
    
    # 7 Send the function result back to the model
    tool_message = {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": str(result)
    }

    final_response = client.chat.completions.create(
        model="gpt-4.1",
        messages = [user_message, message, tool_message],
    )

    print("Final response from model:")
    print(final_response.choices[0].message.content)

if __name__ == "__main__":
    main()
