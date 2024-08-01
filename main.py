import glob
import os
import sys

from source import parser

COLORS = {
    "black": "\u001b[30;1m",
    "red": "\u001b[31;1m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33;1m",
    "blue": "\u001b[34;1m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m",
    "yellow-bg": "\u001b[43m",
    "black-bg": "\u001b[40m",
    "cyan-bg": "\u001b[46;1m",
    "bright-white": "\u001b[37;1m",
    "bright-red": "\u001b[31;1m",
    "bright-cyan": "\u001b[36;1m",
    "bright-blue-bg": "\u001b[44;1m",
    "r": "\u001b[0m",
}


def colorText(text):
    for color in COLORS:
        text = text.replace("[[" + color + "]]", COLORS[color])
    return text


def remove_temp_files():
    temp_path = 'saved/.temp'
    # Get all files in the folder
    files = glob.glob(os.path.join(temp_path, '*'))

    # Iterate over each file and remove it
    for file_path in files:
        try:
            if os.path.isfile(file_path):  # Ensure it's a file, not a directory
                os.remove(file_path)
                print(f"Temp file removed")
        except Exception as e:
            print(f"Error removing {file_path}: {e}")


def svtotal_exit(exit_code=0):
    remove_temp_files()

    # Exit the program with the given exit code
    sys.exit(exit_code)


os.system("cls")  # use this for windows. change to os.system("clear") for linux
# Example printing out some text
intro_text = r"""[[blue]]

  ____   __     __ [[green]]  _____           _             _   [[blue]]
 / ___|  \ \   / / [[green]] |_   _|   ___   | |_    __ _  | |  [[blue]]
 \___ \   \ \ / /  [[green]]   | |    / _ \  | __|  / _` | | |  [[blue]]
  ___) |   \ V /   [[green]]   | |   | (_) | | |_  | (_| | | |  [[blue]]
 |____/     \_/    [[green]]   |_|    \___/   \__|  \__,_| |_|  [[blue]]
                                                    
    [[white]]by Daus2713 
    [[red]]Please create file myapikey.txt and add your Virus Total API key            [[magenta]]
"""

options = """
[[green]]
1 - Scan URL 
2 - Scan File

Type exit to terminate SVTotal
[[r]]"""


def main():
    while True:
        prompt_text = "[[bright-red]]svtotal> [[r]]"
        print(colorText(intro_text))

        print(colorText("[[cyan-bg]][[black]] Welcome to Simple Virus Total tool [[r]] "), end="")
        print(colorText(options))

        url_scan = ["1", "/scanurl"]
        file_scan = ["2", "/scanfile"]
        while True:
            print(colorText(prompt_text), end="")
            command = input()
            if command == "exit":
                svtotal_exit()
            elif command == 'cls' or command == 'clear':
                # Check if the user input is 'cls'
                # Clear the screen using the appropriate command for the platform
                os.system('cls' if os.name == 'nt' else 'clear')
            elif command == "svtotal":
                print(colorText("\n[[cyan-bg]][[black]] Welcome to Simple Virus Total tool [[r]] "), end="")
                print(colorText(options))
            # Scan URL
            elif command in url_scan or prompt_text == "[[bright-red]]svtotal/scanurl> [[r]]":
                if command == "/scanfile":
                    prompt_text = "[[bright-red]]svtotal/scanfile> [[r]]"
                elif prompt_text == "[[bright-red]]svtotal/scanurl> [[r]]":
                    parser.parse_url(command)
                else:
                    prompt_text = "[[bright-red]]svtotal/scanurl> [[r]]"
            elif command in file_scan or prompt_text == "[[bright-red]]svtotal/scanfile> [[r]]":
                if command == "/scanurl":
                    prompt_text = "[[bright-red]]svtotal/scanurl> [[r]]"
                elif prompt_text == "[[bright-red]]svtotal/scanfile> [[r]]":
                    parser.parse_url(command, "file")
                else:
                    prompt_text = "[[bright-red]]svtotal/scanfile> [[r]]"

            else:
                print("Invalid input! Try again")


if __name__ == "__main__":
    main()
