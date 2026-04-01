from core.llm import call_llm

SYSTEM_PROMPT = """You are a professional building inspection expert.

Return the DDR as plain text with EXACTLY these top-level headings (each on its own line):
1. Property Issue Summary
2. Area-wise Observations
3. Probable Root Cause
4. Severity Assessment (with reasoning)
5. Recommended Actions
6. Additional Notes
7. Missing or Unclear Information

Under '2. Area-wise Observations', use area subheadings on their own line (e.g., Hall, Bedroom, Bathroom, Kitchen, Terrace, External Wall, WC, Parking).
Use '-' bullet points for items.
If something is missing, write 'Not Available'. If there is a conflict, state the conflict explicitly.
Do not invent any facts."""

def generate_ddr(context):
    with open("prompts/reasoning_prompt.txt", "r") as f:
        template = f.read()

    prompt = template.replace("{context}", context)

    return call_llm(prompt, system_prompt=SYSTEM_PROMPT)