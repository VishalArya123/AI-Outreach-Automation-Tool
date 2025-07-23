from helper.gemini_helper import generate_email_with_gemini
from helper.prompt_templates import EMAIL_PROMPT_TEMPLATES
from helper.image_generator import generate_image
from helper.mailjet_helper import send_test_email

# Step 1: Compose the prompt using template
prompt = EMAIL_PROMPT_TEMPLATES["follow_up"].format(
    topic="our new product release", name="Alex", tone="enthusiastic"
)

# Step 2: Generate the email text with Gemini
email_text = generate_email_with_gemini(prompt)
print("\nGenerated Email:\n", email_text)

# Step 3: Generate a matching image
image_prompt = "Excited team unveiling a new technology product on a stage"
image_path = generate_image(image_prompt)
print("\nImage saved to:", image_path)

# Step 4: Send the email using Mailjet
subject, body = email_text.split('\n', 1) if '\n' in email_text else ("[No Subject]", email_text)
status, response = send_test_email(
    recipient="vishal080804@gmail.com",  # Replace with an actual email for a real test
    subject=subject.strip(),
    body=body.strip()
)
print(f"\nMailjet status: {status}")
print(response)
