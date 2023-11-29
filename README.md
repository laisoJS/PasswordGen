# PasswordGenCLI

This script generates random passwords based on specified criteria.

## Usage

### Prerequisites
- Python 3.x installed

### Running the Script

1. **Clone the repository:**
    ```bash
    git clone https://github.com/laisoJs/PasswordGen.git
    ```

2. **Navigate to the directory:**
    ```bash
    cd PasswordGen
    ```

3. **Run the script with required arguments:**
    ```bash
    python passwordGenCLI.py [-h] [-l LENGTH] [-u] [-w] [-n] [-s] [-q QUANTITY] [-o OUTPUT] [--sep SEP] [-z]
    ```
    #### Arguments
    - `-h`, `--help`: Show help message and exit.
    - `-l LENGTH`, `--length LENGTH`: Length of the password (default: 8).
    - `-u`, `--upper`: Include uppercase letters.
    - `-w`, `--lower`: Include lowercase letters.
    - `-n`, `--numbers`: Include numbers.
    - `-s`, `--symbols`: Include symbols.
    - `-q QUANTITY`, `--quantity QUANTITY`: Number of passwords to generate (default: 1).
    - `-o OUTPUT`, `--output OUTPUT`: Output file name (default: passwords.txt).
    - `--sep SEP`: Number of files to create (default: 1).
    - `-z`, `--zip`: Create a .tar.gz file.

### Examples

- Generate a password with default settings:
    ```bash
    python passwordGenCLI.py
    ```

- Generate a password with specific criteria:
    ```bash
    python passwordGenCLI.py --length 12 --upper --numbers --symbols
    ```

- Generate multiple passwords into separate files:
    ```bash
    python passwordGenCLI.py --quantity 10 --sep 3
    ```

- Generate passwords and create a compressed file:
    ```bash
    python passwordGenCLI.py --length 10 --upper --numbers --zip
    ```

### Notes

- Passwords will be saved in a text file (`passwords.txt` by default) unless the `-z` flag is used to create a compressed `.tar.gz` file.
- Ensure a minimum length of 8 characters for passwords.
