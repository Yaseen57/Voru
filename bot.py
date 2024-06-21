import logging
from telegram import Update, ForceReply
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import io
import contextlib
import traceback

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define a few command handlers
async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text('Send me Python code and I will run it!')

async def run_code(update: Update, context: CallbackContext) -> None:
    """Run the user's code."""
    user_code = update.message.text
    output = io.StringIO()
    
    try:
        with contextlib.redirect_stdout(output):
            exec(user_code)
        result = output.getvalue()
        if not result:
            result = 'Code executed successfully!'
    except Exception as e:
        result = f'Error: {str(e)}\n{traceback.format_exc()}'
    
    try:
        await update.message.reply_text(f'```\n{result}\n```', parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.error(f"Failed to send message: {e}")

def main() -> None:
    """Start the bot."""
    # Insert your bot's token here
    token = '7111705639:AAHeFXkCSSSuw_kBdvNTrRy5b0WyD-yY9lI'  # Replace with your actual bot token
    application = Application.builder().token(token).connect_timeout(10).read_timeout(10).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e. message - run the user's code
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, run_code))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
