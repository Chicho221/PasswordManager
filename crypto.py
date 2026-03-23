# Loads the encryption key from the file
def load_key():
    try:
        with open('PasswordManager/key.key', 'rb') as file:
            return file.read()
    except FileNotFoundError:       
        raise SystemExit('Error: Encryption key not found. Please create a key.key file with a valid Fernet key.')