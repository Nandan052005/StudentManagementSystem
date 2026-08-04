"""
Quick smoke test for the Student Record Management System.
Validates that all modules load correctly and core logic works.
"""

import sys
sys.path.insert(0, ".")

from file_handler import load_students, save_students
from student_manager import (
    generate_student_id,
    validate_name,
    validate_age,
    validate_email,
    validate_phone,
    validate_gender,
    validate_year,
    validate_department,
)


def run_tests():
    passed = 0
    failed = 0

    def check(description, result):
        nonlocal passed, failed
        if result:
            passed += 1
            print(f"  [PASS] {description}")
        else:
            failed += 1
            print(f"  [FAIL] {description}")

    # --- File Handler ---
    students = load_students()
    check("load_students returns a list", isinstance(students, list))
    check("Sample data has 5 records", len(students) == 5)

    # --- ID Generation ---
    check("Next ID is STU-0006", generate_student_id(students) == "STU-0006")
    check("Empty list yields STU-0001", generate_student_id([]) == "STU-0001")

    # --- Validation: Name ---
    check("Valid name 'John Doe'", validate_name("John Doe")[0] is True)
    check("Short name 'A' rejected", validate_name("A")[0] is False)
    check("Numeric name rejected", validate_name("John123")[0] is False)

    # --- Validation: Age ---
    check("Age 20 accepted", validate_age("20")[0] is True)
    check("Age 5 rejected (too young)", validate_age("5")[0] is False)
    check("Age 'abc' rejected", validate_age("abc")[0] is False)

    # --- Validation: Gender ---
    check("Gender 'Male' accepted", validate_gender("Male")[0] is True)
    check("Gender 'female' accepted", validate_gender("female")[0] is True)
    check("Gender 'xyz' rejected", validate_gender("xyz")[0] is False)

    # --- Validation: Department ---
    check("Dept 'Computer Science' accepted", validate_department("Computer Science")[0] is True)
    check("Dept 'X' rejected (too short)", validate_department("X")[0] is False)

    # --- Validation: Year ---
    check("Year 3 accepted", validate_year("3")[0] is True)
    check("Year 9 rejected", validate_year("9")[0] is False)

    # --- Validation: Email ---
    check("Email 'a@b.com' accepted", validate_email("a@b.com")[0] is True)
    check("Email 'invalid' rejected", validate_email("invalid")[0] is False)

    # --- Validation: Phone ---
    check("Phone '+919876543210' accepted", validate_phone("+919876543210")[0] is True)
    check("Phone '123' rejected (too short)", validate_phone("123")[0] is False)

    # --- Summary ---
    total = passed + failed
    print(f"\n  {'=' * 40}")
    print(f"  Results: {passed}/{total} passed, {failed} failed")
    if failed == 0:
        print("  All tests passed! [OK]")
    print(f"  {'=' * 40}")

    return failed


if __name__ == "__main__":
    print("\n  Student Record System — Smoke Tests\n")
    failures = run_tests()
    sys.exit(1 if failures else 0)
