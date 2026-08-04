import re
from file_handler import load_students, save_students


def generate_student_id(students):
    if not students:
        return "STU-0001"

    max_num = 0
    for s in students:
        sid = s.get("student_id", "STU-0000")
        try:
            num = int(sid.split("-")[1])
            if num > max_num:
                max_num = num
        except (IndexError, ValueError):
            continue

    return f"STU-{max_num + 1:04d}"


# --- validation functions ---

def validate_name(name):
    name = name.strip()
    if len(name) < 2:
        return False, "Name must be at least 2 characters."
    if len(name) > 100:
        return False, "Name is too long (max 100 characters)."
    if not re.match(r"^[A-Za-z\s\-']+$", name):
        return False, "Name should only have letters, spaces, hyphens or apostrophes."
    return True, ""


def validate_age(age_str):
    try:
        age = int(age_str)
    except ValueError:
        return False, "Enter a valid number for age."
    if age < 16 or age > 60:
        return False, "Age should be between 16 and 60."
    return True, ""


def validate_gender(gender):
    valid = {"male", "female", "other"}
    if gender.strip().lower() not in valid:
        return False, "Enter Male, Female, or Other."
    return True, ""


def validate_department(dept):
    dept = dept.strip()
    if len(dept) < 2:
        return False, "Department name is too short."
    if len(dept) > 100:
        return False, "Department name is too long."
    return True, ""


def validate_year(year_str):
    try:
        year = int(year_str)
    except ValueError:
        return False, "Enter a valid number."
    if year < 1 or year > 6:
        return False, "Year should be between 1 and 6."
    return True, ""


def validate_email(email):
    email = email.strip()
    pattern = r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$"
    if not re.match(pattern, email):
        return False, "That doesn't look like a valid email."
    return True, ""


def validate_phone(phone):
    phone = phone.strip()
    if not re.match(r"^\+?[0-9]{7,15}$", phone):
        return False, "Phone should be 7-15 digits (can start with +)."
    return True, ""


# --- helper to keep asking until input is valid ---

def get_validated_input(prompt, validator_func):
    while True:
        value = input(prompt).strip()
        valid, msg = validator_func(value)
        if valid:
            return value
        print(f"  >> {msg}")


def collect_student_details():
    print("\n  Fill in the student details:\n")

    name = get_validated_input("  Name           : ", validate_name)
    age = get_validated_input("  Age            : ", validate_age)
    gender = get_validated_input("  Gender (M/F/O) : ", validate_gender)
    dept = get_validated_input("  Department     : ", validate_department)
    year = get_validated_input("  Year of Study  : ", validate_year)
    email = get_validated_input("  Email          : ", validate_email)
    phone = get_validated_input("  Phone Number   : ", validate_phone)

    # normalize gender
    gender_map = {
        "m": "Male", "male": "Male",
        "f": "Female", "female": "Female",
        "o": "Other", "other": "Other"
    }
    gender = gender_map.get(gender.lower(), gender.title())

    return {
        "name": name.title(),
        "age": int(age),
        "gender": gender,
        "department": dept.title(),
        "year_of_study": int(year),
        "email": email.lower(),
        "phone": phone
    }


# --- CRUD functions ---

def add_student():
    students = load_students()
    details = collect_student_details()
    new_id = generate_student_id(students)

    record = {"student_id": new_id, **details}
    students.append(record)

    if save_students(students):
        print(f"\n  Student added successfully! ID: {new_id}")
    else:
        print("\n  Failed to save the record.")


def view_all_students():
    students = load_students()

    if not students:
        print("\n  No records found. Try adding a student first.")
        return

    col_widths = {
        "id": 10, "name": 22, "age": 5, "gender": 8,
        "dept": 20, "year": 6, "email": 28, "phone": 16
    }

    w = col_widths
    line = ("  +-" + "-" * w["id"] + "-+-" + "-" * w["name"] + "-+-" +
            "-" * w["age"] + "-+-" + "-" * w["gender"] + "-+-" +
            "-" * w["dept"] + "-+-" + "-" * w["year"] + "-+-" +
            "-" * w["email"] + "-+-" + "-" * w["phone"] + "-+")

    header = (f"  | {'ID':<{w['id']}} | {'Name':<{w['name']}} | "
              f"{'Age':<{w['age']}} | {'Gender':<{w['gender']}} | "
              f"{'Department':<{w['dept']}} | {'Year':<{w['year']}} | "
              f"{'Email':<{w['email']}} | {'Phone':<{w['phone']}} |")

    print(f"\n  --- All Students ({len(students)} records) ---\n")
    print(line)
    print(header)
    print(line)

    for s in students:
        row = (f"  | {s.get('student_id', '-'):<{w['id']}} | "
               f"{s.get('name', '-'):<{w['name']}} | "
               f"{str(s.get('age', '-')):<{w['age']}} | "
               f"{s.get('gender', '-'):<{w['gender']}} | "
               f"{s.get('department', '-'):<{w['dept']}} | "
               f"{str(s.get('year_of_study', '-')):<{w['year']}} | "
               f"{s.get('email', '-'):<{w['email']}} | "
               f"{s.get('phone', '-'):<{w['phone']}} |")
        print(row)

    print(line)
    print(f"\n  Total: {len(students)} record(s)")


