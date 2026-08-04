import sys
from student_manager import (
    add_student,
    view_all_students,
    search_student,
    update_student,
    delete_student,
)

BANNER = """
  ====================================================
  |     Student Record Management System  v1.0       |
  |     A simple CLI tool to manage student data     |
  ====================================================
"""

MENU = """
  +------------------------------------------+
  |              MAIN MENU                   |
  +------------------------------------------+
  |                                          |
  |   1. Add New Student                     |
  |   2. View All Students                   |
  |   3. Search Student by ID                |
  |   4. Update Student Details              |
  |   5. Delete Student Record               |
  |   0. Exit                                |
  |                                          |
  +------------------------------------------+
"""

MENU_ACTIONS = {
    "1": add_student,
    "2": view_all_students,
    "3": search_student,
    "4": update_student,
    "5": delete_student,
}


def show_menu():
    print(MENU)


def main():
    print(BANNER)

    while True:
        show_menu()
        choice = input("  Enter your choice [0-5]: ").strip()

        if choice == "0":
            print("\n  Thank you for using the system. Goodbye!\n")
            sys.exit(0)

        action = MENU_ACTIONS.get(choice)

        if action:
            action()
        else:
            print("\n  Invalid option. Pick a number from 0 to 5.")

        input("\n  Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Program interrupted. Exiting...\n")
        sys.exit(0)
