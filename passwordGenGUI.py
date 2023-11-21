import string
import random
import PySimpleGUI as sg

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


layout = [
    [sg.Text("Length of the password (min 8): "), sg.InputText(key='length')],
    [sg.Text("Include uppercase letters? "), sg.Radio("Yes", "uppercase", key='uppercase'),
     sg.Radio("No", "uppercase", default=True)],
    [sg.Text("Include lowercase letters? "), sg.Radio("Yes", "lowercase", key='lowercase'),
     sg.Radio("No", "lowercase", default=True)],
    [sg.Text("Include numbers? "), sg.Radio("Yes", "numbers", key='numbers'), sg.Radio("No", "numbers", default=True)],
    [sg.Text("Include symbols? "), sg.Radio("Yes", "symbols", key='symbols'), sg.Radio("No", "symbols", default=True)],
    [sg.Text("Do you want to save the password? "), sg.Radio("Yes", "save", key='save'),
     sg.Radio("No", "save", default=True)],
    [sg.Text("How many passwords do you want to create? "), sg.InputText(key='num_passwords')],
    [sg.Text("Name of file to store the password: "), sg.InputText(key='filename')],
    [sg.Button("Generate Password")]
]

window = sg.Window("Password Generator", layout)

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    try:
        length = int(values['length'])

        if length < 8:
            sg.popup(ERROR_MESSAGE["TooSmall"])
            continue  # Restart the loop to re-prompt for the length

        include_uppercase = values['uppercase']
        include_lowercase = values['lowercase']
        include_numbers = values['numbers']
        include_symbols = values['symbols']
        save_password = values['save']

        if not (include_uppercase or include_lowercase or include_numbers or include_symbols):
            sg.popup("Please select at least one type of character.")
            continue  # Restart the loop for character type selection

        if save_password:
            num_passwords = int(values['num_passwords'])

            if num_passwords <= 0:
                sg.popup(ERROR_MESSAGE["ZeroPasswords"])
                continue  # Restart the loop for a valid number of passwords

            filename = values['filename'] + ".txt"
            generated_passwords = set()

            with open(filename, "a+") as file:
                file.seek(0)
                generated_passwords = set(password.strip() for password in file.readlines())

                while num_passwords > len(generated_passwords):
                    password = generate_password(length, include_uppercase, include_lowercase, include_numbers,
                                                 include_symbols)
                    if password not in generated_passwords:
                        file.write(password + "\n")
                        generated_passwords.add(password)

                sg.popup(f"{num_passwords} passwords generated and saved in {filename}")

        else:
            password = generate_password(length, include_uppercase, include_lowercase, include_numbers, include_symbols)
            sg.popup(f"Generated Password: {password}")

    except ValueError:
        sg.popup(ERROR_MESSAGE["ValueError"])

window.close()
