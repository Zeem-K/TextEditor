import curses
from Rope import Rope
class TextEditor:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.top_content = "Top Content"
        self.bottom_content = "^Q. Exit"
        self.text_editor = Rope("\nHello World\nJ'ai dit tout va bien\nbonjour boujourno")
        self.cursor_x = 0
        self.cursor_y = 0
        self.lastnewline_coord = [0,0]
        self.cursor_position = 0
        self.run()
        
    def display_top_content(self):
        self.stdscr.addstr(0, 0, self.top_content)

    def display_bottom_content(self):
        _, cols = self.stdscr.getmaxyx()
        self.stdscr.addstr(curses.LINES - 1, 0, self.bottom_content.ljust(cols - 1))

    def display_main_content(self):
        self.stdscr.addstr(self.text_editor.collectleaves())

    def display_cursor(self):
        self.stdscr.move(self.cursor_y+1, self.cursor_x)
    
    def isSameLastnewLineCoord(self):
        return self.cursor_x == self.lastnewline_coord[0] and self.cursor_y == self.lastnewline_coord[1]

    def updateLastNewLineCoord(self,x,y):
        self.lastnewline_coord[0] = x
        self.lastnewline_coord[1] = y

    def handle_cursor_movement(self,key):
        text = self.text_editor.collectleaves()
        if key == curses.KEY_DOWN:
            self.cursor_y += 1
            find = text.find("\n",self.cursor_position,len(text))
            self.cursor_position += find

        elif key == curses.KEY_UP and self.cursor_y > 0:
            self.cursor_position -= self.cursor_x+1
            self.cursor_position = text.rfind("\n",0,self.cursor_position)
            self.cursor_position += self.cursor_x
            self.cursor_y -= 1
        elif key == curses.KEY_RIGHT and self.cursor_position < len(text)+1:
            if self.text_editor.index(self.cursor_position+1) == "\n" and self.cursor_position != 0:
                self.cursor_y +=1
                self.cursor_x = 0
                self.cursor_position+=1
            else:
                self.cursor_position+=1
                self.cursor_x +=1
        elif key == curses.KEY_LEFT and self.cursor_x > 0:
            if self.text_editor.index(self.cursor_position+1) == "\n" and self.cursor_position != 0:
                self.cursor_position -=1
                self.cursor_y -= 1
                num = text.rfind("\n",0,self.cursor_position)
                self.cursor_x = len(text[num:self.cursor_position+1])
            else: 
                self.cursor_x -= 1
                self.cursor_position -=1

    def run(self):
        while True:
            self.display_top_content()
            self.display_main_content()
            self.display_bottom_content()
            self.display_cursor()

            key = self.stdscr.getch()
            self.handle_cursor_movement(key)
            self.stdscr.refresh()
            if key == ord('q'):
                break
                
                


if __name__ == "__main__":
    curses.wrapper(TextEditor)