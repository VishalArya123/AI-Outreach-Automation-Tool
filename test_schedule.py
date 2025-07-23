from helper.scheduler_helper import schedule_email
from helper.mailjet_helper import send_test_email
from datetime import datetime, timedelta

# Example: schedule an email 2 minutes from now
future_time = datetime.now() + timedelta(minutes=2)
schedule_email(
    send_test_email,
    send_time=future_time,
    recipient="recipient@example.com",
    subject="Scheduled Test Email",
    body="This email was scheduled!"
)
