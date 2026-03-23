import json
import random
import string
import getpass
from crypto import load_key
from cryptography.fernet import Fernet

# Password Manager class that handles password storage, retrieval, and management
class PasswordManager:
    def __init__(self):
        self.passwords = self.load_passwords()
        key = load_key()
        self.fernet = Fernet(key)

    ## Generates a random password of the specified length
    def generate_password(self, length):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''
        
        for _ in range(length):
            password += random.choice(characters)
        return password
    
    ## Loads passwords from the file and returns them as a list
    def load_passwords(self):
        try:
            with open('PasswordManager/passwords.json', 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    ## Saves the list of passwords to the file in JSON format
    def save_passwords(self):
        try:
            with open('PasswordManager/passwords.json', 'w') as file:
                json.dump(self.passwords,file, indent=4)
        except FileNotFoundError:
            print('Error: Could not save passwords.')

    ## Adds a new password entry to the list and saves it to the file
    def add_password(self, service, username, password):
        encrypted_password = self.fernet.encrypt(password.encode()).decode()

        entry = {
            'service': service,
            'username': username,
            'password': encrypted_password
        }    
        self.passwords.append(entry)
        self.save_passwords()

    ## Shows all passwords in the list
    def show_passwords(self):
        if not self.passwords:
            print('No passwords saved!')
            return

        for i, entry in enumerate(self.passwords):
            
            decrypted_password = self.fernet.decrypt(entry["password"].encode()).decode()

            print(f'{i + 1}. Service: {entry["service"]} | Username: {entry["username"]} | Password: {decrypted_password}')

    ## Searches for a service in the list and shows the matching entries
    def search_password(self, search):
        found = False
        for entry in self.passwords:
            if search in entry['service'].lower():
                decrypted_password = self.fernet.decrypt(entry["password"].encode()).decode()
                print(f'Service: {entry["service"]} | Username: {entry["username"]} | Password: {decrypted_password}')
                found = True
        if not found:
            print('Service not found!')

    ## Edits password based on provided service name by user
    def edit_password(self, edit):
        found = False
        
        for entry in self.passwords:
            if edit in entry['service'].lower():
                new_password = input('Enter new password.')
                while True:
                    confirm = input('Are you sure you want to change the password? (y/n) ').lower()
                
                    if confirm == 'y':
                        encrypted_password = self.fernet.encrypt(new_password.encode()).decode()
                        entry['password'] = encrypted_password
                        self.save_passwords()
                        print('Password updated!')
                        found = True
                        return
                    elif confirm == 'n':
                        print('Password not updated!')
                        found = True
                        return
                    else:
                        print('Please enter y or n!')
        if not found:
            print('Service not found!') 

    ## Deletes a password entry based on the index provided by the user
    def delete_password(self):
        while True:
            try:
                index = int(input("Enter index password to remove: "))
                if index < 1 or index > len(self.passwords):
                    print('Password does not exist')
                    break
                else:
                    self.passwords.pop(index - 1)
                    self.save_passwords()
                    print('Password removed!')
                    break
            except ValueError:
                print('Please enter a number!')

    ## Main menu loop
    def main(self):   
        while True:
            print('1 - Add password')
            print('2 - Show passwords')
            print('3 - Search password')
            print('4 - Remove password')
            print('5 - Edit password')
            print('6 - Generate password')
            print('7 - Exit')

            choice = input('Choose an option: ')
            if choice == '1':
                service = input('Enter service: ')
                username = input('Enter username: ')
                password = getpass.getpass('Enter password: ')
                self.add_password(service, username, password)
                
            elif choice == '2':
                self.show_passwords()
            elif choice == '3':
                search = input('Enter service to search: ').lower()
                self.search_password(search)
            elif choice == '4':
                self.delete_password()
            elif choice == '5':
                edit = input('Enter name of service of password you wish to edit: ').lower()
                self.edit_password(edit)
            elif choice == '6':
                while True:
                    try:
                        length = int(input('Enter password length: '))
                        break
                    except ValueError:
                        print('Please enter a number!')

                password = self.generate_password(length)
                print(f'Generated password: {password}')
                save = input(f'Use this password ? (y/n)')

                if save.lower() == 'y':
                    service = input('Enter service: ')
                    username = input('Enter username: ')
                    self.add_password(service, username, password)
                elif save.lower() == 'n':
                    print('Password not saved!')
                else:
                    print('Please enter y or n!')
            elif choice == '7':
                break