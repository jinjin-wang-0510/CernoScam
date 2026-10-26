# 🛡️ ScamSnap

**Snap it. Scan it. Stay safe.**

AI-powered scam detection for messages, emails and screenshots — upload a screenshot and let Gemini flag the red flags.

## Features

- 📸 Upload an SMS, WhatsApp, email, job-offer, or bank-alert screenshot
- 🤖 Gemini multimodal AI analysis with structured risk output
- 🎯 Risk score (0–100), risk level, and AI confidence
- 💼 Scam category classification (phishing, payment scam, fake job, banking scam, etc.)
- 🚩 Red flag detection with severity-coded explanations
- 🔍 Red Flag Overlay panel highlighting suspicious content
- 🔗 URL heuristic analysis (no suspicious links are ever visited)
- ✅ Clear, actionable "What should I do?" safety guidance
- 🎬 Demo Mode with 3 built-in example scenarios (no screenshot needed)
- 📊 Session scan statistics
- 🔒 Screenshots are never saved to disk

## Tech Stack

- Python
- Streamlit
- Google Gemini API (`google-genai`)
- Pillow
- python-dotenv

## Installation

```bash
pip install -r requirements.txt
```

## API Key Setup

1. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).
2. Copy `.env.example` to `.env`:

   ```bash
   cp .env.example .env
   ```

3. Open `.env` and set your key:

   ```text
   GEMINI_API_KEY=your_actual_api_key
   ```

## Run

```bash
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## Demo Instructions

No screenshot handy? Toggle **Demo Mode** in the sidebar and pick one of three built-in scenarios:

1. 💼 Fake Job Scam
2. 🏦 Fake Bank/KYC Scam
3. 📦 Suspicious Delivery Message

Click **🔍 SCAN FOR SCAMS** and the same Gemini-powered analysis pipeline runs end-to-end — risk score, category, red flags, and recommended actions.

---

*AI results are advisory and should be independently verified. ScamSnap does not store uploaded screenshots and never visits suspicious URLs.*
