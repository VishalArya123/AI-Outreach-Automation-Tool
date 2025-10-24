from helper.gemini_helper import generate_email_with_gemini
from helper.prompt_templates import EMAIL_PROMPT_TEMPLATES

prompt = EMAIL_PROMPT_TEMPLATES['follow_up'].format(
    recipient_name="Priya",
    email_topic="the new AI workflow",
    context="You recently attended our product demo showcasing the automated AI pipelines.",
    tone="friendly",
    goal="Encourage Priya to schedule a quick call to discuss integration opportunities."
)

email_text = generate_email_with_gemini(prompt)
print("\nGenerated Email:\n", email_text)
