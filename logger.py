import logging
import os

# Setup basic debug logging
logging.basicConfig(
    filename="cinepulse_debug.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# File paths
CLICK_LOG_FILE = "click_logs.txt"
SEARCH_LOG_FILE = "search_logs.txt"

# Username display logic
def get_user_display(user):
    if hasattr(user, 'username') and user.username:
        return f"@{user.username}"
    elif hasattr(user, 'id'):
        return f"ID:{user.id}"
    else:
        return "UnknownUser"

# Log when user clicks category (e.g. Anime)
def log_click(user, category):
    try:
        user_display = get_user_display(user)
        with open(CLICK_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[Click] {category} | User: {user_display}\n")
    except Exception as e:
        logging.error(f"[❌] log_click() error: {e}")

# Log when user searches for something
def log_search(query, user_id, username=None):
    try:
        user_display = f"@{username}" if username else f"ID:{user_id}"
        with open(SEARCH_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[Search] '{query}' | User: {user_display}\n")
    except Exception as e:
        logging.error(f"[❌] log_search() error: {e}")

# Read all click logs
def get_click_logs():
    try:
        with open(CLICK_LOG_FILE, "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        return ["[No click logs yet]"]
    except Exception as e:
        logging.error(f"[❌] get_click_logs() error: {e}")
        return ["[Click log read error]"]

# Read all search logs
def get_search_logs():
    try:
        with open(SEARCH_LOG_FILE, "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        return ["[No search logs yet]"]
    except Exception as e:
        logging.error(f"[❌] get_search_logs() error: {e}")
        return ["[Search log read error]"]

# Clear click logs
def clear_click_logs():
    try:
        open(CLICK_LOG_FILE, "w").close()
        logging.info("[✅] Click logs cleared.")
    except Exception as e:
        logging.error(f"[❌] clear_click_logs() error: {e}")

# Clear search logs
def clear_search_logs():
    try:
        open(SEARCH_LOG_FILE, "w").close()
        logging.info("[✅] Search logs cleared.")
    except Exception as e:
        logging.error(f"[❌] clear_search_logs() error: {e}")