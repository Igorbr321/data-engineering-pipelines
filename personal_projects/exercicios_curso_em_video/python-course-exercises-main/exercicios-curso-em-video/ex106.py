def title(msg, color='\033[:m'):
    """Prints a title message with color formatting."""
    print(color, end='')
    print('~' * (len(msg) + 4))
    print(f'  {msg}')
    print('~' * (len(msg) + 4))
    print('\033[m')

def read(text, type='S', size=99):
    """Returns content received from the keyboard.

    Args:
        text (str): The prompt message displayed on the screen for entering data.
        type (str, optional): The type of return value can be 'i', 's', or 'f' where:
            'i' = for integer value (default is string)
            's' = for string
            'f' = for float
        size (int, optional): The maximum number of digits allowed (default is 99).

    Returns:
        str, int, or float: The value entered by the user.
    """
    if type.upper() == 'S':
        a = str(input(text)[:size])
    elif type.upper() == 'I':
        a = int(input(text)[:size])
    elif type.upper() == 'F':
        a = float(input(text)[:size])
    return a

# Main Program
from time import sleep

while True:
    title('PYHELP SYSTEM', '\033[42:38m')  # Print title with green background
    text = read('Function or library > ')  # Prompt user input for function or library name
    if text.upper() == 'END':
        break  # Exit loop if user inputs 'END'
    title(f"Accessing '{text}' command manual", '\033[46:38m')  # Print title with cyan background
    sleep(2)  # Sleep for 2 seconds
    print(f'\033[47:30m')
    help(len)  # Display help manual for the specified command
