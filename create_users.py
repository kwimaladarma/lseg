import csv
import requests
import re
from datetime import datetime

LOG_FILE = "runlogs.log"
CSV_FILE = "users.csv"
API_URL = "https://example.com/api/create_user"

REQUIRED_FIELDS = ["name", "email", "role"]
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

# Add timestamp to logs
def log_message(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    full_message = f"{timestamp} {message}"
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(full_message + '\n')
    print(full_message)

# Validate required fields and email format
def is_valid_user(row):
    missing = [field for field in REQUIRED_FIELDS if not row.get(field)]
    if missing:
        log_message(f"Skipped row due to missing fields ({', '.join(missing)}): {row}")
        return False

    email = row.get("email", "")
    if not re.match(EMAIL_REGEX, email):
        log_message(f"Skipped row due to invalid email format: {email}")
        return False

    return True

# Create user via API
def create_user(user_data):
    try:
        response = requests.post(API_URL, json=user_data)
        if response.status_code == 201:
            return True
        else:
            log_message(f"Failed to create user {user_data.get('email')}: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        log_message(f"Exception creating user {user_data.get('email')}: {str(e)}")
        return False

# Process CSV
def create_users(file_path):
    total = 0
    success = 0
    failed = 0

    log_message("********** User creation process started. **********")

    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            if not is_valid_user(row):
                failed += 1
                continue
            if create_user(row):
                success += 1
            else:
                failed += 1

    log_message("********** User creation process finished. **********")
    log_message(f"Total users attempted: {total}")
    log_message(f"Users created successfully: {success}")
    log_message(f"Users failed: {failed}")

if __name__ == "__main__":
    create_users(CSV_FILE)
