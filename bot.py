import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import logging

TOKEN = '7111705639:AAHeFXkCSSSuw_kBdvNTrRy5b0WyD-yY9lI'

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'Received /start command from {update.message.from_user.username}')
    await update.message.reply_text('Send me a link and I will download the file for you. Use /download <link> to start the download.')

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        url = context.args[0]
        filename = url.split('/')[-1]
        chat_id = update.message.chat_id

        logger.info(f'Received download request from {update.message.from_user.username} for {url}')

        await update.message.reply_text(f'Starting download for {url}')

        # Use wget to download the file with progress output
        command = f'wget --progress=dot -O {filename} {url}'

        process = await asyncio.create_subprocess_shell(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        while True:
            output = await process.stderr.readline()
            if process.returncode is not None:
                break
            if output:
                output = output.decode('utf-8')  # Decode the output manually
                if '%' in output:
                    try:
                        progress = output.split()[-2]
                        await context.bot.send_message(chat_id=chat_id, text=f'Download progress: {progress}')
                        logger.info(f'Download progress: {progress}')
                    except Exception as e:
                        await context.bot.send_message(chat_id=chat_id, text=f'Error: {e}')
                        logger.error(f'Error: {e}')

        await process.communicate()

        if process.returncode == 0:
            await context.bot.send_message(chat_id=chat_id, text=f'Download complete: {filename}')
            with open(filename, 'rb') as file:
                await context.bot.send_document(chat_id=chat_id, document=file)
            os.remove(filename)
            logger.info(f'Download complete: {filename}')
        else:
            await context.bot.send_message(chat_id=chat_id, text='Download failed.')
            logger.error('Download failed.')
    else:
        await update.message.reply_text('Please provide a link to download. Usage: /download <link>')

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    download_handler = CommandHandler('download', download)

    application.add_handler(start_handler)
    application.add_handler(download_handler)

    logger.info('Bot started')
    application.run_polling()

if __name__ == '__main__':
    main()
