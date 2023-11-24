import random
import string
import argparse
import tarfile
import os

ERROR_MESSAGE = {
    "TooSmall": "ERROR: The minimum password length is 8 characters",
    "ZeroPasswords": "ERROR: Please enter a number greater than 0",
    "FileCreationError": "ERROR: Unable to create the file",
}

def generate_password(length, include_uppercase, include_lowercase, include_numbers, include_symbols):
    characters = ''.join([
        string.ascii_uppercase if include_uppercase else '',
        string.ascii_lowercase if include_lowercase else '',
        string.digits if include_numbers else '',
        string.punctuation if include_symbols else '',
    ])

    return ''.join(random.choice(characters) for _ in range(length))

def main():
    parser = argparse.ArgumentParser(description='Password Generator')
    parser.add_argument('-l', '--length', type=int, default=8, help='Length of the password (default: 8)')
    parser.add_argument('-u', '--upper', action='store_true', help='Include uppercase letters')
    parser.add_argument('-w', '--lower', action='store_true', help='Include lowercase letters')
    parser.add_argument('-n', '--numbers', action='store_true', help='Include numbers')
    parser.add_argument('-s', '--symbols', action='store_true', help='Include symbols')
    parser.add_argument('-q', '--quantity', type=int, default=1, help='Number of passwords to generate (default: 1)')
    parser.add_argument('-o', '--output', default='passwords.txt', help='Output file name')
    parser.add_argument('-z', '--zip', action='store_true', help='Create a .tar.gz file')

    args = parser.parse_args()

    try:
        length = max(args.length, 8)
        num_passwords = max(args.quantity, 1)

        include_uppercase = args.upper or (not any([args.upper, args.lower, args.numbers, args.symbols]))
        include_lowercase = args.lower or (not any([args.upper, args.lower, args.numbers, args.symbols]))
        include_numbers = args.numbers or (not any([args.upper, args.lower, args.numbers, args.symbols]))
        include_symbols = args.symbols or (not any([args.upper, args.lower, args.numbers, args.symbols]))

        filename = args.output

        with open(filename, "a+") as file:
            generated_passwords = {password.strip() for password in file}

            while num_passwords > len(generated_passwords):
                password = generate_password(length, include_uppercase, include_lowercase,
                                             include_numbers, include_symbols)
                if password not in generated_passwords:
                    file.write(password + "\n")
                    generated_passwords.add(password)

        if args.zip:
            zip_filename = os.path.join(args.output + '.tar.gz')
            with tarfile.open(zip_filename, 'w:gz') as tar:
                tar.add(filename, arcname=os.path.basename(filename))
                os.remove(filename)

    except ValueError:
        print(ERROR_MESSAGE["TooSmall"])
    except FileNotFoundError:
        print(ERROR_MESSAGE["FileCreationError"])

if __name__ == "__main__":
    main()
