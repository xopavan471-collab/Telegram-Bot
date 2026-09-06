import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bhai link bhejo, mai download karke deta hu! 🎥")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "youtube.com" not in url and "youtu.be" not in url:
        return
    
    await update.message.reply_text("Downloading... ⏳")
    try:
        ydl_opts = {'format': 'best', 'outtmpl': '%(title)s.%(ext)s'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        await update.message.reply_document(document=open(filename, 'rb'))
        os.remove(filename)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    if not TOKEN:
        print("BOT_TOKEN nahi mila!")
        return
    print("YouTube Bot Running...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    app.run_polling()

if __name__ == "__main__":
    main()
