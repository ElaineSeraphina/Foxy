import os
import time
from datetime import datetime
from git import Repo, GitCommandError
import requests

# Konfigurasi
repo_url_target = 'github.com/ElaineSeraphina/Foxy.git'  # Ganti dengan URL repo tujuan Anda
target_dir = '/storage/emulated/0/Foxy'  # Direktori repositori lokal
proxy_source_url = 'https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt'  # URL sumber proxy
username = 'your_github_username'  # Ganti dengan username GitHub Anda
password = 'your_github_password'  # Ganti dengan password GitHub Anda

# Fungsi untuk memeriksa dan meng-clone repo jika belum ada
def check_or_clone_repo():
    if not os.path.exists(target_dir):
        print(f'Direktori {target_dir} bukan repositori Git yang valid, meng-clone ulang...')
        try:
            Repo.clone_from(f'https://{username}:{password}@{repo_url_target}', target_dir, branch='main')
            print("Repositori berhasil di-clone.")
        except GitCommandError as e:
            print(f"Terjadi kesalahan saat cloning repo: {e}")
            raise
    else:
        try:
            repo_target = Repo(target_dir)
            print("Repositori sudah ada, melanjutkan proses.")
        except GitCommandError as e:
            print(f"Terjadi kesalahan: {e}")
            raise

# Fungsi untuk mendownload proxy terbaru
def download_proxies():
    try:
        response = requests.get(proxy_source_url)
        response.raise_for_status()
        return response.text.splitlines()
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan saat mengunduh proxy: {e}")
        return []

# Fungsi untuk menghindari duplikat proxy dan menyimpan file
def save_proxies_to_file(proxies):
    timestamp = datetime.now().strftime('%d_%m_%Y_%H_%M')
    filename = f"{timestamp}.txt"
    filepath = os.path.join(target_dir, filename)

    with open(filepath, 'w') as f:
        for proxy in proxies:
            f.write(proxy + '\n')

    print(f"File {filename} berhasil disimpan.")

    return filepath

# Fungsi untuk menambahkan dan meng-commit perubahan ke repositori Git
def commit_and_push_to_repo(filepath):
    try:
        repo_target = Repo(target_dir)
        repo_target.git.add(A=True)
        repo_target.index.commit(f"Add new proxy list: {os.path.basename(filepath)}")
        origin = repo_target.remote(name='origin')
        origin.push('main')
        print(f"File {os.path.basename(filepath)} berhasil di-upload ke repositori.")
    except GitCommandError as e:
        print(f"Terjadi kesalahan saat mengunggah ke GitHub: {e}")
        raise

# Main function
def main():
    check_or_clone_repo()

    print("Memulai proses unduhan dan unggahan pembaruan.")

    # Mengunduh daftar proxy terbaru
    proxies = download_proxies()
    if proxies:
        # Simpan daftar proxy ke file dengan timestamp
        filepath = save_proxies_to_file(proxies)

        # Commit dan upload ke repositori GitHub
        commit_and_push_to_repo(filepath)
    else:
        print("Tidak ada proxy yang berhasil diunduh, proses dibatalkan.")

if __name__ == '__main__':
    main()
