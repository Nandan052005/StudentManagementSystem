
import json
import os


DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "students.json")


def load_students(filepath=DATA_FILE):
    if not os.path.exists(filepath):
        _create_empty_file(filepath)
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

            
            if not isinstance(data, list):
                print("\n  [!] Warning: Data file format is invalid. Starting with empty records.")
                return []

            return data

    except json.JSONDecodeError:
        print("\n  [!] Error: The data file contains invalid JSON.")
        print("      A backup has been created and records have been reset.")
        _backup_corrupt_file(filepath)
        return []

    except PermissionError:
        print(f"\n  [!] Error: Permission denied when reading '{filepath}'.")
        return []

    except OSError as error:
        print(f"\n  [!] Error reading file: {error}")
        return []


def save_students(students, filepath=DATA_FILE):
    
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=4, ensure_ascii=False)
        return True

    except PermissionError:
        print(f"\n  [!] Error: Permission denied when writing to '{filepath}'.")
        return False

    except OSError as error:
        print(f"\n  [!] Error writing file: {error}")
        return False


def _create_empty_file(filepath):
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)
    except OSError as error:
        print(f"\n  [!] Error creating data file: {error}")


def _backup_corrupt_file(filepath):
    
    backup_path = filepath + ".bak"
    try:
        os.rename(filepath, backup_path)
        _create_empty_file(filepath)
    except OSError as error:
        print(f"\n  [!] Error creating backup: {error}")
