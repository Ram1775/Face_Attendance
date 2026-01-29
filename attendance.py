import pandas as pd
from datetime import datetime
import os

def mark_attendance(name):
    os.makedirs("data", exist_ok=True)
    file = "data/attendance.csv"

    if not os.path.exists(file) or os.stat(file).st_size == 0:
        df = pd.DataFrame(columns=["Name", "Date", "Time", "Status"])
    else:
        df = pd.read_csv(file)

    today = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")

    user_today = df[(df["Name"] == name) & (df["Date"] == today)]

    status = "IN" if user_today.empty or user_today.iloc[-1]["Status"] == "OUT" else "OUT"

    df.loc[len(df)] = [name, today, time, status]
    df.to_csv(file, index=False)

    return status
