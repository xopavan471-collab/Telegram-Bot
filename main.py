import os, re, requests
from urllib.parse import unquote
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 Bot ON! Mediafire + Direct Link dono bhej sakta hai.")

def get_mediafire_direct_link(url):
    # Mediafire ka asli download link nikalna
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers).text
    # Mediafire ka direct link is button me hota hai
    match = re.search(r'aria-label="Download file"\s+href="([^"]+)"', page)
    if match:
        return match.group(1)
    match2 = re.search(r'https://download[^"]+mediafire\.com[^"]+', page)
    if match2:
        return match2.group(0)
    return None

async def uploader(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not url.startswith("http"):
        return

    msg = await update.message.reply_text("🔍 Link check kar raha hu...")

    try:
        final_url = url
        # Agar mediafire hai to direct link nikalo
        if "mediafire.com" in url:
            await msg.edit_text("📂 Mediafire link mila! Direct link nikal raha hu...")
            direct = get_mediafire_direct_link(url)
            if not direct:
                await msg.edit_text("❌ Mediafire se direct link nahi nikla. Link sahi hai na?")
                return
            final_url = direct

        await msg.edit_text("📥 Downloading... File bada hai to 1-2 min lagega")

        r = requests.get(final_url, stream=True, timeout=120)
        filename = unquote(final_url.split("/")[-1].split("?")[0]) or "mediafire_file"

        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk: f.write(chunk)

        await msg.edit_text(f"🚀 Uploading: {filename}")
        await update.message.reply_document(document=open(filename, 'rb'), filename=filename)

        os.remove(filename)
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"Error: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, uploader))
    app.run_polling()

if __name__ == "__main__":
    main()
