import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import os
import uuid

from helper.gemini_helper import generate_email_with_gemini, generate_image_description_with_gemini
from helper.prompt_templates import EMAIL_PROMPT_TEMPLATES
from helper.image_generator import generate_image
from helper.mailjet_helper import send_test_email
from helper.scheduler_helper import schedule_batch_emails, get_all_jobs, cancel_campaign

st.set_page_config(page_title="AI Outreach Tool", page_icon="📧", layout="wide")
st.title("📧 AI Outreach Automation Tool")

# Initialize session state for email previews
if 'email_previews' not in st.session_state:
    st.session_state.email_previews = []
if 'generation_done' not in st.session_state:
    st.session_state.generation_done = False

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
    
    # Updated template type with more categories
    template_type = st.selectbox(
        "Template Type", 
        list(EMAIL_PROMPT_TEMPLATES.keys()),
        format_func=lambda x: x.replace("_", " ").title()
    )
    
    tone = st.selectbox("Email Tone", ["professional", "friendly", "enthusiastic", "warm", "casual", "formal"])
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

    if st.button("Generate & Preview Emails"):
        if not (topic and goal and (image_description or ai_image_description) and sender_name and sender_title and sender_contact):
            st.error("Please complete all required fields (including sender details and at least one description).")
            st.stop()

        # Prepare emails for preview
        with st.spinner("Generating email previews..."):
            start_dt = datetime.combine(start_date, start_time)
            end_dt = datetime.combine(end_date, end_time)
            email_previews = []

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
                img_path, fallback_description = generate_image(image_description)

                # Handle image generation failure
                if img_path is None:
                    st.error("Failed to generate or download a fallback image. Please try again.")
                    st.stop()

                # Store preview data
                email_previews.append({
                    "recipient_name": entry["Names"],
                    "recipient_email": entry["Emails"],
                    "subject": subject.strip(),
                    "body": body.strip(),
                    "img_path": img_path,
                    "fallback_description": fallback_description
                })

            # Save to session state
            st.session_state.email_previews = email_previews
            st.session_state.generation_done = True
            st.success("✅ Emails generated! Review and edit them below.")

    # Display editable previews
    if st.session_state.generation_done and st.session_state.email_previews:
        st.header("📝 Review & Edit Your Emails")
        st.info("✏️ You can edit the subject and body of each email before sending. Changes are automatically saved.")
        
        for idx, preview in enumerate(st.session_state.email_previews):
            with st.expander(f"✉️ Email for {preview['recipient_name']} <{preview['recipient_email']}>", expanded=True):
                st.subheader("Subject Line")
                # Editable subject
                edited_subject = st.text_input(
                    f"Subject for {preview['recipient_name']}", 
                    value=preview["subject"],
                    key=f"subject_{idx}"
                )
                st.session_state.email_previews[idx]["subject"] = edited_subject
                
                st.subheader("Email Body")
                # Editable body
                edited_body = st.text_area(
                    f"Body for {preview['recipient_name']}", 
                    value=preview["body"],
                    height=300,
                    key=f"body_{idx}"
                )
                st.session_state.email_previews[idx]["body"] = edited_body
                
                st.subheader("Attached Image")
                if os.path.exists(preview["img_path"]):
                    st.image(preview["img_path"], caption="Email Image", use_container_width=True)
                else:
                    st.error(f"Image file {preview['img_path']} not found.")
                if preview["fallback_description"]:
                    st.warning(
                        f"Note: We have exceeded our image generation tool's monthly credits, so we are providing an alternative image that closely aligns with your purpose: "
                        f"\"{preview['fallback_description']}\" Sorry for the inconvenience."
                    )

        # Confirmation button to schedule emails
        st.markdown("---")
        if st.button("✅ Confirm and Schedule Emails", type="primary"):
            with st.spinner("Scheduling emails..."):
                start_dt = datetime.combine(start_date, start_time)
                end_dt = datetime.combine(end_date, end_time)
                scheduled_emails = 0
                
                for preview in st.session_state.email_previews:
                    campaign_id = str(uuid.uuid4())
                    # Schedule batch emails for this recipient
                    schedule_batch_emails(
                        send_func=send_test_email,
                        start_datetime=start_dt,
                        end_datetime=end_dt,
                        total_emails=total_emails,
                        campaign_id=campaign_id,
                        recipient=preview["recipient_email"],
                        subject=preview["subject"],
                        body=preview["body"],
                        image_path=preview["img_path"],
                        sender_name=sender_name,
                        sender_title=sender_title,
                        sender_contact=sender_contact
                    )
                    scheduled_emails += total_emails
                
                st.success(f"✅ {scheduled_emails} emails scheduled for {len(email_targets)} recipients.")
                
                # Reset state
                st.session_state.email_previews = []
                st.session_state.generation_done = False
                st.balloons()
