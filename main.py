import time
import sys
from tqdm import tqdm

# Fungsi animasi menunggu
def loading_animation():
    # Jumlah iterasi yang akan dilakukan (misalnya 100 iterasi untuk progres bar penuh)
    total = 100
    for i in tqdm(range(total), desc="Mengupload ke GitHub", unit="frame", ncols=100, mininterval=0.1):
        time.sleep(0.05)  # Simulasi proses upload (bisa disesuaikan dengan kecepatan asli proses)

    # Pesan setelah upload selesai
    print("\nUpload berhasil ke GitHub!")

# Meminta input dari pengguna untuk username dan password GitHub
github_username = input("Masukkan username GitHub: ")
github_password = input("Masukkan password GitHub: ")

# Menampilkan username dan password untuk verifikasi
print(f"Username GitHub: {github_username}")
print(f"Password GitHub: {github_password}")

# Menunggu proses upload dan memberikan animasi loading
print("Mengupload ke GitHub...")
loading_animation()  # Menampilkan animasi selama upload

# Simulasi upload berhasil
print("Upload berhasil ke GitHub! Menunggu proses selanjutnya...")
loading_animation()  # Menampilkan animasi lagi setelah upload selesai

# Catatan tambahan untuk penggunaan lebih lanjut:
# Proses ini bisa diperpanjang untuk mengimplementasikan pengunggahan file ke GitHub
# misalnya dengan menggunakan GitHub API untuk autentikasi dan mengunggah konten.
