import time
import base64
import requests
from tqdm import tqdm

# Fungsi animasi menunggu
def loading_animation():
    total = 100
    for i in tqdm(range(total), desc="Mengupload ke GitHub", unit="frame", ncols=100, mininterval=0.1):
        time.sleep(0.05)  # Simulasi proses upload (bisa disesuaikan dengan kecepatan asli proses)
    print("\nUpload berhasil ke GitHub!")

# Fungsi untuk mengunduh file dari repositori GitHub lain
def download_from_github(source_url, local_path):
    # Mendapatkan data dari URL sumber
    response = requests.get(source_url)
    
    # Mengecek apakah respons berhasil
    if response.status_code == 200:
        # Menyimpan file yang diunduh ke path lokal
        with open(local_path, "wb") as file:
            file.write(response.content)
        print(f"File berhasil diunduh ke {local_path}")
    else:
        print("Gagal mengunduh file dari GitHub.")

# Fungsi untuk mengunggah file ke repositori GitHub
def upload_to_github(file_path, repo, branch, github_username, github_token):
    url = f"https://api.github.com/repos/{github_username}/{repo}/contents/{file_path}"

    with open(file_path, "rb") as file:
        content = base64.b64encode(file.read()).decode()

    data = {
        "message": f"Upload {file_path}",
        "branch": branch,
        "content": content
    }

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.put(url, json=data, headers=headers)

    if response.status_code == 201:
        print(f"File {file_path} berhasil diunggah ke GitHub!")
    else:
        print(f"Terjadi kesalahan: {response.json()}")

# Meminta input dari pengguna untuk username dan token GitHub
github_username = input("Masukkan username GitHub: ")
github_token = input("Masukkan token GitHub (gunakan personal access token): ")

# Menampilkan username untuk verifikasi
print(f"Username GitHub: {github_username}")

# Meminta URL sumber dan file untuk diupload
source_url = input("Masukkan URL sumber untuk mengunduh file GitHub: ")
repo_name = input("Masukkan nama repositori GitHub tujuan: ")
branch_name = input("Masukkan nama branch GitHub (misalnya: main): ")
file_to_upload = input("Masukkan path file yang ingin diupload (misalnya: file.txt): ")

# Menyimpan file yang diunduh ke path lokal sementara
local_file_path = "downloaded_file.txt"

# Mengunduh file dari repositori GitHub lain
print("Mengunduh file dari GitHub...")
download_from_github(source_url, local_file_path)

# Menunggu proses upload dan memberikan animasi loading
print("Mengupload file ke GitHub...")
loading_animation()  # Menampilkan animasi selama upload

# Memanggil fungsi upload ke GitHub
upload_to_github(local_file_path, repo_name, branch_name, github_username, github_token)
