import os
import random
import string
import tarfile


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


def get_user_input(prompt, default=None):
    if default:
        return input(f"{prompt} [{default}]: ") or default
    else:
        return input(f"{prompt}: ")


def main():
    try:
        length = max(int(get_user_input('Length of the password', default=8)), 8)
        include_uppercase = get_user_input('Include uppercase letters? (y/n)') == 'y'
        include_lowercase = get_user_input('Include lowercase letters? (y/n)') == 'y'
        include_numbers = get_user_input('Include numbers? (y/n)') == 'y'
        include_symbols = get_user_input('Include symbols? (y/n)') == 'y'
        num_passwords = max(int(get_user_input('Number of passwords to generate', default=1)), 1)
        num_files = max(int(get_user_input('Number of files to create', default=1)), 1)
        create_zip = get_user_input('Zip the file as .tar.gz? (y/n)') == 'y'
        output_filename = get_user_input('Output file name', default='password')

        passwords = [
            generate_password(length, include_uppercase, include_lowercase, include_numbers, include_symbols)
            for _ in range(num_passwords)
        ]

        passwords_per_file = (num_passwords + num_files - 1) // num_files

        for i in range(num_files):
            file_suffix = f"_{i + 1}" if num_files > 1 else ''
            file_name = f"{output_filename}{file_suffix}.txt" if num_files > 1 else f"{output_filename}.txt"

            with open(file_name, 'w') as file:
                file_passwords = passwords[i * passwords_per_file:(i + 1) * passwords_per_file]
                file.writelines('%s\n' % password for password in file_passwords)

        if create_zip:
            with tarfile.open(f'{output_filename}.tar.gz', 'w:gz') as tar:
                for i in range(num_files):
                    file_suffix = f"_{i + 1}" if num_files > 1 else ''
                    file_name = f"{output_filename}{file_suffix}.txt" if num_files > 1 else f"{output_filename}.txt"

                    tar.add(file_name, arcname=os.path.basename(file_name))

            # Clean up: remove individual text files after zipping
            for i in range(num_files):
                file_suffix = f"_{i + 1}" if num_files > 1 else ''
                file_name = f"{output_filename}{file_suffix}.txt" if num_files > 1 else f"{output_filename}.txt"

                os.remove(file_name)

    except ValueError:
        print(ERROR_MESSAGE["TooSmall"])
    except IOError as e:
        print(ERROR_MESSAGE["FileCreationError"], e)


if __name__ == "__main__":
    main()
