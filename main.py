import os
import git
import requests
from git import Repo, GitCommandError
from datetime import datetime
import time

# URL file sumber dan repo target
url_source = 'https://raw.githubusercontent.com/BreakingTechFr/Proxy_Free/proxies/all.txt'
repo_url_target = 'https://github.com/ElaineSeraphina/Foxy.git'

# Direktori lokal untuk repo target
local_dir = '/tmp/Proxy_Free'
target_dir = '/tmp/Foxy'

# Path untuk file kredensial dan file log
credentials_path = '/storage/emulated/0/github/file.txt'
log_file = '/storage/emulated/0/script_log.txt'

# Fungsi untuk mencatat log ke file
def write_log(message):
    with open(log_file, 'a') as log:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log.write(f"[{timestamp}] {message}\n")
    print(message)

# Fungsi untuk membaca username dan password dari file
def get_credentials():
    with open(credentials_path, 'r') as file:
        username, password = file.read().strip().split(':')
    return username, password

# Fungsi untuk mendownload file dari URL sumber
def download_file():
    response = requests.get(url_source)
    if response.status_code == 200:
        # Format nama file berdasarkan waktu download
        now = datetime.now()
        file_name = now.strftime("%H_%d_%m_%Y") + ".txt"
        file_path = os.path.join(local_dir, file_name)
        
        # Simpan file yang didownload dengan nama waktu
        with open(file_path, 'wb') as f:
            f.write(response.content)
        write_log(f"File {file_name} berhasil didownload dari {url_source}.")
        return file_path
    else:
        write_log(f"Gagal mengunduh file dari {url_source}. HTTP Status: {response.status_code}")
        return None

# Update repository target dengan file baru yang diberi nama sesuai format waktu
def update_target_repo(file_path):
    # Baca kredensial GitHub
    username, password = get_credentials()
    
    # Clone repo target jika belum ada
    if not os.path.exists(target_dir):
        repo_target = Repo.clone_from(f'https://{username}:{password}@{repo_url_target}', target_dir, branch='main')
        write_log("Cloned repository target for the first time.")
    else:
        repo_target = Repo(target_dir)
    
    # Salin file yang didownload ke target directory dan lakukan commit serta push ke branch 'main'
    os.system(f'cp {file_path} {target_dir}')
    repo_target.git.add(A=True)
    repo_target.index.commit(f"Auto update: {os.path.basename(file_path)}")
    write_log(f"File {file_path} berhasil ditambahkan dan di-commit ke repo target.")
    
    # Pastikan push berhasil
    upload_success = False
    retries = 3
    while not upload_success and retries > 0:
        try:
            repo_target.remotes.origin.push(refspec='main:main')
            write_log(f"Upload berhasil untuk {os.path.basename(file_path)} ke branch 'main'.")
            upload_success = True
        except GitCommandError as e:
            retries -= 1
            write_log(f"Gagal upload: {e}. Mencoba ulang ({3 - retries} / 3)")
            time.sleep(5)  # Jeda 5 detik sebelum mencoba lagi

    if not upload_success:
        write_log("Gagal upload setelah 3 percobaan. Periksa koneksi atau kredensial.")

# Main proses: download dan upload file
def main():
    write_log("Memulai script. Tekan Ctrl+C untuk menghentikan...")
    try:
        while True:
            # Mendownload file baru dari URL sumber
            file_path = download_file()
            if file_path:
                # Jika download berhasil, lanjutkan dengan upload ke repo target
                update_target_repo(file_path)
            else:
                write_log("Tidak ada file baru untuk diunduh.")
            
            # Tunggu selama 30 menit sebelum mencoba lagi
            time.sleep(1800)
    except KeyboardInterrupt:
        write_log("Script dihentikan oleh pengguna.")

# Jalankan fungsi utama
if __name__ == "__main__":
    main()
