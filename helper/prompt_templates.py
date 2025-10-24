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
    ),
    "welcome": (
        "Write a warm welcome email to {recipient_name} about {email_topic}.\n"
        "Context: {context}\n"
        "Tone: {tone}\n"
        "Start with a subject line. Thank them for joining, introduce your brand/service, and guide them on what to expect. Call-to-action: {goal}.\n"
        "Begin your response with the subject line as the first line. "
        "DO NOT include any placeholder text like [....], (...), or blanks. "
        "Fill in all relevant details as if you know them.\n"
        "Do not include any personal sign-off (like 'Best regards') — the system will add it automatically."
    ),
    "promotional": (
        "Write a promotional email to {recipient_name} about {email_topic}.\n"
        "Context: {context}\n"
        "Tone: {tone}\n"
        "Highlight the benefits, create urgency, and include a clear call-to-action: {goal}.\n"
        "Begin your response with the subject line as the first line. "
        "DO NOT include any placeholder text like [....], (...), or blanks. "
        "Fill in all relevant details as if you know them.\n"
        "Do not include any personal sign-off (like 'Best regards') — the system will add it automatically."
    ),
    "newsletter": (
        "Write an engaging newsletter email to {recipient_name} about {email_topic}.\n"
        "Context: {context}\n"
        "Tone: {tone}\n"
        "Share valuable updates, news, or insights. Keep it informative and engaging. Call-to-action: {goal}.\n"
        "Begin your response with the subject line as the first line. "
        "DO NOT include any placeholder text like [....], (...), or blanks. "
        "Fill in all relevant details as if you know them.\n"
        "Do not include any personal sign-off (like 'Best regards') — the system will add it automatically."
    ),
    "re_engagement": (
        "Write a re-engagement email to {recipient_name} about {email_topic}.\n"
        "Context: {context}\n"
        "Tone: {tone}\n"
        "The recipient hasn't engaged recently. Remind them of the value you provide and encourage them to reconnect. Call-to-action: {goal}.\n"
        "Begin your response with the subject line as the first line. "
        "DO NOT include any placeholder text like [....], (...), or blanks. "
        "Fill in all relevant details as if you know them.\n"
        "Do not include any personal sign-off (like 'Best regards') — the system will add it automatically."
    ),
    "thank_you": (
        "Write a heartfelt thank you email to {recipient_name} about {email_topic}.\n"
        "Context: {context}\n"
        "Tone: {tone}\n"
        "Express genuine gratitude and appreciation. Call-to-action: {goal}.\n"
        "Begin your response with the subject line as the first line. "
        "DO NOT include any placeholder text like [....], (...), or blanks. "
        "Fill in all relevant details as if you know them.\n"
        "Do not include any personal sign-off (like 'Best regards') — the system will add it automatically."
    ),
    "event_invitation": (
        "Write an event invitation email to {recipient_name} about {email_topic}.\n"
        "Context: {context}\n"
        "Tone: {tone}\n"
        "Clearly describe the event details (what, when, where, why), highlight the benefits of attending, and encourage RSVP. Call-to-action: {goal}.\n"
        "Begin your response with the subject line as the first line. "
        "DO NOT include any placeholder text like [....], (...), or blanks. "
        "Fill in all relevant details as if you know them.\n"
        "Do not include any personal sign-off (like 'Best regards') — the system will add it automatically."
    ),
    "feedback_request": (
        "Write a polite feedback request email to {recipient_name} about {email_topic}.\n"
        "Context: {context}\n"
        "Tone: {tone}\n"
        "Ask for their honest opinion or review. Explain why their feedback matters. Call-to-action: {goal}.\n"
        "Begin your response with the subject line as the first line. "
        "DO NOT include any placeholder text like [....], (...), or blanks. "
        "Fill in all relevant details as if you know them.\n"
        "Do not include any personal sign-off (like 'Best regards') — the system will add it automatically."
    ),
    "product_announcement": (
        "Write a product announcement email to {recipient_name} about {email_topic}.\n"
        "Context: {context}\n"
        "Tone: {tone}\n"
        "Introduce the new product/service, highlight key features and benefits, and drive excitement. Call-to-action: {goal}.\n"
        "Begin your response with the subject line as the first line. "
        "DO NOT include any placeholder text like [....], (...), or blanks. "
        "Fill in all relevant details as if you know them.\n"
        "Do not include any personal sign-off (like 'Best regards') — the system will add it automatically."
    ),
    "seasonal_campaign": (
        "Write a seasonal campaign email to {recipient_name} about {email_topic}.\n"
        "Context: {context}\n"
        "Tone: {tone}\n"
        "Tie the message to the season or holiday. Create excitement and urgency with time-limited offers. Call-to-action: {goal}.\n"
        "Begin your response with the subject line as the first line. "
        "DO NOT include any placeholder text like [....], (...), or blanks. "
        "Fill in all relevant details as if you know them.\n"
        "Do not include any personal sign-off (like 'Best regards') — the system will add it automatically."
    ),
    "nurture_sequence": (
        "Write a lead nurturing email to {recipient_name} about {email_topic}.\n"
        "Context: {context}\n"
        "Tone: {tone}\n"
        "Guide the recipient through their decision journey with valuable information addressing their needs. Call-to-action: {goal}.\n"
        "Begin your response with the subject line as the first line. "
        "DO NOT include any placeholder text like [....], (...), or blanks. "
        "Fill in all relevant details as if you know them.\n"
        "Do not include any personal sign-off (like 'Best regards') — the system will add it automatically."
    )
}
