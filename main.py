import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("YouTube Downloader Ready Hai Bhai! 🔥\nBas YouTube ka link bhejo, mai video bhej dunga.")

async def download_yt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("Bhai sahi YouTube link bhejo 🫂")
        return

    await update.message.reply_text("Downloading... ⏳ Thoda wait karo bhai")

    try:
        ydl_opts = {
            'format': 'best[height<=720]',
            'outtmpl': '/tmp/%(title)s.%(ext)s',
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        await update.message.reply_video(video=open(file_path, 'rb'), caption=f"{info.get('title')}")
        os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(f"Error aa gaya bhai: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_yt))
    print("YouTube Bot Running...")
    app.run_polling()

if __name__ == "__main__":
    main()
