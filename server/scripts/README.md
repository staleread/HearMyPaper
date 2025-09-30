# Server Scripts

This directory contains utility scripts for server administration.

## create_admin_user.py

Interactive script to generate a SQL INSERT statement for creating an admin
user with custom access levels and writes encrypted
credentials to a binary file compatible with the client application.

### Usage

```bash
cd /home/mykola/edu/chnu/python-web/HearMyPaper/server
source .venv/bin/activate
python scripts/create_admin_user.py
```

### What it does

1. **Prompts for user information:**
   - User ID (integer) - manually set for the admin user
   - First Name
   - Last Name
   - Email address
   - Account expiry date (ISO format)
   - Confidentiality level (1-4)
   - Integrity levels (comma-separated list)
   - Credentials file path
   - Password for credentials file

2. **Generates Ed25519 key pair:**
   - Creates a new cryptographic key pair
   - Uses the same algorithm as the client application

3. **Saves encrypted credentials:**
   - Stores user ID and private key in encrypted binary file
   - Uses same encryption format as client's `credentials_repo.py`
   - PBKDF2 + AES-256-GCM encryption with secure random salt/IV

4. **Outputs:**
   - SQL statements to create the admin user
   - Sequence update using `setval()` for manual ID setting
   - Credentials file path for client authentication
   - Raw keys for reference

### Security Notes

- **Credentials file is encrypted** with the password you provide
- **Use the credentials file with the client** to authenticate as admin
- The script generates cryptographically secure keys using the `cryptography`
  library
- Run this script on a secure machine and store the credentials file safely
- The generated SQL can be executed directly against your PostgreSQL database

### Example Output

```sql
-- Step 1: Update sequence
SELECT setval('users_id_seq', 1000, true);

-- Step 2: Insert admin user
INSERT INTO users (id, name, surname, email, confidentiality_level, integrity_levels, public_key, expires_at)
VALUES (
    1000,
    'Admin',
    'User',
    'admin@example.com',
    4,
    ARRAY[3,4],
    '\x1234567890abcdef...',
    '2025-09-30T10:00:00'
);
```

### Access Levels Reference

- `1` = UNCLASSIFIED
- `2` = CONTROLLED
- `3` = RESTRICTED
- `4` = CONFIDENTIAL

### Manual User ID Setting

The script uses PostgreSQL's `setval()` function to manually set the user ID:
- Ensures the specified ID is used for the admin user
- Updates the sequence counter to prevent conflicts with future auto-generated
  IDs
- Recommended to use a high ID (e.g., 1000+) to avoid conflicts with regular
  users
