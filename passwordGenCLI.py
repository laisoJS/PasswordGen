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
    """
    Generate a random password based on specified criteria.

    :param length: Length of the password.
    :type length: int

    :param include_uppercase: Include uppercase letters.
    :type include_uppercase: bool

    :param include_lowercase: Include lowercase letters.
    :type include_lowercase: bool

    :param include_numbers: Include numbers.
    :type include_numbers: bool

    :param include_symbols: Include symbols.
    :type include_symbols: bool

    :return: A randomly generated password.
    :rtype: str
    """
    characters = ''.join([
        string.ascii_uppercase if include_uppercase else '',
        string.ascii_lowercase if include_lowercase else '',
        string.digits if include_numbers else '',
        string.punctuation if include_symbols else '',
    ])

    return ''.join(random.choice(characters) for _ in range(length))


def main():
    """
    Main function to generate passwords based on provided arguments.

    Handles argument parsing, password generation, and optional file zipping.

    Raises:
        ValueError: If the provided length is smaller than 8.
        IOError: If there's an issue creating the file.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description='Password Generator')
    parser.add_argument('-l', '--length', type=int, default=8, help='Length of the password (default: 8)')
    parser.add_argument('-u', '--upper', action='store_true', help='Include uppercase letters')
    parser.add_argument('-w', '--lower', action='store_true', help='Include lowercase letters')
    parser.add_argument('-n', '--numbers', action='store_true', help='Include numbers')
    parser.add_argument('-s', '--symbols', action='store_true', help='Include symbols')
    parser.add_argument('-q', '--quantity', type=int, default=1, help='Number of passwords to generate (default: 1)')
    parser.add_argument('-o', '--output', default='passwords.txt', help='Output file name')
    parser.add_argument('--sep', type=int, default=1, help='Number of files to create')
    parser.add_argument('-z', '--zip', action='store_true', help='Create a .tar.gz file')

    args = parser.parse_args()

    try:
        length = max(args.length, 8)
        num_passwords = max(args.quantity, 1)
        num_files = max(args.sep, 1)

        include_uppercase = args.upper or (not any([args.upper, args.lower, args.numbers, args.symbols]))
        include_lowercase = args.lower or (not any([args.upper, args.lower, args.numbers, args.symbols]))
        include_numbers = args.numbers or (not any([args.upper, args.lower, args.numbers, args.symbols]))
        include_symbols = args.symbols or (not any([args.upper, args.lower, args.numbers, args.symbols]))

        filename = args.output

        passwords = [
            generate_password(length, include_uppercase, include_lowercase, include_numbers, include_symbols)
            for _ in range(num_passwords)
        ]

        passwords_per_file = (num_passwords + num_files - 1) // num_files

        if args.zip:
            for i in range(num_files):
                file_name = f"{filename}_{i + 1}.txt"
                with open(file_name, 'w') as file:
                    file_passwords = passwords[i * passwords_per_file:(i + 1) * passwords_per_file]
                    file.writelines('%s\n' % password for password in file_passwords)

            with tarfile.open(f'{args.output}.tar.gz', 'w:gz') as tar:
                for i in range(num_files):
                    file_name = f"{filename}_{i + 1}.txt"
                    tar.add(file_name, arcname=os.path.basename(file_name))

            # Clean up: remove individual text files after zipping
            for i in range(num_files):
                file_name = f"{filename}_{i + 1}.txt"
                os.remove(file_name)
        else:
            for i in range(num_files):
                file_name = f"{filename}_{i + 1}.txt"
                with open(file_name, 'w') as file:
                    file_passwords = passwords[i * passwords_per_file:(i + 1) * passwords_per_file]
                    file.writelines('%s\n' % password for password in file_passwords)

    except ValueError:
        print(ERROR_MESSAGE["TooSmall"])
    except IOError as e:
        print(ERROR_MESSAGE["FileCreationError"], e)


if __name__ == "__main__":
    main()
