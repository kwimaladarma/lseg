import csv
import requests
from datetime import datetime

LOG_FILE = "runlogs.log"
CSV_FILE = "users.csv"
API_URL = "https://example.com/api/create_user"

REQUIRED_FIELDS = ["name", "email", "role"]



#add time stamp to err log
def log_error(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    full_message = f"{timestamp} {message}"
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(full_message + '\n')
    print(full_message)  # Print to console

#validate users by checking if all the feilds are available
def is_valid_user(row):
    missing = [field for field in REQUIRED_FIELDS if not row.get(field)]
    if missing:
        log_error(f"Skipped row due to missing fields ({', '.join(missing)}): {row}")
        return False
    return True

#create user
def create_user(user_data):
    try:
        response = requests.post(API_URL, json=user_data)
        if response.status_code != 201:
            log_error(f"Failed to create user {user_data.get('email')}: HTTP {response.status_code}")
    except requests.exceptions.RequestException as e:
        log_error(f"Exception creating user {user_data.get('email')}: {str(e)}")

#read users from csv and create valid users
def create_users(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not is_valid_user(row):
                continue
            create_user(row)

if __name__ == "__main__":
    create_users(CSV_FILE)
