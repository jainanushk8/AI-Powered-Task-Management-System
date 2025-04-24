import uuid
import random
import string
from faker import Faker
import pandas as pd
from datetime import datetime, timedelta

fake = Faker()

NUM_RECORDS = 1000
ROLES = ["Admin", "Manager", "Employee"]
PRIORITIES = ["Urgent", "High", "Medium", "Low"]
STATUSES = ["To-Do", "In Progress", "Completed", "On-Hold"]
SENTIMENTS = ["Positive", "Negative", "Neutral"]

def random_hash(length=64):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# 1. Users
users = []
for _ in range(100):
    users.append({
        "user_id": str(uuid.uuid4()),
        "username": fake.user_name(),
        "email": fake.email(),
        "password_hash": random_hash(),
        "role": random.choices(ROLES, weights=[0.1, 0.2, 0.7])[0],
        "date_joined": fake.date_time_between(start_date='-2y', end_date='now')
    })
user_ids = [u["user_id"] for u in users]

# 2. Tasks
tasks = []
for i in range(NUM_RECORDS):
    created_at = fake.date_time_between(start_date='-1y', end_date='-1d')
    deadline = created_at + timedelta(days=random.randint(2, 90))
    tasks.append({
        "task_id": f"task_{i+1:04}",
        "title": fake.bs().capitalize(),
        "description": fake.text(max_nb_chars=200),
        "assigned_to": random.choice(user_ids),
        "priority": random.choices(PRIORITIES, weights=[0.1, 0.2, 0.4, 0.3])[0],
        "status": random.choices(STATUSES, weights=[0.4, 0.3, 0.2, 0.1])[0],
        "deadline": deadline,
        "created_at": created_at
    })

# 3. Sentiment Labels
def infer_sentiment(description, priority):
    desc = description.lower()
    if "urgent" in desc or "asap" in desc or priority == "Urgent":
        return "Negative"
    elif "great" in desc or "success" in desc:
        return "Positive"
    return random.choice(["Neutral", "Positive", "Negative"])

sentiment_labels = [{
    "task_id": t["task_id"],
    "description": t["description"],
    "sentiment": infer_sentiment(t["description"], t["priority"])
} for t in tasks]

# 4. Schedules
schedules = []
for task in tasks:
    start = fake.date_time_between(start_date=task["created_at"], end_date=task["deadline"])
    end = start + timedelta(hours=random.uniform(1, 4))
    schedules.append({
        "schedule_id": f"sched_{uuid.uuid4().hex[:8]}",
        "task_id": task["task_id"],
        "assigned_to": task["assigned_to"],
        "start_time": start,
        "end_time": end,
        "is_auto": random.random() < 0.6
    })

# 5. Performance Metrics
performance = []
for task in tasks:
    est = round(random.uniform(1, 5), 1)
    act = round(est + random.uniform(-0.5, 1.5), 1)
    complete = fake.date_time_between(start_date=task["created_at"], end_date=task["deadline"])
    performance.append({
        "task_id": task["task_id"],
        "assigned_to": task["assigned_to"],
        "estimated_duration (hrs)": est,
        "actual_duration (hrs)": max(act, 0.5),
        "completed_on": complete
    })

# 6. Chat & Feedback
chat_data = []
for _ in range(NUM_RECORDS):
    sender, receiver = random.sample(user_ids, 2)
    chat_data.append({
        "chat_id": str(uuid.uuid4()),
        "sender_id": sender,
        "receiver_id": receiver,
        "message": fake.sentence(nb_words=random.randint(5, 12)),
        "timestamp": fake.date_time_this_year()
    })

# Convert datetime fields to ISO string format for export
df_users = pd.DataFrame(users)
df_users["date_joined"] = df_users["date_joined"].apply(lambda x: x.isoformat())

df_tasks = pd.DataFrame(tasks)
df_tasks["created_at"] = df_tasks["created_at"].apply(lambda x: x.isoformat())
df_tasks["deadline"] = df_tasks["deadline"].apply(lambda x: x.isoformat())

df_schedules = pd.DataFrame(schedules)
df_schedules["start_time"] = df_schedules["start_time"].apply(lambda x: x.isoformat())
df_schedules["end_time"] = df_schedules["end_time"].apply(lambda x: x.isoformat())

df_performance = pd.DataFrame(performance)
df_performance["completed_on"] = df_performance["completed_on"].apply(lambda x: x.isoformat())

df_chat = pd.DataFrame(chat_data)
df_chat["timestamp"] = df_chat["timestamp"].apply(lambda x: x.isoformat())

# Export to CSV
df_users.to_csv("users.csv", index=False)
df_tasks.to_csv("tasks.csv", index=False)
pd.DataFrame(sentiment_labels).to_csv("sentiments.csv", index=False)
df_schedules.to_csv("schedules.csv", index=False)
df_performance.to_csv("performance.csv", index=False)
df_chat.to_csv("chat.csv", index=False)

print("✅ Dataset generated and saved successfully.")
