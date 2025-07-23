# helper/prompt_templates.py

EMAIL_PROMPT_TEMPLATES = {
    "follow_up": (
        "Write a personalized follow-up email to {recipient_name} about {email_topic}.\n"
        "Context: {context}\n"
        "Tone: {tone}\n"
        "Goal: {goal}\n"
        "Begin your response with the subject line as the first line. "
        "DO NOT include any placeholder text like [....], (...), or blanks. "
        "Fill in all relevant details as if you know them.\n"
        "Do not include any personal sign-off (like 'Best regards') — the system will add it automatically."
    ),
    "reminder": (
        "Draft a polite reminder email for {recipient_name} about {email_topic}.\n"
        "Context: {context}\n"
        "The first line should be the subject. Use a {tone} tone. The action needed is: {goal}.\n"
        "Begin your response with the subject line as the first line. "
        "DO NOT include any placeholder text like [....], (...), or blanks. "
        "Fill in all relevant details as if you know them.\n"
        "Do not include any personal sign-off (like 'Best regards') — the system will add it automatically."
    ),
    "introduction": (
        "Write an introduction email to {recipient_name} about {email_topic}.\n"
        "Details: {context}\n"
        "Start with a subject line, followed by a concise, friendly intro. Add a clear call-to-action: {goal}.\n"
        "Begin your response with the subject line as the first line. "
        "DO NOT include any placeholder text like [....], (...), or blanks. "
        "Fill in all relevant details as if you know them.\n"
        "Do not include any personal sign-off (like 'Best regards') — the system will add it automatically."
    )
    # Add more as needed.
}
