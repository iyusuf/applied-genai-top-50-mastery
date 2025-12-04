from openai import OpenAI
from deterministic_prompt import build_prompt

client = OpenAI()

def run_deterministic(prompt):
    response = client.responses.create(
        model="gpt-4.1-mini",     # or gpt-4.1/gpt-5.1/gpt-5.1-preview
        input=prompt,
        temperature=0,            # deterministic
        top_p=1,
        # seed=123,                 # ensures reproducibility
        max_output_tokens=300,
    )
    return response.output_text