def search_student():
    students = load_students()

    if not students:
        print("\n  No records to search.")
        return

    sid = input("\n  Enter Student ID (e.g. STU-0001): ").strip().upper()
    if not sid:
        print("  ID can't be empty.")
        return

    result = None
    for s in students:
        if s.get("student_id", "").upper() == sid:
            result = s
            break

    if result:
        show_student_details(result)
    else:
        print(f"\n  No student found with ID '{sid}'.")


def update_student():
    students = load_students()

    if not students:
        print("\n  No records to update.")
        return

    sid = input("\n  Enter Student ID to update: ").strip().upper()

    idx = None
    for i, s in enumerate(students):
        if s.get("student_id", "").upper() == sid:
            idx = i
            break

    if idx is None:
        print(f"\n  Student '{sid}' not found.")
        return

    show_student_details(students[idx])

    fields = {
        "1": ("name",          "Name",          validate_name),
        "2": ("age",           "Age",           validate_age),
        "3": ("gender",        "Gender",        validate_gender),
        "4": ("department",    "Department",    validate_department),
        "5": ("year_of_study", "Year of Study", validate_year),
        "6": ("email",         "Email",         validate_email),
        "7": ("phone",         "Phone Number",  validate_phone),
    }

    print("\n  What do you want to update?\n")
    for k, (_, label, _) in fields.items():
        print(f"    {k}. {label}")
    print("    0. Cancel")

    pick = input("\n  Choice: ").strip()

    if pick == "0" or pick not in fields:
        print("  Update cancelled.")
        return

    key, label, validator = fields[pick]
    new_val = get_validated_input(f"\n  New {label}: ", validator)

    # type conversions
    if key == "age":
        new_val = int(new_val)
    elif key == "year_of_study":
        new_val = int(new_val)
    elif key == "gender":
        gmap = {"m": "Male", "male": "Male", "f": "Female",
                "female": "Female", "o": "Other", "other": "Other"}
        new_val = gmap.get(new_val.lower(), new_val.title())
    elif key in ("name", "department"):
        new_val = new_val.title()
    elif key == "email":
        new_val = new_val.lower()

    old_val = students[idx].get(key, "N/A")
    students[idx][key] = new_val

    if save_students(students):
        print(f"\n  Updated {label}: '{old_val}' -> '{new_val}'")
    else:
        print("\n  Could not save the update.")


def delete_student():
    students = load_students()

    if not students:
        print("\n  Nothing to delete.")
        return

    sid = input("\n  Enter Student ID to delete: ").strip().upper()

    idx = None
    for i, s in enumerate(students):
        if s.get("student_id", "").upper() == sid:
            idx = i
            break

    if idx is None:
        print(f"\n  Student '{sid}' not found.")
        return

    show_student_details(students[idx])

    confirm = input("\n  Are you sure? (yes/no): ").strip().lower()

    if confirm in ("yes", "y"):
        removed = students.pop(idx)
        if save_students(students):
            print(f"\n  Deleted '{removed['name']}' ({sid}).")
        else:
            print("\n  Error saving after deletion.")
    else:
        print("  Cancelled.")


def show_student_details(student):
    print("\n  +------------------------------------------------+")
    print("  |            Student Details                      |")
    print("  +------------------------------------------------+")
    print(f"  |  Student ID    :  {student.get('student_id', '-'):<28}|")
    print(f"  |  Name          :  {student.get('name', '-'):<28}|")
    print(f"  |  Age           :  {str(student.get('age', '-')):<28}|")
    print(f"  |  Gender        :  {student.get('gender', '-'):<28}|")
    print(f"  |  Department    :  {student.get('department', '-'):<28}|")
    print(f"  |  Year of Study :  {str(student.get('year_of_study', '-')):<28}|")
    print(f"  |  Email         :  {student.get('email', '-'):<28}|")
    print(f"  |  Phone         :  {student.get('phone', '-'):<28}|")
    print("  +------------------------------------------------+")
