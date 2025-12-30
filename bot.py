from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import instaloader

loader = instaloader.Instaloader(
    download_pictures=True,
    download_videos=True,
    save_metadata=False
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send Instagram username to download stories\n\nExample:\ncristiano"
    )

async def get_story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.strip()
    try:
        profile = instaloader.Profile.from_username(loader.context, username)

        if not profile.has_viewable_story:
            await update.message.reply_text("❌ No stories found or private account.")
            return

        for story in loader.get_stories([profile.userid]):
            for item in story.get_items():
                if item.is_video:
                    await update.message.reply_video(item.video_url)
                else:
                    await update.message.reply_photo(item.url)

    except:
        await update.message.reply_text("⚠️ Error or private account.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_story))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
