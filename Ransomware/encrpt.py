import os
import shutil
import logging
import random
import string
from getpass import getpass
from cryptography.fernet import Fernet
from tqdm import tqdm

logging.basicConfig(filename='encryption.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def encrypt_data(data_path, key):
    try:
        with open(data_path, "rb") as file_data:
            data = file_data.read()
        encrypted_data = Fernet(key).encrypt(data)
        with open(data_path + ".encrypted", "wb") as file_encrypted:
            file_encrypted.write(encrypted_data)
        os.remove(data_path)
        logging.info(f"Encrypted: {data_path}")
    except Exception as e:
        logging.error(f"Failed to encrypt {data_path}: {str(e)}")

def encrypt_directory(directory_path, key, extensions=None):
    for folder, subfolders, files in os.walk(directory_path):
        for file_name in tqdm(files, desc="Encrypting files"):
            file_path = os.path.join(folder, file_name)
            if extensions and not any(file_path.endswith(ext) for ext in extensions):
                continue
            encrypt_data(file_path, key)

def backup_data(data):
    try:
        os.mkdir("backup")
        for item in data:
            random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
            backup_filename = os.path.join("backup", os.path.splitext(os.path.basename(item))[0] + '_' + random_suffix + os.path.splitext(os.path.basename(item))[1])
            shutil.copy2(item, backup_filename)
    except Exception as e:
        logging.error(f"Failed to create backup: {str(e)}")

def generate_encryption_key():
    password = getpass("Enter a password to generate the encryption key: ")
    return Fernet.generate_key()

data = [item for item in os.listdir() if os.path.isfile(item)]
logging.info("Files to encrypt: " + ', '.join(data))

key = generate_encryption_key()

with open("key.key", "wb") as key_file:
    key_file.write(key)
logging.info("Encryption key generated and saved.")

for item in data:
    encrypt_data(item, key)

current_directory = os.getcwd()
encrypt_directory(current_directory, key, extensions=['.txt', '.docx'])

backup_data(data)
logging.info("Backup created.")

print("Encryption completed. Check encryption.log for details.")
