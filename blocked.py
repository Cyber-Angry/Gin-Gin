import json
import os

BLOCKED_FILE = "blocked_users.json"
BANNED_FILE = "banned_users.json"

# ✅ Utility to ensure the file exists
def ensure_file_exists(file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)

# ✅ Blocked Users Handling
def load_blocked_users():
    ensure_file_exists(BLOCKED_FILE)
    with open(BLOCKED_FILE, "r") as f:
        return json.load(f)

def save_blocked_users(user_ids):
    with open(BLOCKED_FILE, "w") as f:
        json.dump(user_ids, f, indent=2)

def is_user_blocked(user_id):
    blocked_users = load_blocked_users()
    return str(user_id) in blocked_users

def block_user(user_id):
    user_id = str(user_id)
    blocked_users = load_blocked_users()
    if user_id not in blocked_users:
        blocked_users.append(user_id)
        save_blocked_users(blocked_users)

def unblock_user(user_id):
    user_id = str(user_id)
    blocked_users = load_blocked_users()
    if user_id in blocked_users:
        blocked_users.remove(user_id)
        save_blocked_users(blocked_users)

def get_blocked_users():
    return load_blocked_users()

# ✅ Optional: Banned Users Handling
def load_banned_users():
    ensure_file_exists(BANNED_FILE)
    with open(BANNED_FILE, "r") as f:
        return json.load(f)

def is_banned(user_id):
    banned_users = load_banned_users()
    return str(user_id) in banned_users