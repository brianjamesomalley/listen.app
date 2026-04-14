#!/usr/bin/env python3
"""
listen_server.py
Flask API — receives browser context, extracts leads, generates emails.
Pairs with PROTOCOL.py and CHILL_AF_BACKEND.py.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import json
import os
from datetime import datetime
from listener import Listener
from database import init_db, log_lead, log_email, get_ignored_leads

app = Flask(__name__)
CORS(app)

client   = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
listener = Listener()

# ── RECEIVE BROWSER CONTEXT ───────────────────────────────────────

@app.route("/context", methods=["POST"])
def receive_context():
    data      = request.json
    url       = data.get("url", "")
    page_text = data.get("text", "")[:3000]  # cap tokens
    user_id   = data.get("user_id", "default")

    lead = extract_lead(url, page_text)
    if lead and lead.get("is_lead"):
        log_lead(user_id, lead)
        listener.notify(user_id, lead)

    return jsonify({"lead": lead})

# ── EXTRACT LEAD VIA CLAUDE ───────────────────────────────────────

def extract_lead(url, page_text):
    prompt = f"""
You are a B2B lead extraction engine.
Analyze this webpage and extract a sales lead if one exists.

URL: {url}
Page content: {page_text}

Respond ONLY in JSON with these fields (no markdown, no explanation):
{{
  "company": "company name or null",
  "contact_name": "decision maker name or null",
  "contact_title": "their title or null",
  "email": "email if found or null",
  "pain_point": "one sentence — what problem they likely have",
  "is_lead": true or false
}}

If this is not a business page with an identifiable decision maker, return is_lead: false.
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip()

    # fix: added robust JSON cleanup before parsing
    raw = raw.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        parsed = json.loads(raw)
        return parsed
    except json.JSONDecodeError:
        print(f"[extract_lead] JSON parse failed. Raw response:\n{raw}")
        return None

# ── GENERATE OUTREACH EMAIL ───────────────────────────────────────

@app.route("/email", methods=["POST"])
def generate_email():
    data       = request.json
    lead       = data.get("lead", {})
    user_voice = data.get("voice", "professional but human, brief, no jargon")
    user_name  = data.get("user_name", "Brian")
    user_email = data.get("user_email", "")
    user_id    = data.get("user_id", "default")

    prompt = f"""
Write a cold outreach email from {user_name} ({user_email}) to {lead.get('contact_name', 'the team')} 
at {lead.get('company')}.

Their likely pain point: {lead.get('pain_point')}
Voice: {user_voice}
Length: under 100 words
Goal: get a 10 minute meeting

Return ONLY the email in this format (no explanation):
Subject: [subject line]

[body]
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    email_text = response.content[0].text
    log_email(user_id, lead.get("company"), email_text)

    return jsonify({"email": email_text})

# ── ACKNOWLEDGE LEAD (remove from ignored queue) ──────────────────

@app.route("/acknowledge", methods=["POST"])
def acknowledge():
    data    = request.json
    user_id = data.get("user_id", "default")
    company = data.get("company", "")
    listener.acknowledge(user_id, company)
    return jsonify({"status": "acknowledged", "company": company})

# ── GET IGNORED LEADS (for dashboard / Vince) ─────────────────────

@app.route("/ignored", methods=["GET"])
def ignored():
    user_id = request.args.get("user_id", "default")
    leads   = get_ignored_leads(user_id)
    return jsonify({"ignored": leads})

# ── HEALTH CHECK ──────────────────────────────────────────────────

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "LISTEN is running"})

# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    app.run(port=5001, debug=True)
