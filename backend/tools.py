import sqlite3

conn = sqlite3.connect("appointments.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date TEXT,
    time TEXT
)
""")
conn.commit()

def check_availability(date: str, time: str) -> bool:
    cursor.execute("SELECT * FROM appointments WHERE date=? AND time=?", (date, time))
    result = cursor.fetchone()
    return result is None  # True = slot is free

def save_to_db(name: str, date: str, time: str) -> str:
    cursor.execute(
        "INSERT INTO appointments (name, date, time) VALUES (?, ?, ?)",
        (name, date, time)
    )
    conn.commit()
    return "Appointment booked successfully"