import os, sys, termios, tty

class TextEditor:
    def __init__(self):
        self.file_path = ""
        self.buffer = ""
        self.cursor_pos = 0

    def load_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                self.buffer = file.read()
            self.file_path = file_path
        except FileNotFoundError:
            print("File not found.")

    def save_file(self):
        if not self.file_path:
            self.file_path = input("Enter file path to save: ")

        with open(self.file_path, 'w') as file:
            file.write(self.buffer)
        print("File saved.")

    def edit_content(self):
        while True : 
            os.system('clear' if os.name == 'posix' else 'cls')  # Clear the screen (Linux/Windows)
            print("Simple Text Editor")
            print("File: {}".format(self.file_path))
            print("\n" + self.buffer)
            print(self.buffer[:self.cursor_pos] + '|' + self.buffer[self.cursor_pos:])
            print("\nCommands: (q)uit, (w)rite, (e)dit > ")
            print("Select where you want to edit before typing ^^")
            key = self.get_keypress()
            if key == 'q':
                break
            elif key == 's':
                self.save_file()
                input("Press Enter to continue...")
                break
            elif key == 'e':
                new_content = input("Enter new content:\n")
                self.buffer = self.buffer[:self.cursor_pos] + new_content + self.buffer[self.cursor_pos:]
            elif key == 'right':
                self.move_cursor(1)
            elif key == 'left':
                self.move_cursor(-1)

    def get_keypress(self):
        if os.name == 'posix':

            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)

            try:
                tty.setcbreak(sys.stdin.fileno())
                key = sys.stdin.read(1)
                if key == '\x1b':
                    key += sys.stdin.read(2)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

            if key == '\x1b[A':
                return 'up'
            elif key == '\x1b[B':
                return 'down'
            elif key == '\x1b[C':
                return 'right'
            elif key == '\x1b[D':
                return 'left'
            elif key == '\x1b':
                return 'esc'
            elif key == '\r':
                return 'enter'
            elif key == '\x03':
                return 'q'  # Ctrl+C
            else:
                return key
 
    def move_cursor(self, offset):
        self.cursor_pos = max(0, min(self.cursor_pos + offset, len(self.buffer)))


    
def main():
    editor = TextEditor()
    if len(sys.argv) == 2:
       file_path = sys.argv[1]
       print(file_path)
       editor.load_file(file_path)
    while editor.edit_content():
        pass

if __name__ == "__main__":
    main()
