"""
PROTOCOL.py

Sadowski watches the clock.
Vince watches the leads.
Chill AF watches everything and feels nothing.

Yahdahmean.
"""

import time
import random
import threading
import requests
import argparse
from datetime import datetime, timedelta
from playsound import playsound
import os

# ── SOUNDS ──────────────────────────────────────────────────────────────────

LISTEN_SOUND = os.path.join("sounds", "listen.mp3")       # fix: path.join not pathjoin
VINCE_SOUND  = os.path.join("sounds", "vince_dunk.mp3")   # fix: missing closing paren
ITS_OVER     = os.path.join("sounds", "its_over.mp3")

# ── URLS ─────────────────────────────────────────────────────────────────────

CHILL_AF_URL = "http://localhost:5003"                     # fix: missing closing quote
LISTEN_URL   = "http://localhost:5001"

# ── SADOWSKI EMERGENCY LINES ─────────────────────────────────────────────────

SADOWSKI_EMERGENCIES = [
    "LISTEN.  There's a situation in the kitchen.",
    "LISTEN.  Your 2 o'clock is here and they look expensive.",
    "LISTEN.  Server's down.  Like, down down.",
    "LISTEN.  The client called.  The other client.",          # fix: stray period inside string
    "LISTEN.  Legal is on line two and they sound calm which is bad.",
    "LISTEN.  The demo environment is on fire.  Metaphorically.  Mostly metaphorically.",
]

# ── VINCE LEAD CHECKS ────────────────────────────────────────────────────────

VINCE_CHECKS = [
    "While you were in that meeting, {company} got colder.",
    "{company} has been sitting there.  Vince is watching.",
    "You have {count} leads ignored.  Vince has entered the building.",
    "The pipeline called.  It's disappointed in you.",
    "{company} didn't email themselves.  That was supposed to be you.",
]

# ── PLAY SOUND ───────────────────────────────────────────────────────────────

def play(sound_file):
    try:
        if os.path.exists(sound_file):
            threading.Thread(target=playsound, args=(sound_file,), daemon=True).start()
    except Exception as e:                                     # fix: except was inside try
        print(f"[sound] {e}")

# ── CALENDAR CHECK ───────────────────────────────────────────────────────────

def in_long_meeting():
    """Stub — wire up Google Calendar / Outlook API here."""
    return False

def check_calendar(args):
    """Detect if you're supposed to be in a meeting right now."""
    if args.auto:
        while True:
            if in_long_meeting():
                TheProtocol().full_send()
            time.sleep(60)

# ── SADOWSKI PROTOCOL ────────────────────────────────────────────────────────

class SadowskiProtocol:
    """
    Jeremy walked in at 25 minutes and said LISTEN.
    Now Python does it.
    Configure your escape window.
    Set it.  Forget it.
    """

    def __init__(self, trigger_minutes=25, user_id="default"):   # fix: def_init_ -> __init__
        self.trigger_minutes = trigger_minutes
        self.user_id         = user_id
        self.meeting_start   = None
        self.armed           = False

    def arm(self):
        self.meeting_start = datetime.now()                      # fix: meting_start typo
        self.armed         = True
        deadline           = self.meeting_start + timedelta(minutes=self.trigger_minutes)  # fix: miutes typo
        print(f"\n🍳 SADOWSKI PROTOCOL ARMED")
        print(f"   Meeting start: {self.meeting_start.strftime('%l:%M %p')}")   # fix: bad format string
        print(f"   ({self.trigger_minutes} minutes.  Then LISTEN.)\n")
        threading.Thread(target=self._watch, daemon=True).start()  # fix: targer -> target; was outside method

    def _watch(self):                                            # fix: def_watch -> _watch
        while self.armed:                                        # fix: missing colon
            elapsed = (datetime.now() - self.meeting_start).total_seconds() / 60
            if elapsed >= self.trigger_minutes:                  # fix: elapsed.= -> elapsed >=
                self._fire()
                self.armed = False
                return
            time.sleep(15)

    def _fire(self):                                             # fix: def_fire -> _fire
        emergency = random.choice(SADOWSKI_EMERGENCIES)
        print("\n" + "🚨" * 30)
        print(f"\n  {emergency}")
        print(f"\n  Elapsed: {self.trigger_minutes} minutes.")
        print(f"  Jeremy has entered the room.")                 # fix: broken print statements
        print(f"  You're welcome.\n")
        print("🚨" * 30 + "\n")
        play(LISTEN_SOUND)

        try:
            requests.post(
                f"{CHILL_AF_URL}/crash",                         # fix: stray space in URL
                json={
                    "user_id":    self.user_id,
                    "company":    "meeting room",
                    "vince_level": "Sadowski Protocol",
                },
                timeout=2,
            )
        except Exception:
            pass

    def disarm(self):
        self.armed = False
        print("\n✅ Sadowski Protocol disarmed.  You survived the meeting.\n")


# ── VINCE WATCHER ────────────────────────────────────────────────────────────

