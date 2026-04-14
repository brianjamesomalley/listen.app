#!/usr/bin/env python3
"""
listener.py
Tracks new leads and escalates irritation the longer they're ignored.
"""

import time
import threading
from datetime import datetime
from playsound import playsound
import os

LISTEN_SOUND = os.path.join(os.path.dirname(__file__), "sounds", "listen.mp3")

# Escalates the longer a lead sits untouched
IRRITATION_SCHEDULE = [
    {"minutes":  5, "message": "Hey. You have a lead."},
    {"minutes": 15, "message": "Still there. Lead is getting cold."},
    {"minutes": 30, "message": "LISTEN. You are ignoring money."},
    {"minutes": 60, "message": "This is embarrassing for both of us."},
]

class Listener:
    def __init__(self):
        # fix: added threading.Lock() — pending is written by notify/acknowledge
        # and read by the watchdog on separate threads
        self.pending = {}   # user_id -> list of {lead, time_found, irritation_level}
        self._lock   = threading.Lock()
        self._start_watchdog()

    def notify(self, user_id, lead):
        with self._lock:  # fix: lock around pending mutation
            if user_id not in self.pending:
                self.pending[user_id] = []
            self.pending[user_id].append({
                "lead":             lead,
                "time_found":       datetime.now(),
                "irritation_level": 0,
            })
        self._play_listen()
        print(f"[LISTEN] New lead: {lead.get('company')} — {lead.get('contact_name')}")

    def acknowledge(self, user_id, company):
        with self._lock:  # fix: lock around pending mutation
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

                # fix: snapshot pending under lock so notify/acknowledge
                # can't mutate the dict mid-iteration (RuntimeError: dictionary changed size)
                with self._lock:
                    snapshot = {
                        uid: list(leads)
                        for uid, leads in self.pending.items()
                    }

                for user_id, leads in snapshot.items():
                    for pending in leads:
                        elapsed = (now - pending["time_found"]).total_seconds() / 60
                        level   = pending["irritation_level"]

                        if level < len(IRRITATION_SCHEDULE):
                            threshold = IRRITATION_SCHEDULE[level]["minutes"]
                            if elapsed >= threshold:
                                msg = IRRITATION_SCHEDULE[level]["message"]
                                print(f"\n[LISTEN] {msg}")
                                print(f"  Company: {pending['lead'].get('company')}")
                                print(f"  Contact: {pending['lead'].get('contact_name')}")
                                self._play_listen()

                                # write irritation_level increment back under lock
                                with self._lock:
                                    for p in self.pending.get(user_id, []):
                                        if p["lead"].get("company") == pending["lead"].get("company"):
                                            p["irritation_level"] += 1
                                            break

                time.sleep(60)

        threading.Thread(target=watch, daemon=True).start()
