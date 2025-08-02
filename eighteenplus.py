from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from utils import load_json
from logger import log_click  # ✅ Stylish click logger

# Load data
eighteenplus_data = load_json("eighteenplus_data.json")

# ✅ CinePulseBot-compatible name
async def show_eighteen(update: Update, context: ContextTypes.DEFAULT_TYPE, page=1):
    context.user_data["eighteen_page"] = page
    titles = list(eighteenplus_data.keys())
    total_items = len(titles)
    total_pages = (total_items - 1) // 30 + 1

    if page < 1 or page > total_pages:
        await update.message.reply_text("❌ No more pages.")
        return

    start = (page - 1) * 30
    end = start + 30
    current_titles = titles[start:end]

    keyboard = []
    for i in range(0, len(current_titles), 2):
        row = [current_titles[i]]
        if i + 1 < len(current_titles):
            row.append(current_titles[i + 1])
        keyboard.append(row)

    nav = []
    if page > 1:
        nav.append("⏮ Back")
    if page < total_pages:
        nav.append("⏭ Next")
    if nav:
        keyboard.append(nav)
    keyboard.append(["🏠 Main Menu"])

    await update.message.reply_text(
        "🔞🔥 𝟏𝟖+ 𝐂𝐨𝐧𝐭𝐞𝐧𝐭",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# ✅ This name must match: handle_eighteen_buttons
async def handle_eighteen_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user = update.effective_user
    page = context.user_data.get("eighteen_page", 1)
    titles = list(eighteenplus_data.keys())
    total_pages = (len(titles) - 1) // 30 + 1

    # Navigation
    if text == "⏮ Back":
        if page > 1:
            await show_eighteen(update, context, page - 1)
        else:
            await update.message.reply_text("❌ Already at first page.")
        return

    elif text == "⏭ Next":
        if page < total_pages:
            await show_eighteen(update, context, page + 1)
        else:
            await update.message.reply_text("❌ No more pages.")
        return

    elif text == "🏠 Main Menu":
        from bot import reply_markup
        await update.message.reply_text("🏠 Back to Main Menu:", reply_markup=reply_markup)
        return

    # Show selected item
    if text in eighteenplus_data:
        data = eighteenplus_data[text]

        log_click(user, text)  # ✅ Logging user click

        poster = data.get("poster", "")
        links = "\n".join(data.get("links", []))
        audio = "Hindi + Multi Audio"

        caption = (
            f"<b>{text}</b>\n\n"
            f"🔊 Audio: {audio}\n\n"
            f"{links}\n\n"
            "😌 <b>दिक्कत आ रही है?</b>\n"
            "🎬 <b>वीडियो देखो – सब सेट हो जाएगा!</b>\n"
            "🔗 <b>लिंक नीचे है 👇</b>\n"
            "🎥 https://t.me/cinepulsebot_official/25"
        )

        try:
            if poster:
                if len(caption) > 1024:
                    await update.message.reply_photo(photo=poster)
                    await update.message.reply_text(caption, parse_mode="HTML", disable_web_page_preview=True)
                else:
                    await update.message.reply_photo(photo=poster, caption=caption, parse_mode="HTML")
            else:
                await update.message.reply_text(caption, parse_mode="HTML", disable_web_page_preview=True)
        except Exception as e:
            print(f"[❗] Image error for {text}: {e}")
            await update.message.reply_text(caption, parse_mode="HTML", disable_web_page_preview=True)
        return

    await update.message.reply_text("❌ Invalid option. Please use the menu.")