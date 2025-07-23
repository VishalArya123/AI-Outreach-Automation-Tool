import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import os
import uuid

from helper.gemini_helper import generate_email_with_gemini, generate_image_description_with_gemini
from helper.prompt_templates import EMAIL_PROMPT_TEMPLATES
from helper.image_generator import generate_image
from helper.mailjet_helper import send_test_email
from helper.scheduler_helper import schedule_batch_emails, get_all_jobs,cancel_campaign

st.set_page_config(page_title="AI Outreach Tool", page_icon="📧", layout="wide")
st.title("📧 AI Outreach Automation Tool")

# --- Campaign Dashboard ---
st.sidebar.header("📊 Campaign Dashboard")
jobs = get_all_jobs()
if jobs:
    for job_id, job in sorted(jobs.items()):
        st.sidebar.write(f"🕓 {job['send_time'].strftime('%Y-%m-%d %H:%M')} | {job['status']} | {job['recipient']}")
else:
    st.sidebar.info("No campaigns scheduled yet.")

# --- Active Campaign Controls ---
st.sidebar.header("🎯 Active Campaigns")

campaign_ids = set(info['campaign_id'] for info in get_all_jobs().values())

for cid in sorted(campaign_ids):
    if st.sidebar.button(f"Cancel Campaign {cid}"):
        count = cancel_campaign(cid)
        st.sidebar.success(f"🛑 Canceled {count} scheduled emails for Campaign ID: {cid}")


# --- Sender Details ---
st.header("Sender Details")
col_sender1, col_sender2, col_sender3 = st.columns(3)
with col_sender1:
    sender_name = st.text_input("Your Name", value=os.environ.get("SENDER_NAME", ""))
with col_sender2:
    sender_title = st.text_input("Your Title", placeholder="e.g., Business Development Manager")
with col_sender3:
    sender_contact = st.text_input("Contact Info", placeholder="e.g., 555-555-1234 | you@example.com")

st.markdown("---")

# --- Campaign Recipient Mode ---
st.header("Campaign Recipients")
recipient_mode = st.radio("Send to...", ["One person", "Many people (CSV/Excel upload)"])

if recipient_mode == "One person":
    recipient = st.text_input("Recipient Email")
    recipient_name = st.text_input("Recipient Name")
    email_targets = [{"Names": recipient_name, "Emails": recipient}]
else:
    st.info(
        "Upload a CSV or Excel file with required columns: **Names** (the recipient name) and **Emails** (the email address) for each contact."
    )
    upload_file = st.file_uploader("Upload file", type=["csv", "xlsx"])
    if upload_file:
        if upload_file.name.endswith(".csv"):
            df = pd.read_csv(upload_file)
        else:
            df = pd.read_excel(upload_file)
        if "Names" not in df.columns or "Emails" not in df.columns:
            st.error("Uploaded file must contain columns: Names, Emails")
            st.stop()
        email_targets = df.dropna(subset=["Names", "Emails"]).to_dict(orient="records")
        st.success(f"{len(email_targets)} contacts loaded.")
    else:
        email_targets = []

# --- Campaign & Message Details ---
if recipient_mode == "One person" or (recipient_mode == "Many people (CSV/Excel upload)" and email_targets):
    st.header("Email Message Details")

    topic = st.text_input("Email Topic", placeholder="What is the main subject of this email?")
    template_type = st.selectbox("Template Type", list(EMAIL_PROMPT_TEMPLATES.keys()))
    tone = st.selectbox("Email Tone", ["professional", "friendly", "enthusiastic", "warm"])
    context = st.text_area("Background/Context", placeholder="Describe the context or background for this email (optional).")
    goal = st.text_input("Goal / Call-to-Action", placeholder="What is the purpose or next step?")

    # AI-Generated image description if enabled
    use_ai_img_desc = st.checkbox("Let AI generate the email image description from other fields", value=True)
    if use_ai_img_desc and topic and context:
        ai_image_description = generate_image_description_with_gemini(topic=topic, context=context, goal=goal)
        st.info(f"AI Image Description: {ai_image_description}")
        image_description = ai_image_description
    else:
        image_description = st.text_input("Image Description", placeholder="Describe the visual to generate")

    # Batch scheduling controls
    total_emails = st.slider("Total Emails to Send (per recipient)", 1, 20, 1)
    start_date = st.date_input("Start Date", datetime.now().date())
    start_time = st.time_input("Start Time", datetime.now().time())
    end_date = st.date_input("End Date", (datetime.now() + timedelta(days=1)).date())
    end_time = st.time_input("End Time", (datetime.now() + timedelta(hours=1)).time())

    if st.button("Generate & Schedule Emails"):
        if not (topic and goal and (image_description or ai_image_description) and sender_name and sender_title and sender_contact):
            st.error("Please complete all required fields (including sender details and at least one description).")
            st.stop()

        # Prepare prompt and workflow for each recipient
        with st.spinner("Generating AI content and scheduling..."):
            start_dt = datetime.combine(start_date, start_time)
            end_dt = datetime.combine(end_date, end_time)
            scheduled_emails = 0

            for entry in email_targets:
                # Prepare prompt
                prompt = EMAIL_PROMPT_TEMPLATES[template_type].format(
                    recipient_name=entry["Names"],
                    email_topic=topic,
                    tone=tone,
                    context=context if context else "None provided",
                    goal=goal
                )
                email_text = generate_email_with_gemini(prompt)
                # Split subject/body on first line
                subject, body = email_text.split('\n', 1) if '\n' in email_text else ("No Subject", email_text)
                img_path = generate_image(image_description)

                campaign_id = str(uuid.uuid4())
                # Schedule batch emails for this recipient
                schedule_batch_emails(
                    send_func=send_test_email,
                    start_datetime=start_dt,
                    end_datetime=end_dt,
                    total_emails=total_emails,
                    campaign_id=campaign_id,
                    recipient=entry["Emails"],
                    subject=subject.strip(),
                    body=body.strip(),
                    image_path=img_path,
                    sender_name=sender_name,
                    sender_title=sender_title,
                    sender_contact=sender_contact
                )
                scheduled_emails += total_emails

            st.success(f"✅ {scheduled_emails} emails scheduled for {len(email_targets)} recipients.")

