import os

USERS_FILE = "users.txt"
DB_FILE = "issues.txt"

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return [line.strip().split("|") for line in f.readlines()]

def save_user(username, password, first_name, last_name, phone, role):
    with open("users.txt", "a") as f:
        f.write(f"{username}|{password}|{first_name}|{last_name}|{phone}|{role}\n")

def save_issue(x, y, issue_type, description):
    with open(DB_FILE, "a") as f:
        f.write(f"2025-04-02 | {x},{y} | {issue_type} | {description} | Status: Reported\n")

def load_issues():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        return f.readlines()

def load_contacts():
    if not os.path.exists("contact_info.txt"):
        return []
    contacts = []
    with open("contact_info.txt", "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 4:
                location, category, name, number = map(str.strip, parts)
                contacts.append([name, location, category, number])
    return contacts

