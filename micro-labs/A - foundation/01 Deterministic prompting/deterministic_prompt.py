# Template

TEMPLATE = """
AIM
A - {actor}
I - {input}
M - {mission}

MAAP
Memory: {memory}
Assets: {assets}
Actions: {actions}
Prompt: {prompt}

EVV - Deterministic Self-Check
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