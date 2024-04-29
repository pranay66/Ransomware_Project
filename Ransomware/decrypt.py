import os
import shutil
from cryptography.fernet import Fernet
from tqdm import tqdm

def decrypt_file(file_path, key):
    try:
        with open(file_path, "rb") as file:
            encrypted_contents = file.read()
            decrypted_contents = Fernet(key).decrypt(encrypted_contents)
        with open(file_path, "wb") as file:
            file.write(decrypted_contents)
        
        # Check file integrity
        original_size = os.path.getsize(file_path + ".encrypted")
        decrypted_size = os.path.getsize(file_path)
        if original_size == decrypted_size:
            print(f"Decrypted: {file_path}")
        else:
            print(f"Warning: Decryption of {file_path} may not be successful. File size mismatch.")
            
        # Delete the encrypted file
        os.remove(file_path + ".encrypted")
        print(f"Deleted encrypted file: {file_path}.encrypted")
    except Exception as e:
        print(f"Failed to decrypt {file_path}: {e}")

def decrypt_directory(directory_path, key):
    for root, _, filenames in os.walk(directory_path):
        for filename in tqdm(filenames, desc="Decrypting files"):
            if filename not in ["encrpt.py", "decrypt.py", "edkey.key"]:
                file_path = os.path.join(root, filename)
                decrypt_file(file_path, key)

def decrypt_current_directory(key):
    current_directory = os.getcwd()
    for filename in os.listdir(current_directory):
        file_path = os.path.join(current_directory, filename)
        if os.path.isfile(file_path) and filename.endswith(".encrypted"):
            decrypt_file(file_path, key)

def main():
    key_file_path = os.path.join(os.getcwd(), "edkey.key")
    if not os.path.exists(key_file_path):
        print("Key file 'edkey.key' not found. Make sure the key file exists.")
        return

    with open(key_file_path, "rb") as key_file:
        key = key_file.read()
        if not key:
            print("Key file is empty. Please make sure it contains the encryption key.")
            return

    print("Decrypting files in the current directory...")
    decrypt_current_directory(key)

    print("\nDecrypting files in child folders...")
    decrypt_directory(os.getcwd(), key)

    print("\nDecryption completed.")

if __name__ == "__main__":
    main()
