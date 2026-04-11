import time
import threading
from datetime import datetime, timedelta
from playsound import playsound
import os

LISTEN_SOUND = os.path.join(os.path.dirname(__file__), "listen.mp3")

# Irritation levels — escalates the longer a lead is ignored
IRRITATION_SCHEDULE = [
    {"minutes": 5,  "message": "Hey. You have a lead."},
    {"minutes": 15, "message": "Still there. Lead is getting cold."},
    {"minutes": 30, "message": "LISTEN. You are ignoring money."},
    {"minutes": 60, "message": "This is embarrassing for both of us."},
]

class Listener:
    def __init__(self):
        self.pending = {}  # user_id -> list of {lead, time_found, irritation_level}
        self._start_watchdog()

    def notify(self, user_id, lead):
        if user_id not in self.pending:
            self.pending[user_id] = []
        self.pending[user_id].append({
            "lead": lead,
            "time_found": datetime.now(),
            "irritation_level": 0
        })
        self._play_listen()
        print(f"[LISTEN] New lead found: {lead.get('company')} — {lead.get('contact_name')}")

    def acknowledge(self, user_id, company):
        if user_id in self.pending:
            self.pending[user_id] = [
                p for p in self.pending[user_id]
                if p["lead"].get("company") != company
            ]

    def _play_listen(self):
        try:
            if os.path.exists(LISTEN_SOUND):
                threading.Thread(target=playsound, args=(LISTEN_SOUND,), daemon=True).start()
        except Exception as e:
            print(f"[LISTEN] Sound error: {e}")

    def _start_watchdog(self):
        def watch():
            while True:
                now = datetime.now()
                for user_id, leads in self.pending.items():
                    for pending in leads:
                        elapsed = (now - pending["time_found"]).total_seconds() / 60
                        level = pending["irritation_level"]
                        if level < len(IRRITATION_SCHEDULE):
                            threshold = IRRITATION_SCHEDULE[level]["minutes"]
                            if elapsed >= threshold:
                                msg = IRRITATION_SCHEDULE[level]["message"]
                                print(f"\n[LISTEN] {msg}")
                                print(f"  Company: {pending['lead'].get('company')}")
                                print(f"  Contact: {pending['lead'].get('contact_name')}")
                                self._play_listen()
                                pending["irritation_level"] += 1
                time.sleep(60)
        threading.Thread(target=watch, daemon=True).start()
