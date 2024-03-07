import curses
from Rope import Rope
class TextEditor:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.top_content = "Top Content"
        self.bottom_content = "^Q. Exit"
        self.text_editor = Rope("\nHello World\nJ'ai dit tout va bien\nquoicoucou\naaaa")
        self.cursor_x = 0
        self.cursor_y = 0
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
    
    
    def handleDown(self):
        text = self.text_editor.collectleaves()
        find = text.find("\n",self.cursor_position+1,len(text))
        find2 = text.find("\n",find+1,len(text))
        if(self.cursor_y+1 == text.count("\n") and self.cursor_position < len(text)-1):
            self.cursor_x += (len(text)-1-self.cursor_position)
            self.cursor_position += (len(text)-1-self.cursor_position)
        else : 
            if find2 == -1 :
                if len(text)- find < self.cursor_x+1 :
                    self.cursor_x = (len(text) -find)-1
            elif find2-find < self.cursor_x+1:
                self.cursor_x = (find2 -find)-1
            self.cursor_position += find - self.cursor_position
            self.cursor_position += self.cursor_x
            self.cursor_y += 1

    def handleUp(self):
        text = self.text_editor.collectleaves()
        find = text.rfind("\n",0,self.cursor_position+1)
        find2 = text.rfind("\n",0,find-1)
        if self.cursor_y == 1 and self.text_editor.index(self.cursor_position) == "\n" :
            self.cursor_position = 0
            self.cursor_y -= 1
        else :
            if find-find2 < self.cursor_x+1:
                self.cursor_x = (find -find2)-1
            self.cursor_position = find2
            self.cursor_position += self.cursor_x
            self.cursor_y -= 1
                
    def handleRight(self):
        if self.text_editor.index(self.cursor_position+1) == "\n" and self.cursor_position != 0:
            self.cursor_y +=1
            self.cursor_x = 0
            self.cursor_position+=1
        else:
            self.cursor_position+=1
            self.cursor_x +=1

    def handleLeft(self):
        text = self.text_editor.collectleaves()
        find = text.rfind("\n",0,self.cursor_position+1)
        find2 = text.rfind("\n",0,find-1)
        if self.cursor_position >0:
            if self.cursor_position == find and self.cursor_position != 1:
                self.cursor_position -=1
                self.cursor_y -= 1
                self.cursor_x = (find - find2)-1
            else: 
                self.cursor_x -= 1
                self.cursor_position -=1

    def handle_cursor_movement(self,key):
        text = self.text_editor.collectleaves()
        if key == curses.KEY_DOWN and self.cursor_position < len(text)-1:
            self.handleDown()
        elif key == curses.KEY_UP and self.cursor_y > 0:
            self.handleUp()
        elif key == curses.KEY_RIGHT and self.cursor_position < len(text)-1:
            self.handleRight()
        elif key == curses.KEY_LEFT:
            self.handleLeft()

    def run(self):
        self.stdscr.nodelay(True)
        while True:
            self.display_top_content()
            self.display_main_content()
            self.display_bottom_content()
            self.display_cursor()
            key = self.stdscr.getch()
            self.handle_cursor_movement(key)
            if key == 17:
                break    

if __name__ == "__main__":
    curses.wrapper(TextEditor)