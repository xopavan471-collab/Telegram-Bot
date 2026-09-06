import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot ON hai bhai! 🔥\nAb YouTube link bhejo.")

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("Bhai ye YouTube link nahi hai!")
        return

    status_msg = await update.message.reply_text("Downloading... ⏳ 1 min ruko")

    try:
        ydl_opts = {
            'format': 'best[ext=mp4][height<=720]/best',
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await status_msg.edit_text("Uploading to Telegram... 🚀")
        await update.message.reply_document(document=open(filename, 'rb'))
        os.remove(filename)
        await status_msg.delete()

    except Exception as e:
        print(f"Error: {e}")
        await status_msg.edit_text(f"Error aa gaya bhai: {e}")

def main():
    if not TOKEN:
        print("CRITICAL ERROR: BOT_TOKEN nahi mila Variables me!")
        return
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
    print("Bot Started...")
    app.run_polling()

if __name__ == "__main__":
    main()
