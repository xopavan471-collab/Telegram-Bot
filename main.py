import logging
import time
import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Token ko seedha string mein define kar diya hai taaki tuple error na aaye
TOKEN = "8819977957:AAHnYDrOolaKokG5fZ6UyLYp2KxvEsmWxDo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        f"Hello {user_name}!\n\n"
        f"Welcome to GF Zexon Bypass Bot! 🔗\n"
        f"Koi bhi short link bhejiye aur turant bypassed link paaiye.\n\n"
        f"Command: /bypass <link> ya direct link bhejein."
    )
    await update.message.reply_text(welcome_text)

async def bypass_link_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        url = context.args[0]
    else:
        url = update.message.text.strip()

    if not url.startswith("http"):
        return

    msg = await update.message.reply_text("🔄 Bypassing link, please wait...")
    start_time = time.time()

    api_url = f"https://api.bypass.vip/bypass?url={url}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    time_taken = round(time.time() - start_time, 2)
                    
                    if data.get("status") == 200 or "destination" in data:
                        final_url = data.get("destination") or data.get("url")
                        response_text = (
                            f"⚡ **Bypass Successful!**\n\n"
                            f"🔗 **Original Link:**\n{url}\n\n"
                            f"🎯 **Bypassed Link:**\n{final_url}\n\n"
                            f"⏱ **Time Taken:** {time_taken} seconds\n\n"
                            f"Powered By : @GF_Zexon_Bypass_Bot"
                        )
                        await msg.edit_text(response_text, disable_web_page_preview=True)
                    else:
                        error_msg = data.get("msg", "Unknown error from API")
                        await msg.edit_text(f"❌ Bypass Failed! Server response: {error_msg}")
                else:
                    await msg.edit_text(f"❌ Bypass Failed! API status code: {response.status}")

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        await msg.edit_text(f"❌ Bypass Failed! Error occurred: {str(e)[:50]}")

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("bypass", bypass_link_logic))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), bypass_link_logic))

    print("🤖 Bot started successfully!")
    application.run_polling()

if __name__ == '__main__':
    main()
                    
