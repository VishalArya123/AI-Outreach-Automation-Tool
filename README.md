# AI Outreach Automation Tool — Day 1 Setup

**Date:** Wednesday, July 23, 2025

---

## Project Overview

This repository contains the foundational setup for an automated, AI-powered outreach tool. It will generate personalized emails and images, schedule campaigns, and ensure legal compliance — all using free-tier APIs and tools.

---

## 1. Features to be Developed

- Natural language email prompt handling  
- AI-generated email body (OpenAI free tier)  
- Matching image creation (Hugging Face, free API)  
- Automated email sending, initially via Mailjet's free tier  
- Scheduler setup (sending emails at intervals)  
- Built-in legal compliance (CAN-SPAM, GDPR)  
- User interface with Streamlit  

---

## 2. Project Structure

```
outreach-ai-app/
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── helper/           # For additional modules/utilities
└── README.md
```

---

## 3. Environment Setup

### a) Requirements

- **Python 3.9+**  
- **pip** (Python package installer)  
- **git** (for version control, optional but recommended)  

### b) Dependency Installation

Install essential libraries:
```bash
pip install streamlit requests python-dotenv apscheduler sqlalchemy
```

### c) Project Initialization

1. Clone/init the repo:
    ```bash
    git init
    ```

2. Set up **`.gitignore`**:
    ```
    .env
    __pycache__/
    *.pyc
    .streamlit/
    email_jobs.sqlite
    ```

3. Create a **`.env`** file (for API keys and secrets):
    ```
    OPENAI_API_KEY=your_openai_key_here
    HUGGINGFACE_API_KEY=your_huggingface_key_here
    MAILJET_API_KEY=your_mailjet_key_here
    MAILJET_SECRET_KEY=your_mailjet_secret_key_here
    SENDER_NAME=Vishal Arya Dacha
    SENDER_ADDRESS=Plot number 90,road number 8, maple homes colony, kapra, Ecil, Hyderabad, Telangana
    ```
    *Do not share this file or commit it to version control.*

---

## 4. API Key Setup and Testing

- [OpenAI API](https://platform.openai.com/): Get your free API key and add it to `.env`.  
- [Hugging Face API](https://huggingface.co/settings/tokens): Generate your token and add to `.env`.  
- [Mailjet API](https://app.mailjet.com/account/api_keys): Get your API key/secret.  

Test your key loading with:
```python
import os
print("OpenAI loaded:", bool(os.getenv("OPENAI_API_KEY")))
print("Mailjet loaded:", bool(os.getenv("MAILJET_API_KEY")))
```

---

## 5. Legal Compliance

All outreach emails will include:

- **Sender:** Vishal Arya Dacha  
- **Address:** Plot number 90,road number 8, maple homes colony, kapra, Ecil, Hyderabad, Telangana  
- **Unsubscribe/Privacy Policy Links:** (Placeholders for now)  
- Legal footer template (to be included in all emails for compliance with CAN-SPAM and GDPR)  

---

## 6. Next Steps

- Day 2: Integrate GPT prompt setup, Hugging Face image generation, Mailjet test mailer, and fallback logic.  
- Day 1 support: If any installation/config issues arise, copy-paste error messages for direct help.

---

**Contact for Legal or Branding Questions:**  
*Placeholders will be used until actual links are provided.*

---

**Progress powered by OpenAI, Hugging Face, Mailjet, and Streamlit.**