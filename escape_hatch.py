
#!/usr/bin/env python3
"""
PROFESSIONAL_ESCALATION.py
Corporate-safe version of the Sadowski Protocol.

Same urgency. Zero references to fires, dumpsters, or Jeremy.
Now with "professional development" and "time management" language.
"""

import time
import threading
from datetime import datetime, timedelta
from playsound import playsound
import os

# ── HR-APPROVED ESCALATION MATRIX ─────────────────────────────────
# Words changed: "fire" → "time constraint"
#                "emergency" → "scheduling conflict"
#                "dumpster" → "resource allocation issue"

ESCALATION_LEVELS = {
    1: {
        "minutes": 5,
        "code": "Time check",
        "message": "Pardon the interruption — noting that we're at the 5-minute mark.",
        "action": "Subtly glance at watch. Continue professionally.",
        "sound": "gentle_chime.mp3"
    },
    2: {
        "minutes": 10,
        "code": "Resource reallocation needed",
        "message": "I want to be respectful of everyone's time. We have a hard stop at the 30-minute mark.",
        "action": "Place notebook on table. Shift posture slightly.",
        "sound": "calendar_notification.mp3"
    },
    3: {
        "minutes": 20,
        "code": "Schedule conflict alert",
        "message": "I have a prior commitment in 10 minutes. Can we summarize key action items?",
        "action": "Stand up. Not aggressively. Just... vertically.",
        "sound": "meeting_warning.mp3"
    },
    4: {
        "minutes": 30,
        "code": "Mandatory departure",
        "message": "I apologize — I have another obligation I cannot reschedule. Let's continue this async.",
        "action": "Exit with purpose. No further explanation required.",
        "sound": "professional_exit.mp3"
    }
}

class ProfessionalEscalation:
    """
    Corporate-safe meeting timer. Not an emergency. A 'scheduling optimization.'
    """
    
    def __init__(self, user_id="default", department="Sales"):
        self.user_id = user_id
        self.department = department
        self.active = False
        self.start_time = None
        self.current_level = 0
        self.meeting_name = None
        
    def start_meeting(self, meeting_name="Strategic Review"):
        """Begin timer — with professional language"""
        self.active = True
        self.start_time = datetime.now()
        self.meeting_name = meeting_name
        self.current_level = 0
        
        print(f"\n📊 Meeting timer engaged: {meeting_name}")
        print(f"   Hard stop: 30 minutes (standard corporate courtesy)")
        print(f"   Notifications will be discreet.\n")
        
        threading.Thread(target=self._watchdog, daemon=True).start()
        
    def _watchdog(self):
        """Monitor meeting duration with professional escalation"""
        while self.active:
            elapsed = (datetime.now() - self.start_time).total_seconds() / 60
            
            for level_num, level_data in ESCALATION_LEVELS.items():
                if elapsed >= level_data["minutes"] and self.current_level < level_num:
                    self.current_level = level_num
                    self._deliver_notification(level_data)
                    
            time.sleep(30)
            
    def _deliver_notification(self, level_data):
        """Polite but firm reminders"""
        print("\n" + "="*50)
        print(f"⏰ {level_data['code']} — {self.meeting_name}")
        print(f"   {level_data['message']}")
        print(f"   Suggested action: {level_data['action']}")
        print("="*50 + "\n")
        
        # Play gentle sound if available
        sound_file = os.path.join(os.path.dirname(__file__), "sounds", level_data["sound"])
        if os.path.exists(sound_file):
            threading.Thread(target=playsound, args=(sound_file,), daemon=True).start()
            
        if self.current_level >= 4:
            self.end_meeting(professionally=True)
            
    def end_meeting(self, professionally=False):
        """Close the meeting timer"""
        self.active = False
        elapsed = (datetime.now() - self.start_time).total_seconds() / 60
        
        if professionally:
            print(f"\n✅ Meeting concluded at {round(elapsed, 1)} minutes.")
            print(f"   Thank you for respecting everyone's calendar.")
        else:
            print(f"\n📅 Meeting ended at {round(elapsed, 1)} minutes.")
