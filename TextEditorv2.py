import curses
from Rope import Rope
from curses import wrapper

class TextEditor:
    def __init__(self, stdscr):
        self.rope_editor = Rope("Hello, World!")
        self.stdscr = stdscr
        self.cursor_x = 0
        self.cursor_y = 0
        self.commands = ["1. Insert", "2. Exit"]
        self.command_index = 0
        self.run()

    def insert_text(self, index, text):
        self.rope_editor.insert(index, text)

    def display_text(self):
        self.stdscr.clear()
        text_to_display = self.rope_editor.collectleaves()
        self.stdscr.addstr(0, 0, text_to_display)

    def display_commands(self):
        for i, command in enumerate(self.commands):
            self.stdscr.addstr(curses.LINES-1-i, 0, command)

    def run(self):
        while True:
            self.stdscr.clear()

            self.display_text()
            self.display_commands()

            self.stdscr.move(self.cursor_y, self.cursor_x)

            key = self.stdscr.getch()

            if key == curses.KEY_DOWN and self.command_index < len(self.commands) - 1:
                self.command_index += 1
            elif key == curses.KEY_UP and self.command_index > 0:
                self.command_index -= 1
            elif key == curses.KEY_ENTER or key == 10 or key == 13:
                if self.command_index == 0:
                    index = int(self.stdscr.getstr().decode())
                    text_to_insert = self.stdscr.getstr().decode()
                    self.insert_text(index, text_to_insert)
                elif self.command_index == 1:
                    break

if __name__ == "__main__":
    wrapper(TextEditor)
