import os

class TextEditor:
    def __init__(self):
        self.file_path = ""
        self.buffer = ""

    def load_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.buffer = file.read()
        except FileNotFoundError:
            print("File not found.")

    def save_file(self):
        if not self.file_path:
            self.file_path = input("Enter file path to save: ")

        with open(self.file_path, 'w') as file:
            file.write(self.buffer)
        print("File saved.")

    def edit_content(self):
        os.system('clear' if os.name == 'posix' else 'cls')  # Clear the screen (Linux/Windows)
        print("Simple Text Editor")
        print("File: {}".format(self.file_path))
        print("\n" + self.buffer)

        user_input = input("\nCommands: (q)uit, (w)rite, (e)dit > ")

        if user_input == 'q':
            return False
        elif user_input == 'w':
            self.save_file()
            input("Press Enter to continue...")
        elif user_input == 'e':
            new_content = input("Enter new content:\n")
            self.buffer = new_content
        else:
            print("Invalid command. Press Enter to continue...")

        return True
    
def main():
    editor = TextEditor()

    while editor.edit_content():
        pass

if __name__ == "__main__":
    main()