class VinceWatcher:                                              # fix: missing colon
    """
    Runs in the background while you're trapped.
    Checks ignored leads.  Reports back when you escape.
    """

    def __init__(self, user_id="default", check_interval=300):  # fix: def_init_ -> __init__
        self.user_id        = user_id
        self.check_interval = check_interval
        self.running        = False
        self.ignored_leads  = []

    def start(self):
        self.running = True
        print(f"🏀 Vince Watcher running.")
        print(f"   Checking leads every {self.check_interval // 60} minutes.\n")
        threading.Thread(target=self._watch, daemon=True).start()  # fix: targer -> target; method name

    def stop(self):
        self.running = False                                     # fix: stop() was the _watch loop body

    def _watch(self):                                            # fix: logic was tangled inside stop()
        while self.running:
            try:
                r    = requests.get(
                    f"{LISTEN_URL}/ignored",
                    params={"user_id": self.user_id},
                    timeout=2,
                )
                data = r.json()
                self.ignored_leads = data.get("ignored", [])
                if self.ignored_leads:
                    lead = self.ignored_leads[0]                 # fix: duplicate assignment removed
                    msg  = random.choice(VINCE_CHECKS).format(
                        company=lead.get("company", "someone"),
                        count=len(self.ignored_leads),
                    )
                    print(f"\n🏀 VINCE UPDATE: {msg}\n")
            except Exception:
                pass
            time.sleep(self.check_interval)

    def report(self):
        if not self.ignored_leads:
            print("\n🏀 VINCE REPORT: No ignored leads.  Vince is cautiously optimistic.\n")  # fix: stray paren
            return
        print(f"\n🏀 VINCE REPORT — {len(self.ignored_leads)} leads ignored while you were trapped:\n")
        for lead in self.ignored_leads:
            print(f"  💀 {lead.get('company')} - {lead.get('contact_name')}")
            print(f"     {lead.get('pain_point')}")
            print()


# ── THE PROTOCOL ─────────────────────────────────────────────────────────────

class TheProtocol:
    """
    Full send.
    Sadowski watches the clock.
    Vince watches the leads.
    Chill AF watches everything and feels nothing.
    """

    def __init__(self, user_id="default", meeting_minutes=25):  # fix: def_init_ -> __init__
        self.sadowski = SadowskiProtocol(meeting_minutes, user_id)  # fix: SadoskiProtocol typo
        self.vince    = VinceWatcher(user_id)
        self.user_id  = user_id

    def full_send(self):
        print("\n" + "=" * 60)
        print("  THE PROTOCOL — FULL SEND")
        print("  Sadowski + Vince + Chill AF")
        print("  Yahdahmean.")
        print("=" * 60 + "\n")

        play(LISTEN_SOUND)
        self.vince.start()
        self.sadowski.arm()

        print("Running.  Press Ctrl+C to disarm and get the Vince report.\n")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.sadowski.disarm()
            self.vince.stop()
            self.vince.report()
            print("  Chill AF Backend logged everything.")
            print("  It felt nothing.")
            print("  Yahdahmean.\n")


# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="TheProtocol — Sadowski + Vince + Chill AF")
    parser.add_argument("--meeting",   action="store_true", help="Arm Sadowski Protocol only")
    parser.add_argument("--leads",     action="store_true", help="Start Vince Watcher only")  # fix: add_arguement typo
    parser.add_argument("--full-send", action="store_true", help="All three.  Chaos.  Michelada.")
    parser.add_argument("--minutes",   type=int, default=25, help="Sadowski trigger time in minutes (default: 25)")  # fix: missing comma
    parser.add_argument("--user",      default="default",   help="User ID")   # fix: unclosed quote
    parser.add_argument("--auto",      action="store_true", help="Auto-arm when a long meeting is detected")
    args = parser.parse_args()                                   # fix: parse.args() -> parse_args()

    if args.meeting:
        s = SadowskiProtocol(args.minutes, args.user)
        s.arm()
        try:
            while s.armed:
                time.sleep(1)
        except KeyboardInterrupt:
            s.disarm()

    elif args.leads:
        v = VinceWatcher(args.user)
        v.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            v.stop()
            v.report()

    elif args.full_send:
        protocol = TheProtocol(args.user, args.minutes)
        protocol.full_send()

    elif args.auto:
        check_calendar(args)

    else:
        print("\nThe Protocol is ready.")
        print("  --meeting    Sadowski only")
        print("  --leads      Vince only")
        print("  --full-send  All three.  Yahdahmean.\n")


if __name__ == "__main__":                                       # fix: if_name_=="_main_"
    main()


# ── PROFESSIONAL_PROTOCOL.py ─────────────────────────────────────────────────
"""
Same engine.  Different labels.

Sadowski  -> "Meeting Efficiency Module"
Vince     -> "Lead Aging Monitor"
Chill AF  -> "Event Logging Service"

Yahdahmean -> "Understood"
"""

SADOWSKI_EMERGENCIES_PRO = [
    "Time check: This meeting has reached its scheduled duration.",   # fix: reacherd typo
    "Please note: There are pending action items requiring attention.",  # fix: stray quote
    "Respectfully, we should table remaining items for async follow-up.",
]

VINCE_CHECKS_PRO = [
    "Lead {company} has exceeded recommended response window.",
    "Follow-up required for {count} outstanding opportunities.",
]
