import tkinter as tk
from tkinter import messagebox, simpledialog
import time
import random
import winsound
import os

# Offline Activity Suggestions
activities = [
    "📖 Read a book",
    "🚶 Go for a walk",
    "🧘 Try a breathing exercise",
    "🎨 Draw or doodle",
    "📓 Journal your thoughts",
    "📞 Call a friend"
]

# Create log file if it doesn't exist
LOG_FILE = "session_log.txt"
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("Phone Detox Session Log\n")
        f.write("========================\n\n")

class DetoxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📱 Phone Detox Coach")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f8ff")  # Light blue background
        self.start_time = None
        self.limit_minutes = 30

        # Welcome popup
        messagebox.showinfo("Welcome!", "Track your screen time and stay focused.\nStart a session, then end it when you're done.")

        self.label = tk.Label(root, text="📱 Phone Detox Coach", font=("Helvetica", 16, "bold"), bg="#f0f8ff")
        self.label.pack(pady=10)

        self.start_btn = tk.Button(root, text="Start Screen Session", command=self.start_session)
        self.start_btn.pack(pady=5)

        self.stop_btn = tk.Button(root, text="End Session", command=self.end_session)
        self.stop_btn.pack(pady=5)

        self.set_limit_btn = tk.Button(root, text="Set Time Limit", command=self.set_limit)
        self.set_limit_btn.pack(pady=5)

        self.activity_btn = tk.Button(root, text="Suggest Offline Activity", command=self.suggest_activity)
        self.activity_btn.pack(pady=5)

        self.view_log_btn = tk.Button(root, text="View Session Log", command=self.view_log)
        self.view_log_btn.pack(pady=5)

    def start_session(self):
        self.start_time = time.time()
        messagebox.showinfo("Session Started", "Screen session started. Stay mindful!")

    def end_session(self):
        if self.start_time:
            duration = (time.time() - self.start_time) / 60  # in minutes
            self.start_time = None
            message = f"Session ended. You used the screen for {duration:.2f} minutes."

            # Log session to file
            with open(LOG_FILE, "a") as log:
                log.write(f"{time.ctime()}: {duration:.2f} minutes\n")

            if duration > self.limit_minutes:
                self.play_alert()
                message += "\n⚠️ You exceeded your limit!"
            else:
                message += "\n✅ Great job staying within your limit!"
            messagebox.showinfo("Session Summary", message)
        else:
            messagebox.showwarning("No Session", "Start a session first.")

    def set_limit(self):
        limit = simpledialog.askinteger("Set Limit", "Enter screen time limit (minutes):")
        if limit:
            self.limit_minutes = limit
            messagebox.showinfo("Limit Set", f"New limit: {limit} minutes")

    def suggest_activity(self):
        suggestion = random.choice(activities)
        messagebox.showinfo("Try This!", suggestion)

    def view_log(self):
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as log:
                content = log.read()
            messagebox.showinfo("Session Log", content[-500:] if len(content) > 500 else content)
        else:
            messagebox.showinfo("Session Log", "No sessions logged yet.")

    def play_alert(self):
        winsound.Beep(1000, 500)  # Frequency, Duration

if __name__ == "__main__":
    root = tk.Tk()
    app = DetoxApp(root)
    root.mainloop()