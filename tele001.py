from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import os

# Fungsi untuk menanggapi perintah /start
async def start(update: Update, context):
    await update.message.reply_text("Halo! Selamat datang di bot Telegram.")

# Fungsi untuk menanggapi setiap pesan teks yang dikirim pengguna
async def echo(update: Update, context):
    text_received = update.message.text
    await update.message.reply_text(f"Kamu berkata: {text_received}")

# Fungsi untuk mengirim file log massage.txt
async def send_log(update: Update, context):
    chat_id = update.message.chat_id
    log_file = os.path.join(os.path.dirname(__file__), 'massage.txt')
    
    if os.path.exists(log_file):
        await context.bot.send_document(chat_id=chat_id, document=open(log_file, 'rb'))
    else:
        await update.message.reply_text("File log tidak ditemukan.")

if __name__ == '__main__':
    # Ganti 'YOUR_TOKEN' dengan token API bot Telegram yang didapat dari BotFather
    application = ApplicationBuilder().token('YOUR_TOKEN').build()

    # Handler untuk perintah /start
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Handler untuk membalas semua pesan teks
    echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    application.add_handler(echo_handler)
    
    # Handler untuk mengirim file log ketika diminta (/sendlog)
    sendlog_handler = CommandHandler('sendlog', send_log)
    application.add_handler(sendlog_handler)

    # Jalankan bot
    application.run_polling()
