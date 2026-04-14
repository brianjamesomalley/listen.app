#!/usr/bin/env python3
“””
CHILL_AF_BACKEND.py
The server that processes sales meltdowns while drinking a michelada.

Architecture:

- Handles 10k concurrent crash-outs
- Logs every scream for posterity
- Sends zero fucks
- Pairs well with escape_hatch.py and its_over.py
- Vince Carter approved
“””

from flask import Flask, jsonify, request
import time
from datetime import datetime
import random

app = Flask(**name**)

# The chillest database in SaaS

CRASH_LOG = []

BACKEND_MOODS = [
“sipping michelada”,
“watching the game”,
“completely unbothered”,
“aggressively relaxed”,
“professionally indifferent”,
“chill AF”,
“not reading your emails”,
“on a hammock technically”,
]

USER_REACTIONS = [
“screamed at monitor”,
“threw mouse”,
“typed ‘I AM BAD AT SALES’”,
“unplugged computer”,
“called us a bad word”,
“stared into void for 4 minutes”,
“opened LinkedIn to update resume”,
“googled ‘is sales right for me’”,
“ate lunch at 10am out of stress”,
“texted mom”,
]

# ── CRASH HANDLER ─────────────────────────────────────────────────

@app.route(’/crash’, methods=[‘POST’])
def handle_crash():
“””
User’s machine is having a meltdown.
We log it. We laugh. We move on.
Frontend: unhinged.
Backend: *yawns*
“””
data = request.json
crash_event = {
“user_id”: data.get(‘user_id’),
“lead_ignored”: data.get(‘company’),
“vince_level”: data.get(‘vince_level’, ‘unknown’),
“crash_time”: datetime.now().isoformat(),
“user_reaction”: random.choice(USER_REACTIONS),
“backend_reaction”: “🍹 logged. moving on.”,
“fucks_given”: 0
}

```
CRASH_LOG.append(crash_event)

# Simulate chill AF response time
time.sleep(0.01) # barely a blink

return jsonify({
"status": "crash recorded",
"backend_vibe": "chill AF",
"user_reaction": crash_event["user_reaction"],
"message": "Your rep is having a moment. We'll be here when they calm down.",
"estimated_recovery_time": random.choice([
"3-5 business minutes",
"after they eat something",
"once Vince stops dunking",
"when they accept what they've done",
])
})
```

# ── CRASH STATS ───────────────────────────────────────────────────

@app.route(’/crash/stats’, methods=[‘GET’])
def crash_stats():
“”“Dashboard for watching the carnage”””
most_ignored = None
if CRASH_LOG:
companies = [c[“lead_ignored”] for c in CRASH_LOG if c.get(“lead_ignored”)]
if companies:
most_ignored = max(set(companies), key=companies.count)

```
return jsonify({
"total_crashes": len(CRASH_LOG),
"backend_status": random.choice(BACKEND_MOODS),
"uptime": "99.99% (crashes are client-side only)",
"fucks_given": 0,
"most_ignored_lead": most_ignored or "everyone equally",
"top_user_reaction": "screamed at monitor",
"vince_carter_status": "disappointed but not surprised",
})
```

# ── HEALTH CHECK ──────────────────────────────────────────────────

@app.route(’/health’, methods=[‘GET’])
def health():
return jsonify({
“status”: “chill AF”,
“temp”: “room temperature rosé”,
“load”: random.choice([“light breeze”, “gentle waves”, “hammock weather”]),
“vince”: “watching from halfcourt”,
“navi”: “screaming somewhere else right now”,
})

# ── FORGIVENESS ENDPOINT ──────────────────────────────────────────

@app.route(’/forgive’, methods=[‘POST’])
def forgive():
“””
User typed FORGIVE ME.
Backend does not judge.
Backend has seen worse.
“””
data = request.json
company = data.get(‘company’, ‘unknown lead’)
return jsonify({
“status”: “forgiven”,
“company”: company,
“message”: f”The backend forgives you for ignoring {company}.”,
“vince_says”: “this is your last chance”,
“backend_says”: “we don’t care either way honestly”,
})

# ── WIN ENDPOINT ──────────────────────────────────────────────────

@app.route(’/win’, methods=[‘POST’])
def log_win():
“””
Someone actually sent an email.
Backend is mildly impressed.
“””
data = request.json
return jsonify({
“status”: “dunk logged”,
“company”: data.get(‘company’),
“backend_reaction”: “hm. not bad.”,
“vince_reaction”: “nods slowly”,
“message”: “Email sent. Backend acknowledges your minimal effort with minimal enthusiasm.”,
})

if **name** == ‘**main**’:
print(”\n🍹 CHILL AF BACKEND RUNNING”)
print(” Port: 5003”)
print(” Vibe: unbothered”)
print(” Clients may be melting down.”)
print(” We are not.\n”)
app.run(port=5003, debug=False)
