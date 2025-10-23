# Impor modul yang diperlukan
import os
import shutil

# Fungsi untuk mengatur file
def organize_files():
    """
    Fungsi ini mengkategorikan file di direktori saat ini ke dalam subfolder
    berdasarkan ekstensi filenya.
    """
    # Dapatkan path direktori tempat skrip ini dijalankan
    path = os.getcwd()

    # Dapatkan daftar semua file dan folder di direktori saat ini
    files = os.listdir(path)

    print(f"Starting to organize files in: {path}\n")

    # Loop melalui setiap item di direktori
    for file in files:
        # Abaikan skrip ini sendiri dan direktori yang sudah ada
        if file == 'file_organizer.py' or os.path.isdir(file):
            continue

        # Dapatkan nama file dan ekstensinya
        filename, extension = os.path.splitext(file)
        # Hapus titik (.) dari awal ekstensi
        extension = extension[1:]

        # Jika tidak ada ekstensi, lewati file ini
        if not extension:
            continue

        # Tentukan folder tujuan berdasarkan ekstensi
        # Anda bisa menambahkan lebih banyak ekstensi dan folder di sini
        destination_folders = {
            # Gambar
            'jpeg': 'Images', 'jpg': 'Images', 'png': 'Images', 'gif': 'Images', 'bmp': 'Images', 'svg': 'Images', 'webp': 'Images',
            # Dokumen
            'pdf': 'Documents', 'doc': 'Documents', 'docx': 'Documents', 'txt': 'Documents', 'xls': 'Documents', 'xlsx': 'Documents', 'ppt': 'Documents', 'pptx': 'Documents', 'csv': 'Documents',
            # Audio
            'mp3': 'Music', 'wav': 'Music', 'aac': 'Music', 'flac': 'Music',
            # Video
            'mp4': 'Videos', 'mkv': 'Videos', 'avi': 'Videos', 'mov': 'Videos', 'wmv': 'Videos',
            # Arsip
            'zip': 'Archives', 'rar': 'Archives', 'tar': 'Archives', 'gz': 'Archives', '7z': 'Archives',
            # Kode & Program
            'py': 'Code', 'js': 'Code', 'html': 'Code', 'css': 'Code', 'cpp': 'Code', 'java': 'Code', 'sh': 'Scripts', 'exe': 'Programs', 'msi': 'Programs'
        }

        # Dapatkan nama folder tujuan, defaultnya adalah 'Others' jika ekstensi tidak ditemukan
        folder_name = destination_folders.get(extension.lower(), 'Others')

        # Buat path lengkap untuk folder tujuan
        destination_folder_path = os.path.join(path, folder_name)

        # Buat folder tujuan jika belum ada
        if not os.path.exists(destination_folder_path):
            os.makedirs(destination_folder_path)
            print(f"Created folder: {folder_name}")

        # Path lengkap file sumber
        source_path = os.path.join(path, file)
        # Path lengkap file tujuan
        destination_path = os.path.join(destination_folder_path, file)
        
        # Pindahkan file ke folder tujuan
        try:
            shutil.move(source_path, destination_path)
            print(f"Moved: '{file}'  ->  '{folder_name}'")
        except Exception as e:
            print(f"ERROR: Could not move '{file}'. Reason: {e}")

    print("\nFile organization complete!")

# Jalankan fungsi utama jika skrip dieksekusi secara langsung
if __name__ == "__main__":
    organize_files()
