import os
from dotenv import load_dotenv
from mailjet_rest import Client
import base64

load_dotenv()
api_key = os.getenv('MAILJET_API_KEY')
api_secret = os.getenv('MAILJET_SECRET_KEY')
sender_email = os.getenv('SENDER_MAIL')

def send_test_email(recipient, subject, body, image_path=None,
                    sender_name="", sender_title="", sender_contact=""):
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    # Compose sender info for footer
    sender_footer = f"<br><br>Best regards,<br>{sender_name}<br>{sender_title}<br>{sender_contact}"

    # Properly preserve newlines
    html_body = body.replace('\n', "<br>") + sender_footer

    msg = {
        "From": {"Email": sender_email, "Name": sender_name},
        "To": [{"Email": recipient, "Name": recipient}],
        "ReplyTo": {"Email": sender_email, "Name": sender_name},
        "Subject": subject,
        "TextPart": (body + f"\n\nBest regards,\n{sender_name}\n{sender_title}\n{sender_contact}"),
        "HTMLPart": html_body + f'<br><br><a href="https://yourdomain.com/unsubscribe">Unsubscribe</a>',
        "TrackOpens": "enabled",
        "TrackClicks": "enabled"
    }

    # Handle image inline/attachment
    if image_path:
        try:
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            encoded_image = base64.b64encode(image_bytes).decode()
            msg["HTMLPart"] += f'<br><img src="cid:embedded_image" alt="Embedded Image" style="max-width:100%;height:auto;">'
            msg["InlineAttachments"] = [{
                "ContentType": "image/png",
                "Filename": os.path.basename(image_path),
                "ContentID": "embedded_image",
                "Base64Content": encoded_image
            }]
            msg["Attachments"] = [{
                "ContentType": "image/png",
                "Filename": os.path.basename(image_path),
                "Base64Content": encoded_image
            }]
        except Exception as e:
            print(f"Error attaching image: {e}")

    try:
        result = mailjet.send.create({'Messages': [msg]})
        return result.status_code, result.json()
    except Exception as e:
        return 500, {"error": f"Failed to send email: {str(e)}"}
