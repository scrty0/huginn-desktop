import os
import sqlite3

def init_db():
    os.makedirs("data/audio", exist_ok=True)
    conn = sqlite3.connect("data/huginn.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS calls
                 (id TEXT PRIMARY KEY, timestamp TEXT, caller_info TEXT, duration INTEGER DEFAULT 0,
                  transcript TEXT, is_fraud BOOLEAN, confidence REAL, triggers TEXT,
                  trigger_category TEXT, audio_path TEXT, feedback BOOLEAN)''')
    conn.commit()
    conn.close()
    print("Database initialized.")

def main():
    init_db()
    if not os.path.exists(".env"):
        with open(".env.example", "r") as f_ex, open(".env", "w") as f_env:
            f_env.write(f_ex.read())
    print("Setup complete.")

if __name__ == "__main__":
    main()
