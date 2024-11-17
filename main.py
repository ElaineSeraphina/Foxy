import os
import git
from git import Repo, GitCommandError
from datetime import datetime
import time

# URL repository sumber dan target
repo_url_source = 'https://github.com/BreakingTechFr/Proxy_Free.git'
repo_url_target = 'https://github.com/ElaineSeraphina/Foxy.git'

# Direktori lokal untuk repository source dan target
local_dir = '/storage/emulated/0/Proxy_Free'
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

# Clone repository source jika belum ada
if not os.path.exists(local_dir):
    Repo.clone_from(repo_url_source, local_dir)
    write_log("Cloned repository source for the first time.")

# Cek pembaruan pada repository source
def check_for_updates():
    repo = Repo(local_dir)
    origin = repo.remotes.origin
    origin.fetch()
    if repo.head.commit != origin.refs.main.commit:
        write_log("Pembaruan ditemukan pada repository source.")
        return True
    write_log("Repository source sudah up-to-date.")
    return False

# Update repository target dengan file baru yang diberi nama sesuai format waktu
def update_target_repo():
    # Format nama file berdasarkan waktu download
    now = datetime.now()
    file_name = now.strftime("%H_%d_%m_%Y") + ".txt"
    file_path = os.path.join(local_dir, file_name)
    
    # Buat file dengan nama waktu yang ditentukan
    with open(file_path, 'w') as f:
        f.write(f"Downloaded content from {repo_url_source} at {now}")
    write_log(f"File {file_name} berhasil dibuat dengan konten dari sumber.")
    
    # Proses upload file ke branch 'main' di repo target
    username, password = get_credentials()
    
    # Clone repo target jika belum ada
    if not os.path.exists(target_dir):
        repo_target = Repo.clone_from(f'https://{username}:{password}@{repo_url_target}', target_dir, branch='main')
        write_log("Cloned repository target for the first time.")
    else:
        repo_target = Repo(target_dir)
    
    # Copy file baru ke target directory dan lakukan commit serta push ke branch 'main'
    os.system(f'cp {file_path} {target_dir}')
    repo_target.git.add(A=True)
    repo_target.index.commit(f"Auto update: {file_name}")
    write_log(f"File {file_name} berhasil ditambahkan dan di-commit ke repo target.")
    
    # Pastikan push berhasil
    upload_success = False
    retries = 3
    while not upload_success and retries > 0:
        try:
            repo_target.remotes.origin.push(refspec='main:main')
            write_log(f"Upload berhasil untuk {file_name} ke branch 'main'.")
            upload_success = True
        except GitCommandError as e:
            retries -= 1
            write_log(f"Gagal upload: {e}. Mencoba ulang ({3 - retries} / 3)")
            time.sleep(5)  # Jeda 5 detik sebelum mencoba lagi

    if not upload_success:
        write_log("Gagal upload setelah 3 percobaan. Periksa koneksi atau kredensial.")

# Main proses: cek pembaruan dan upload
def main():
    write_log("Memulai script. Tekan Ctrl+C untuk menghentikan...")
    try:
        while True:
            if check_for_updates():
                write_log("Memulai proses unduhan dan unggahan pembaruan.")
                update_target_repo()
            else:
                write_log("Tidak ada pembaruan ditemukan pada repository source.")
            time.sleep(1800)  # Cek pembaruan setiap 30 menit
    except KeyboardInterrupt:
        write_log("Script dihentikan oleh pengguna.")

# Jalankan fungsi utama
if __name__ == "__main__":
    main()