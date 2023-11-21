import random
import string

ERROR_MESSAGE = {
    "ValueError": "ERROR: Please enter a valid number",
    "TooSmall": "ERROR: The minimum password length is 8 characters",
    "InvalidChoice": "ERROR: Please enter 'yes' or 'no'",
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


while True:
    try:
        length = int(input("Length of the password (min 8): "))

        if length < 8:
            print(ERROR_MESSAGE["TooSmall"])
            continue  # Restart the loop to re-prompt for the length

        include_uppercase = input("Include uppercase letters? (y/n): ").lower() in ['yes', 'y']
        include_lowercase = input("Include lowercase letters? (y/n): ").lower() in ['yes', 'y']
        include_numbers = input("Include numbers? (y/n): ").lower() in ['yes', 'y']
        include_symbols = input("Include symbols? (y/n): ").lower() in ['yes', 'y']

        if not (include_uppercase or include_lowercase or include_numbers or include_symbols):
            print("Please select at least one type of character.")
            continue  # Restart the loop for character type selection

        dosave = input("Do you want to save the password (y/n)? ").lower()

        if dosave not in ["yes", "y", "no", "n"]:
            print(ERROR_MESSAGE["InvalidChoice"])
            continue  # Restart the loop to re-prompt for saving choice

        if dosave in ["yes", "y"]:
            num_passwords = int(input("How many passwords do you want to create? "))

            if num_passwords <= 0:
                print(ERROR_MESSAGE["ZeroPasswords"])
                continue  # Restart the loop for a valid number of passwords

            filename = input("Name of file to store the password: ").lower() + ".txt"

            with open(filename, "a+") as file:
                file.seek(0)
                generated_passwords = set(password.strip() for password in file.readlines())

                while num_passwords > len(generated_passwords):
                    password = generate_password(length, include_uppercase, include_lowercase, include_numbers,
                                                 include_symbols)
                    if password not in generated_passwords:
                        file.write(password + "\n")
                        generated_passwords.add(password)

                break
        else:
            password = generate_password(length, include_uppercase, include_lowercase, include_numbers, include_symbols)
            print("Generated Password:", password)
            break

    except ValueError:
        print(ERROR_MESSAGE["ValueError"])
