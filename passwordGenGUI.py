import random
import string

ERROR_MESSAGE = {
    "TooSmall": "ERROR: The minimum password length is 8 characters",
    "ZeroPasswords": "ERROR: Please enter a number greater than 0",
}

def generate_password(length, include_uppercase, include_lowercase, include_numbers, include_symbols):
    characters = ''
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_numbers:
        characters += string.digits
    if include_symbols:
        characters += string.punctuation

    return ''.join(random.choice(characters) for _ in range(length))

def generate_passwords(length, include_uppercase, include_lowercase, include_numbers, include_symbols,
                       num_passwords, separate_files, num_files, file_name):
    try:
        with open(file_name, "a+") as file:
            file.seek(0)
            generated_passwords = set(password.strip() for password in file.readlines())

            while num_passwords > len(generated_passwords):
                password = generate_password(length, include_uppercase, include_lowercase, include_numbers,
                                             include_symbols)
                if password not in generated_passwords:
                    file.write(password + "\n")
                    generated_passwords.add(password)

        if separate_files and num_files > 1:
            passwords = list(generated_passwords)
            passwords_per_file = (num_passwords + num_files - 1) // num_files

            for i in range(num_files):
                start_idx = i * passwords_per_file
                end_idx = min((i + 1) * passwords_per_file, num_passwords)

                file_suffix = f"_{i + 1}" if num_files > 1 else ""

                new_file_name = f"{file_name}{file_suffix}.txt"

                with open(new_file_name, 'w') as file:
                    file_passwords = passwords[start_idx:end_idx]
                    file.writelines('%s\n' % password for password in file_passwords)

    except ValueError:
        print(ERROR_MESSAGE["TooSmall"])
    except IOError:
        print("Unable to create the file.")

def get_yes_no_input(prompt):
    while True:
        user_input = input(prompt).lower()
        if user_input in ['yes', 'no', 'y', 'n']:
            return user_input == 'yes' or user_input == 'y'
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.")

def generate_passwords_cli():
    try:
        length = int(input("Length of the password (min 8): "))
        if length < 8:
            print(ERROR_MESSAGE["TooSmall"])
            return

        include_uppercase = get_yes_no_input("Include uppercase letters? (yes/no): ")
        include_lowercase = get_yes_no_input("Include lowercase letters? (yes/no): ")
        include_numbers = get_yes_no_input("Include numbers? (yes/no): ")
        include_symbols = get_yes_no_input("Include symbols? (yes/no): ")

        separate_files = get_yes_no_input("Do you want to separate your file? (yes/no): ")
        if separate_files:
            num_files = int(input("How many files do you want to create? "))
        else:
            num_files = 1

        file_name = input("Name of file to store the password (press Enter for default 'password.txt'): ").strip()
        if file_name == "":
            file_name = "password.txt"

        num_passwords = int(input("How many passwords do you want to create? "))

        generate_passwords(length, include_uppercase, include_lowercase, include_numbers, include_symbols,
                           num_passwords, separate_files, num_files, file_name)

    except ValueError:
        print(ERROR_MESSAGE["TooSmall"])
    except IOError:
        print("Unable to create the file.")


if __name__ == "__main__":
    generate_passwords_cli()
