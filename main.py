from manager import PasswordManager
from auth import Authentication

if __name__ == "__main__":
    auth = Authentication()

    if auth.verify_master_password():
        manager = PasswordManager()
        manager.main()