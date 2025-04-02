# User Creation from CSV with Validation, Logging, and Retry Logic

This Python script reads a list of users from a CSV file and attempts to create them via an API. It performs various validations, handles API failures with retry logic, and generates comprehensive logs for both successes and errors.

---

## Features

- Read users from a CSV file (`users.csv`)
- Validation includes:
  - Required fields: `name`, `email`, `role`
  - Proper **email format**
  - Valid **role** (`admin`, `user`, `moderator`)
  - Proper **name format** (letters, spaces, hyphens, apostrophes only)
  - Duplicate email check within the CSV
  - Skips **empty lines**
- Normalizes fields (trims spaces, lowercases roles)
- Retries API requests up to 3 times if they fail
- Logs:
  - Start and end of the process
  - Skipped rows with reasons (and row numbers)
  - API failures with retry attempts
  - Successfully created users in a separate file
- Supports UTF-8 CSV files

---

## File Structure

```bash
.
├── user_create.py          # Main script
├── users.csv               # Input file with user data
├── runlogs.log             # Error and process logs
├── created_users.log       # Successfully created users
├── README.md               # This documentation
```
---
## Future improvements

- Can deploy this on Azure or AWS in a containerized environment and run this as a scheduler using a tool like microsoft power automate or logic app
- Can check if the user already exist using API's on the system before creating the user
- Can have parallel processing using threading for large scale csv's
- Failed users/rows can be exported to a different csv for re-processing later after reviewing
- Can extract the email from the csv and add power automate or logic app email action to notify the user telling that their user has been created.
