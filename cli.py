import os
import platform
from prompt_toolkit import PromptSession
from prompt_toolkit.validation import Validator, ValidationError
from colorama import Fore, Style, init
# Ensure these imports are correct based on your application structure
from app import app  # Import the Flask app
from db_operations import add_user, get_users, update_user, delete_user  # Importing functions from db_operations
from tabulate import tabulate

init(autoreset=True)

logo = r"""
       .d8b.                                 
       _.d8888888b._                                     
     .88888888888888b.               (      (      (      (
    d88888888888888888b              )\     )\ )   )\     )\ )    )    (
    8888888888888888888              ((((_)(  (()/( ((((_)(  (()/(   (     )\   (
    Y88888888888888888P               )\ _ )\  ((_))  )\ _ )\  ((_))  )\  '((_)  )\ )
     'Y8888888888888P'                (_)_\(_) _| |  (_)_\(_) _| | _((_))  (_) _(_/(
   _..._ 'Y88888P' _..._               / _ \ / _` || '  \()  / _ \ / _` || '  \() | || ' \)) 
 .d88888b. Y888P .d88888b.            /_/ \_\\__,_||_|_|_|  /_/ \_\\__,_||_|_|_|  |_||_||_|
d888888888b 888 d88888888b
888P  `Y8888888888P'  Y888
 b8b    Y88888888P    d8Y
  `"'  #############  '"`
         dP d8b Yb
     Ob=dP d888b Yb=dO
      `"` O88888O `"`
   jgs     'Y8P'

"""

class EmailValidator(Validator):
    def validate(self, document):
        if "@" not in document.text or "." not in document.text:
            raise ValidationError(message="Please enter a valid email", cursor_position=len(document.text))

def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    print(f"{Fore.YELLOW}{logo}{Style.RESET_ALL}")

def handle_add_user():
    session = PromptSession()

    username = session.prompt(f"{Fore.BLUE}Enter username: {Style.RESET_ALL}")
    email = session.prompt(f"{Fore.BLUE}Enter email: {Style.RESET_ALL}", validator=EmailValidator())

    with app.app_context():
        try:
            response = add_user(username, email)
            print(f"{Fore.YELLOW}{response}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}An error occurred: {e}{Style.RESET_ALL}")

def handle_get_users():
    with app.app_context():
        try:
            users = get_users()
            user_table = [[user.id, user.username, user.email] for user in users]
            print(f"{Fore.YELLOW}{tabulate(user_table, headers=['ID', 'Username', 'Email'], tablefmt='grid')}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}An error occurred: {e}{Style.RESET_ALL}")

def handle_update_user():
    session = PromptSession()

    user_id = session.prompt(f"{Fore.BLUE}Enter user ID to update: {Style.RESET_ALL}")
    new_username = session.prompt(f"{Fore.BLUE}Enter new username: {Style.RESET_ALL}")
    new_email = session.prompt(f"{Fore.BLUE}Enter new email: {Style.RESET_ALL}", validator=EmailValidator())

    with app.app_context():
        try:
            response = update_user(user_id, new_username, new_email)
            print(f"{Fore.YELLOW}{response}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}An error occurred: {e}{Style.RESET_ALL}")

def handle_delete_user():
    session = PromptSession()

    user_id = session.prompt(f"{Fore.BLUE}Enter user ID to delete: {Style.RESET_ALL}")

    with app.app_context():
        try:
            response = delete_user(user_id)
            print(f"{Fore.YELLOW}{response}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}An error occurred: {e}{Style.RESET_ALL}")

def main():
    print(f"{Fore.YELLOW}{logo}{Style.RESET_ALL}")
    while True:
        user_input = PromptSession().prompt(f"{Fore.BLUE}VyomWatching> {Style.RESET_ALL}").strip()
        if not user_input:
            continue

        command = user_input.split()[0].lower()

        if command == 'exit':
            break
        elif command == 'clear':
            clear_screen()
        elif command == 'add_user':
            handle_add_user()
        elif command == 'get_users':
            handle_get_users()
        elif command == 'update_user':
            handle_update_user()
        elif command == 'delete_user':
            handle_delete_user()
        elif command == 'help':
            print(f"{Fore.YELLOW}Available commands: add_user, get_users, update_user, delete_user, clear, exit{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Unknown command: {command}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
