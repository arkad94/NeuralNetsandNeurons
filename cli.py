# Import the os library to interact with the operating system.
import os
# Import the platform library to identify the type of operating system.
import platform
# Import PromptSession to create an interactive command line session.
from prompt_toolkit import PromptSession
# Import Validator and ValidationError to create custom input validation rules.
from prompt_toolkit.validation import Validator, ValidationError
# Import Fore and Style for colored text in the terminal, and init to initialize colorama with autoreset.
from colorama import Fore, Style, init
# Import the Flask app to use it within the command line interface.
from app import app
# Import database operation functions to add, retrieve, update, and delete users.
from db_operations import add_user, get_users, update_user, delete_user
# Import tabulate to nicely format tables in the command line output.
from tabulate import tabulate

# Initialize colorama to automatically reset text color after each print statement.
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

# Define a custom Validator class to check if input text is a valid email.
class EmailValidator(Validator):
    # Define the validation logic: the email should contain an "@" and a "."
    def validate(self, document):
        if "@" not in document.text or "." not in document.text:
            # If the condition is not met, raise a ValidationError with a helpful message.
            raise ValidationError(message="Please enter a valid email", cursor_position=len(document.text))


# Define a function to clear the terminal screen.
def clear_screen():
    # Use the 'cls' command for Windows, 'clear' for other operating systems.
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    # Print the logo with yellow color using the Fore module from colorama.
    print(f"{Fore.YELLOW}{logo}{Style.RESET_ALL}")

# Define a function to handle the 'add_user' command.
def handle_add_user():
    # Start a new prompt session for interactive input.
    session = PromptSession()

 # Prompt for a username with blue text color.
    username = session.prompt(f"{Fore.BLUE}Enter username: {Style.RESET_ALL}")
    # Prompt for an email with blue text color, using the custom EmailValidator.
    email = session.prompt(f"{Fore.BLUE}Enter email: {Style.RESET_ALL}", validator=EmailValidator())

# Wrap the following code in the Flask application context.
    with app.app_context():
        try:
            # Try to add a user with the provided username and email.
            response = add_user(username, email)
            # Print a success message with yellow text color.
            print(f"{Fore.YELLOW}{response}{Style.RESET_ALL}")
        except Exception as e:
            # If an exception occurs, print an error message with yellow text color.
            print(f"{Fore.YELLOW}An error occurred: {e}{Style.RESET_ALL}")

            # Each function follows a similar pattern: prompt for input, call a db_operations function, and handle exceptions.

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

# Define the main function to run the command line interface.
def main():
    # Print the logo with yellow color at the start of the program.
    print(f"{Fore.YELLOW}{logo}{Style.RESET_ALL}")

    # Enter an infinite loop to continuously accept commands.
    while True:
        # Prompt for a command with blue text color and a custom prompt text.
        user_input = PromptSession().prompt(f"{Fore.BLUE}VyomWatching> {Style.RESET_ALL}").strip()
        # If no command is entered, start the loop again.
        if not user_input:
            continue

        # Parse the command by taking the first word and converting it to lower case.
        command = user_input.split()[0].lower()

        # Check the command and execute the corresponding function or print a message.
        if command == 'exit':
            # If the command is 'exit', break the loop to end the program.
            break
        elif command == 'clear':
            # If the command is 'clear', call the clear_screen function to clear the terminal.
            clear_screen()
        elif command == 'add_user':
            # If the command is 'add_user', call the handle_add_user function to add a new user.
            handle_add_user()
        elif command == 'get_users':
            # Call the corresponding function for each command.
            handle_get_users()
        elif command == 'update_user':
            handle_update_user()
        elif command == 'delete_user':
            handle_delete_user()
        elif command == 'help':
            # If the command is 'help', print available commands.
            print(f"{Fore.YELLOW}Available commands: add_user, get_users, update_user, delete_user, clear, exit{Style.RESET_ALL}")
        else:
            # If an unknown command is entered, inform the user.
            print(f"{Fore.YELLOW}Unknown command: {command}{Style.RESET_ALL}")

# Check if the script is being run directly (not imported) and if so, call the main function.
if __name__ == "__main__":
    main()
