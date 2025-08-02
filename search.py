from difflib import get_close_matches
from telegram import Update
from telegram.ext import ContextTypes
import os
import json
from user_logger import handle_bot_block
from logger import log_search  # ✅ Logging integration

# ✅ All JSON sources to search
DATA_FILES = [
    "anime_data.json",
    "kdrama_data.json",
    "bollywood_data.json",
    "marvel_data.json",
    "hollywood_data.json",
    "series_data.json",
    "south_data.json",
    "latest_data.json",
    "eighteenplus_data.json",
    "multipart_data.json",
]

# ✅ Fix poster URLs
def fix_poster_url(url: str) -> str:
    if not url:
        return ""
    if url.endswith((".jpg", ".jpeg", ".png", ".webp")) or "i.ibb.co" in url:
        return url
    if "ibb.co/" in url:
        code = url.strip().split("/")[-1]
        return f"https://i.ibb.co/{code}/poster.jpg"
    if "catbox.moe" in url:
        return url.replace("https://catbox.moe/", "https://files.catbox.moe/")
    return url

# ✅ Load JSON data
def load_all_data():
    all_data = {}
    for file in DATA_FILES:
        if os.path.exists(file):
            try:
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    all_data.update(data)
            except Exception as e:
                print(f"[❌] Failed to load {file}: {e}")
    return all_data

# ✅ Search core
def search_movie(query):
    data = load_all_data()
    matches = get_close_matches(query, list(data.keys()), n=1, cutoff=0.3)

    if not matches:
        return None

    title = matches[0]
    item = data.get(title, {})
    poster = fix_poster_url(item.get("poster", ""))
    audio = item.get("audio", "Hindi + Multi Audio")
    links = "\n".join(item.get("links", []))

    # ✅ Hindi support footer
    footer = (
        "\n\n😌 <b>दिक्कत आ रही है?</b>\n"
        "🎬 <b>वीडियो देखो – सब सेट हो जाएगा!</b>\n"
        "🔗 <b>लिंक नीचे है 👇</b>\n"
        "🎥 https://t.me/cinepulsebot_official/25"
    )

    base = f"<b>{title}</b>\n🔊 Audio: {audio}\n\n{links}{footer}"

    if len(base) > 1024:
        allowed_links = 1024 - len(title) - len(audio) - len(footer) - 50
        trimmed_links = links[:allowed_links] + "\n 🔗 More links available..."
        base = f"<b>{title}</b>\n🔊 Audio: {audio}\n\n{trimmed_links}{footer}"

    return title, poster, base

# ✅ Search Handler
async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    query = update.message.text.strip()

    if not query:
        await update.message.reply_text("❌ Please enter something to search.")
        return

    # ✅ Log search
    try:
        log_search(query, user.id, user.username)
    except Exception as e:
        print(f"[⚠️] Logging search failed: {e}")

    # ✅ Search logic
    result = search_movie(query)
    if not result:
        await update.message.reply_text("❌ No results found. Try a different name.")
        return

    title, poster, caption = result

    try:
        if poster:
            await update.message.reply_photo(
                photo=poster,
                caption=caption,
                parse_mode="HTML",
                disable_web_page_preview=True  # ✅ No link preview
            )
        else:
            await update.message.reply_text(
                caption,
                parse_mode="HTML",
                disable_web_page_preview=True
            )
    except Exception as e:
        err = str(e).lower()
        print(f"[❗] Search error: {e}")
        if "forbidden" in err or "bot was blocked" in err or "unauthorized" in err:
            handle_bot_block(user.id)
        await update.message.reply_text(caption[:4000], parse_mode="HTML", disable_web_page_preview=True)