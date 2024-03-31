import curses
import curses.ascii
from Rope import Rope
class TextEditor:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.top_content = "Top Content\n"
        self.bottom_content = "^Q. Exit"
        self.text_editor = Rope("Bonjour\n")
        self.cursor_x = 0
        self.cursor_y = 0
        self.cursor_position = 0
        self.scroll_pos = 0
        self.run()
        
    def display_top_content(self):
        self.stdscr.addstr(0, 0, self.top_content)

    def display_bottom_content(self):
        _, cols = self.stdscr.getmaxyx()
        self.stdscr.addstr(curses.LINES - 1, 0, self.bottom_content.ljust(cols - 1))

    def display_main_content(self):
        self.stdscr.addstr(self.text_editor.report())

    def display_cursor(self):
        self.stdscr.move(self.cursor_y+1, self.cursor_x)
     
    def handleDown(self):
        text = self.text_editor.report()
        lines = text.split('\n')
        if self.cursor_y + 1 < len(lines):
            self.cursor_y += 1
            next_line_length = len(lines[self.cursor_y])
            # Adjust cursor_x to not exceed the next line's length, subtracting 1 to convert count to index
            self.cursor_x = min(self.cursor_x, next_line_length - 1 if next_line_length > 0 else 0)
            # Update cursor_position based on the new cursor_y and cursor_x
            self.cursor_position = sum(len(line) + 1 for line in lines[:self.cursor_y]) + self.cursor_x

    def handleUp(self):
        if self.cursor_y > 0:
            text = self.text_editor.report()
            lines = text.split('\n')
            self.cursor_y -= 1
            prev_line_length = len(lines[self.cursor_y])
            # Adjust cursor_x to not exceed the previous line's length, subtracting 1 to convert count to index
            self.cursor_x = min(self.cursor_x, prev_line_length - 1 if prev_line_length > 0 else 0)
            # Update cursor_position based on the new cursor_y and cursor_x
            self.cursor_position = sum(len(line) + 1 for line in lines[:self.cursor_y]) + self.cursor_x
                
    def handleRight(self):
        if self.text_editor.get_character_at_index(self.cursor_position) == "\n" and self.cursor_position != 0:
            self.cursor_y +=1
            self.cursor_x = 0
            self.cursor_position +=1
        else:
            self.cursor_position += 1
            self.cursor_x += 1
  
    def handleLeft(self,isNewline=False):
        text =self.text_editor.report()
        if isNewline:
            res = text.rfind("\n",0,self.cursor_position-1)
            self.cursor_x = len(text[res+1:self.cursor_position-1])
            self.cursor_position -=1
            self.cursor_y -= 1
        else:
            self.cursor_x -= 1
            self.cursor_position -=1

    def handleEnter(self):
        self.insert_character("\n")
    
    def insert_character(self,char):
        _, max_x = self.stdscr.getmaxyx()
        if self.cursor_x  == max_x - 1:
            if self.text_editor.get_character_at_index(self.cursor_position) != "\n":
                self.text_editor.insert(self.cursor_position,"\n")
            self.handleRight()
        self.text_editor.insert(self.cursor_position,char)
        self.handleRight()
    
    def delete_character(self):
        char_to_delete = self.text_editor.get_character_at_index(self.cursor_position - 1)
        # Delete the character before the cursor in the rope
        self.text_editor.delete(self.cursor_position - 1, 1)
        self.handleLeft()  # Move cursor left to reflect deletion

        # Additional handling if deleting a newline character
        if char_to_delete == "\n":
            # Adjust cursor_x and cursor_y if we've deleted a newline character
            self.cursor_y -= 1
            # Find the new cursor_x position at the end of the now-extended line
            line_start = self.text_editor.report().rfind("\n", 0, self.cursor_position - 1)
            self.cursor_x = (self.cursor_position - line_start - 1) if line_start != -1 else self.cursor_position

    def handle_movement(self,key):
        text =self.text_editor.report()
        if key == curses.KEY_DOWN and self.cursor_position < len(text)-1:
            self.handleDown()
        elif key == curses.KEY_UP and self.cursor_y > 0:
            self.handleUp()
        elif key == curses.KEY_RIGHT and self.cursor_position < len(text):
            self.handleRight()
        elif key == curses.KEY_LEFT and self.cursor_position > 0:
            if self.text_editor.get_character_at_index(self.cursor_position - 1) == "\n": self.handleLeft(True)
            else: self.handleLeft()
        elif (key == curses.KEY_ENTER or key == ord('\n') or key == ord('\r')) and self.cursor_position > 0:
            self.handleEnter()
        elif key == curses.KEY_BACKSPACE and self.cursor_position > 0:
            self.delete_character()
        elif curses.ascii.isprint(key):
            self.insert_character(chr(key))

    def run(self):
        self.stdscr.nodelay(True)
        while True:
            self.stdscr.erase()
            self.display_top_content()
            self.display_main_content()
            self.display_bottom_content()
            self.display_cursor()
            self.stdscr.refresh()
            key = self.stdscr.getch()
            self.handle_movement(key)
            
            if key == 17:
                break

if __name__ == "__main__":
    curses.wrapper(TextEditor)