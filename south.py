from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from utils import load_json
from logger import log_click  # ✅ Logging

# Load South Indian movie data
south_data = load_json("south_data.json")

# Show South Indian Movies in 15x2 layout
async def show_south(update: Update, context: ContextTypes.DEFAULT_TYPE, page=1):
    context.user_data["south_page"] = page
    items = [{"title": title, "emoji": south_data[title].get("emoji", "")} for title in south_data]
    total_items = len(items)
    total_pages = (total_items - 1) // 30 + 1

    if page < 1 or page > total_pages:
        await update.message.reply_text("❌ No more pages.")
        return

    start = (page - 1) * 30
    end = start + 30
    current_items = items[start:end]

    keyboard = []
    for i in range(0, len(current_items), 2):
        row = []
        left = current_items[i]
        row.append(f"{left['title']} {left['emoji']}".strip())
        if i + 1 < len(current_items):
            right = current_items[i + 1]
            row.append(f"{right['title']} {right['emoji']}".strip())
        keyboard.append(row)

    keyboard.append(["⏮ Back", "⏭ Next"])
    keyboard.append(["🏠 Main Menu"])

    await update.message.reply_text(
        "🔥🎭 𝐒𝐨𝐮𝐭𝐡 𝐈𝐧𝐝𝐢𝐚𝐧 𝐂𝐨𝐥𝐥𝐞𝐜𝐭𝐢𝐨𝐧",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

# Handle South Indian movie selection
async def handle_south_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user = update.effective_user
    page = context.user_data.get("south_page", 1)
    items = [{"title": title, "emoji": south_data[title].get("emoji", "")} for title in south_data]
    total_pages = (len(items) - 1) // 30 + 1

    # Navigation
    if text == "⏮ Back":
        if page > 1:
            await show_south(update, context, page - 1)
        else:
            await update.message.reply_text("❌ Already at first page.")
        return

    elif text == "⏭ Next":
        if page < total_pages:
            await show_south(update, context, page + 1)
        else:
            await update.message.reply_text("❌ No more pages.")
        return

    elif text == "🏠 Main Menu":
        from bot import reply_markup
        await update.message.reply_text("🏠 Back to Main Menu:", reply_markup=reply_markup)
        return

    # Match button text
    for title in south_data:
        expected_btn = f"{title} {south_data[title].get('emoji', '')}".strip()
        if text == expected_btn:
            data = south_data[title]
            log_click(user, title)

            poster = data.get("poster", "")
            links = "\n".join(data.get("links", []))
            audio = "Hindi + Multi Audio"

            promo = (
                "\n\n😌 <b>दिक्कत आ रही है?</b>\n"
                "🎬 <b>वीडियो देखो – सब सेट हो जाएगा!</b>\n"
                "🔗 <b>लिंक नीचे है 👇</b>\n"
                "🎥 https://t.me/cinepulsebot_official/25"
            )

            caption = f"<b>{title}</b>\n\n🔊 Audio: {audio}\n\n{links}{promo}"

            try:
                if poster:
                    if len(caption) > 1024:
                        await update.message.reply_photo(photo=poster)
                        await update.message.reply_text(
                            caption, parse_mode="HTML", disable_web_page_preview=True
                        )
                    else:
                        await update.message.reply_photo(
                            photo=poster,
                            caption=caption,
                            parse_mode="HTML",
                            disable_web_page_preview=True,
                        )
                else:
                    await update.message.reply_text(
                        caption, parse_mode="HTML", disable_web_page_preview=True
                    )
            except Exception as e:
                print(f"[❗] Image error for {title}: {e}")
                await update.message.reply_text(
                    caption, parse_mode="HTML", disable_web_page_preview=True
                )
            return

    await update.message.reply_text("❌ Invalid option. Please use the menu.")