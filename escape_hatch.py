#!/usr/bin/env python3
"""
ESCAPE_HATCH.py - False Genuine Moments Generator
RNG-based alarm that makes you sound like a real human being
who has a life and is doing them a favor by talking to them.
"""

import random
import sqlite3
import time
import threading
import schedule
from datetime import datetime, timedelta
from playsound import playsound
from database import DB
import os

# ── EXIT LINES ────────────────────────────────────────────────────
EXIT_LINES = [
    "I gotta pick my kid up from school but real quick —",
    "I'm walking into a meeting in two minutes but I wanted to catch you —",
    "My phone's about to die but —",
    "I'm literally in the parking lot but —",
    "I've got thirty seconds before my next call but —",
    "I'm grabbing lunch but I saw your name and wanted to reach out —",
    "I can't talk long but this felt important —",
    "I'm between meetings but —",
    "Quick one before I lose you —",
    "I was just thinking about you guys and I've got sixty seconds —",
]

# ── 30 SECOND PITCHES ─────────────────────────────────────────────
PITCHES = [
    "Listen dot app. AI salesbot. Watches your browser, finds leads, writes the email, sends it. Irritating when you need it to be. That's the feature.",
    "We built a salesbot that says LISTEN like Navi from Zelda when you ignore a lead too long. It works. Middle management loves the dashboard. Salespeople actually use it.",
    "Passive lead gen from browser activity. AI writes the outreach. One key sends it. Your team closes more. You see everything. Nobody can say they didn't know about a lead.",
    "It's a sales co-pilot that won't leave you alone. Configurable irritation levels. Your team sets it. Or you set it for them.",
    "We replace the part of sales your team hates — the finding and the writing. They just approve and send. Conversion goes up. Excuses go down.",
]

PHONE_ALARM = os.path.join(os.path.dirname(__file__), "listen.mp3")

# ── GET HOTTEST LEAD ──────────────────────────────────────────────
def get_hottest_lead(user_id="default"):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT company, contact_name, pain_point
        FROM leads
        WHERE user_id = ? AND emailed = 0
        ORDER BY found_at ASC
        LIMIT 1
    """, (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"company": row[0], "contact": row[1], "pain": row[2]}
    return None

# ── GENERATE THE MOMENT ───────────────────────────────────────────
def generate_moment(user_id="default"):
    exit_line = random.choice(EXIT_LINES)
    pitch = random.choice(PITCHES)
    lead = get_hottest_lead(user_id)

    print("\n" + "="*60)
    print("📱 FALSE GENUINE MOMENT ACTIVATED")
    print("="*60)
    print(f"\n🎭 YOUR EXIT LINE:")
    print(f'   "{exit_line}"')
    print(f"\n⚡ YOUR 30 SECOND PITCH:")
    print(f'   "{pitch}"')

    if lead:
        print(f"\n🎯 HOTTEST LEAD RIGHT NOW:")
        print(f"   Company: {lead['company']}")
        print(f"   Contact: {lead['contact']}")
        print(f"   Their pain: {lead['pain']}")
        print(f"\n💡 PERSONALIZED CLOSER:")
        print(f'   "...and honestly given what you guys are dealing with at {lead["company"]}, this is exactly what you need."')

    print("\n" + "="*60)
    print("   Go. You've got 30 seconds. Sound busy. Be brief.")
    print("="*60 + "\n")

    # Trigger phone alarm
    try:
        if os.path.exists(PHONE_ALARM):
            playsound(PHONE_ALARM)
    except Exception as e:
        print(f"[alarm] {e}")

# ── RNG SCHEDULER ─────────────────────────────────────────────────
class EscapeHatch:
    def __init__(self, user_id="default", min_hour=9, max_hour=16, daily_count=3):
        self.user_id = user_id
        self.min_hour = min_hour
        self.max_hour = max_hour
        self.daily_count = daily_count
        self.fired_today = 0
        self.scheduled_times = []

    def schedule_day(self):
        """Pick random times within work hours for today"""
        self.fired_today = 0
        self.scheduled_times = []

        window_minutes = (self.max_hour - self.min_hour) * 60
        times = sorted(random.sample(range(window_minutes), self.daily_count))

        for t in times:
            fire_hour = self.min_hour + (t // 60)
            fire_minute = t % 60
            self.scheduled_times.append(f"{fire_hour:02d}:{fire_minute:02d}")
            schedule.every().day.at(f"{fire_hour:02d}:{fire_minute:02d}").do(
                self._fire
            )

        print(f"\n📅 False genuine moments scheduled for today:")
        for t in self.scheduled_times:
            print(f"   {t}")
        print()

    def _fire(self):
        if self.fired_today < self.daily_count:
            generate_moment(self.user_id)
            self.fired_today += 1

    def run(self):
        """Start the scheduler"""
        self.schedule_day()
        schedule.every().day.at("08:55").do(self.schedule_day)
        print("🎭 EscapeHatch running. False genuine moments incoming.")
        print("   Press Ctrl+C to stop being a real person.\n")
        while True:
            schedule.run_pending()
            time.sleep(30)

# ── CLI ───────────────────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser(description="False Genuine Moments Generator")
    parser.add_argument("--now", action="store_true", help="Fire a moment right now")
    parser.add_argument("--user", default="default", help="User ID")
    parser.add_argument("--count", type=int, default=3, help="False moments per day")
    parser.add_argument("--start", type=int, default=9, help="Start hour (24h)")
    parser.add_argument("--end", type=int, default=16, help="End hour (24h)")
    args = parser.parse_args()

    if args.now:
        generate_moment(args.user)
        return

    hatch = EscapeHatch(
        user_id=args.user,
        min_hour=args.start,
        max_hour=args.end,
        daily_count=args.count
    )
    hatch.run()

if __name__ == "__main__":
    main()
