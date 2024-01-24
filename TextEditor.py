import os
from Rope import Rope

rope_editor = Rope("Hello, World!")

if __name__ == "__main__":
    os.system('clear' if os.name == 'posix' else 'cls')
    while True:
        print("\nCurrent text:")
        print(rope_editor.collectleaves())
        print("\nCommands:")
        print("1. Insert")
        print("2. Delete")
        print("3. Concat")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            index = int(input("Enter the index to insert at: "))
            text_to_insert = input("Enter the text to insert: ")
            rope_editor.insert(index, text_to_insert)
        elif choice == "2":
            start = int(input("Enter starting deletion index: "))
            length = int(input("Enter deletion length"))
            rope_editor.delete(start,length)
        elif choice == "3":
            data = input("Enter the string to concat: ")
            rope_editor.concatRope(Rope(data))
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")