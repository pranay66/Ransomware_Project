import os
import shutil
import zipfile
import logging
from datetime import datetime

def perform_backup(source_dir, backup_dir):
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_subdir = os.path.join(backup_dir, f'backup_{now}')
    os.makedirs(backup_subdir, exist_ok=True)

    total_files_copied = 0
    total_size_copied = 0

    for root, dirs, files in os.walk(source_dir):
        dest_dir = os.path.join(backup_subdir, os.path.relpath(root, source_dir))
        os.makedirs(dest_dir, exist_ok=True)
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)
            shutil.copy2(src_file, dest_file)
            total_files_copied += 1
            total_size_copied += os.path.getsize(src_file)

    print(f'Backup completed successfully to {backup_subdir}')
    print(f'Total files copied: {total_files_copied}')
    print(f'Total size copied: {total_size_copied / (1024 * 1024):.2f} MB')

    # Compress the backup directory into a zip file
    zip_filename = os.path.join(backup_dir, f'backup_{now}.zip')
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(backup_subdir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, backup_subdir)
                zipf.write(file_path, arcname=arcname)

    print(f'Backup compressed successfully to {zip_filename}')

    # Log backup details
    logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(message)s')
    logging.info(f'Backup completed: {total_files_copied} files, {total_size_copied / (1024 * 1024):.2f} MB')

def main():
    source_directory = 'source path'
    backup_directory = 'Destination path'

    print(f'Backing up files from: {source_directory}')
    print(f'To directory: {backup_directory}')

    try:
        perform_backup(source_directory, backup_directory)
    except Exception as e:
        print(f"Error occurred during backup: {e}")
        logging.error(f"Error occurred during backup: {e}")

if __name__ == "__main__":
    main()
