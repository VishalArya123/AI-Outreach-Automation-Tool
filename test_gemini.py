from helper.gemini_helper import generate_email_with_gemini
from helper.prompt_templates import EMAIL_PROMPT_TEMPLATES

prompt = EMAIL_PROMPT_TEMPLATES['follow_up'].format(
    topic="the new AI workflow", name="Priya", tone="friendly"
)
email_text = generate_email_with_gemini(prompt)
print("\nGenerated Email:\n", email_text)
