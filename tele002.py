from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Fungsi untuk menanggapi perintah /start
async def start(update: Update, context):
    text_received = update.message.text
    chat_id = update.message.chat.id  # Mengambil Chat ID
    await update.message.reply_text(f"Kamu berkata: {text_received}\nChat ID kamu: {chat_id}")

# Fungsi untuk menanggapi setiap pesan teks yang dikirim pengguna
async def echo(update: Update, context):
    text_received = update.message.text
    chat_id = update.message.chat.id  # Mengambil Chat ID
    await update.message.reply_text(f"Kamu berkata: {text_received}\nChat ID kamu: {chat_id}")

if __name__ == '__main__':
    # Ganti 'YOUR_TOKEN' dengan token API bot Telegram yang didapat dari BotFather
    application = ApplicationBuilder().token('7390806693:AAGDNK2npBDFuBeDou3ZHVgER_M_uscliQI').build()

    # Handler untuk perintah /start
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Handler untuk membalas semua pesan teks dan menunjukkan Chat ID
    echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    application.add_handler(echo_handler)

    # Jalankan bot
    application.run_polling()
