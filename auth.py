import hashlib

class Authentication():
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # Sets up the master password by hashing it and saving it to a file
    def setup_master_password(self):
        master = input('Create master password: ')

        hashed = self.hash_password(master)
        with open('PasswordManager/master_password.txt', 'w') as file:
            file.write(hashed)

        print('Master password has been created!')

    # Verifies the master password by comparing the hashed input with the stored hash
    def verify_master_password(self):
        try:
            with open('PasswordManager/master_password.txt', 'r') as file:
                saved_password = file.read()
        except FileNotFoundError:
            self.setup_master_password()
            return True
        tries = 1
        while True:
            entered = input('Enter master password: ')

            if self.hash_password(entered) == saved_password:
                print('Access granted!')
                return True
            elif tries < 3:
                print('Incorrect password, try again!')
                tries += 1
            else:
                print('Access denied!')
                return False