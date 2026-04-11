import sqlite3
from datetime import datetime

DB = "listen.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            company TEXT,
            contact_name TEXT,
            contact_title TEXT,
            email TEXT,
            pain_point TEXT,
            found_at TEXT,
            emailed INTEGER DEFAULT 0,
            ignored_count INTEGER DEFAULT 0
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            company TEXT,
            email_text TEXT,
            sent_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_lead(user_id, lead):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        INSERT INTO leads (user_id, company, contact_name, contact_title, email, pain_point, found_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        lead.get("company"),
        lead.get("contact_name"),
        lead.get("contact_title"),
        lead.get("email"),
        lead.get("pain_point"),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def log_email(user_id, company, email_text):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        INSERT INTO emails (user_id, company, email_text, sent_at)
        VALUES (?, ?, ?, ?)
    """, (user_id, company, email_text, datetime.now().isoformat()))
    c.execute("""
        UPDATE leads SET emailed = 1 WHERE user_id = ? AND company = ?
    """, (user_id, company))
    conn.commit()
    conn.close()

def get_ignored_leads(user_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT company, contact_name, contact_title, pain_point, found_at
        FROM leads
        WHERE user_id = ? AND emailed = 0
        ORDER BY found_at DESC
    """, (user_id,))
    rows = c.fetchall()
    conn.close()
    return [{"company": r[0], "contact_name": r[1], "contact_title": r[2], "pain_point": r[3], "found_at": r[4]} for r in rows]
