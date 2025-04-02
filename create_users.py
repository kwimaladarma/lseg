import csv
import requests
import re
import time
from datetime import datetime

LOG_FILE = "runlogs.log"
SUCCESS_LOG_FILE = "created_users.log"
CSV_FILE = "users.csv"
API_URL = "https://example.com/api/create_user"

REQUIRED_FIELDS = ["name", "email", "role"]
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"
NAME_REGEX = r"^[a-zA-Z\s'-]+$"
VALID_ROLES = {"admin", "user", "moderator"}

# Timestamped log
def log_message(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    full_message = f"{timestamp} {message}"
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(full_message + '\n')
    print(full_message)

# Success log
def log_success(row_num, email):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(SUCCESS_LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] Row {row_num}: User created successfully: {email}\n")

# Validation
def is_valid_user(row, row_num):
    missing = [field for field in REQUIRED_FIELDS if not row.get(field)]
    if missing:
        log_message(f"Row {row_num}: Skipped due to missing fields ({', '.join(missing)}): {row}")
        return False

    name = row.get("name", "").strip()
    if not re.match(NAME_REGEX, name):
        log_message(f"Row {row_num}: Skipped due to invalid name format: '{name}'")
        return False

    email = row.get("email", "").strip()
    if not re.match(EMAIL_REGEX, email):
        log_message(f"Row {row_num}: Skipped due to invalid email format: {email}")
        return False

    role = row.get("role", "").strip().lower()
    if role not in VALID_ROLES:
        log_message(f"Row {row_num}: Skipped due to invalid role '{role}'. Must be one of {', '.join(VALID_ROLES)}")
        return False

    # Normalize cleaned values back to row
    row["name"] = name
    row["email"] = email
    row["role"] = role

    return True

# Create user with retry logic
def create_user(user_data, row_num, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(API_URL, json=user_data)
            if response.status_code == 201:
                log_success(row_num, user_data.get("email"))
                return True
            else:
                log_message(f"Row {row_num}: Attempt {attempt}: Failed to create user {user_data.get('email')}: HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            log_message(f"Row {row_num}: Attempt {attempt}: Exception creating user {user_data.get('email')}: {str(e)}")

        if attempt < max_retries:
            time.sleep(2)  # wait before retrying

    return False

# Main CSV processing
def create_users(file_path):
    total = 0
    success = 0
    failed = 0
    seen_emails = set()

    log_message("********** User creation process started. **********")

    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):  # CSV line numbers
            # Check for empty line (all values empty or just whitespace)
            if all(not str(value).strip() for value in row.values()):
                log_message(f"Row {row_num}: Skipped empty line.")
                continue

            total += 1
            email = row.get("email", "").strip()
            if email in seen_emails:
                log_message(f"Row {row_num}: Skipped due to duplicate email in CSV: {email}")
                failed += 1
                continue

            if not is_valid_user(row, row_num):
                failed += 1
                continue

            seen_emails.add(email)

            if create_user(row, row_num):
                success += 1
            else:
                failed += 1

    log_message("********** User creation process finished. **********")
    log_message(f"Total users attempted: {total}")
    log_message(f"Users created successfully: {success}")
    log_message(f"Users failed: {failed}")

if __name__ == "__main__":
    create_users(CSV_FILE)
