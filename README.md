# Student Record Management System

A command-line Python application to manage student records. It stores all data in a JSON file and doesn't need any external libraries - just standard Python.

## Features

- Add, view, search, update, and delete student records
- Auto-generates unique Student IDs (STU-0001, STU-0002, ...)
- Validates all user input (email, phone, age, etc.)
- Data is saved to `students.json` and persists between sessions
- The JSON file is created automatically if it doesn't exist
- Handles errors like missing files or bad data gracefully

## Tech Stack

- Python 3.10+
- Standard library only (`json`, `os`, `re`, `sys`)

## Project Structure

```
StudentManagementSystem/
├── main.py               # entry point, handles the menu loop
├── student_manager.py    # all the logic - CRUD, validation, display
├── file_handler.py       # reading/writing the JSON file
├── students.json         # where records are stored
├── requirements.txt      # no external deps needed
├── .gitignore
└── README.md
```

## How to Run

Make sure you have Python 3.10 or newer installed, then:

```bash
git clone https://github.com/your-username/StudentManagementSystem.git
cd StudentManagementSystem
python main.py
```

That's it. No packages to install.

## Student Fields

| Field | Validation |
|-------|-----------|
| Student ID | Auto-generated, can't be changed |
| Name | Letters, spaces, hyphens (2-100 chars) |
| Age | 16-60 |
| Gender | Male / Female / Other |
| Department | 2-100 characters |
| Year of Study | 1-6 |
| Email | Standard email format |
| Phone | 7-15 digits, optional + prefix |

## Sample Output

```
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
```

## Ideas for Future Work

- Add password protection
- Export data to CSV
- Switch to SQLite for larger datasets
- Build a web interface with Flask
- Add search by name or department
- Unit tests

## License

MIT
