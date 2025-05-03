import re
from datetime import datetime

# Utility functions for validation
def validate_name(name, field_name):
    if not re.match(r'^[a-zA-Z0-9\s~_\-]+$', name):
        raise ValueError(f"Invalid {field_name}. Only alphabets, digits, spaces, ~, _, - are allowed.")

def validate_email(email):
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise ValueError("Invalid email format.")

def validate_phone(phone):
    if not re.match(r'^(\+91)?[0-9]{10}$', phone):
        raise ValueError("Invalid phone number. Must be 10 digits or +91 followed by 10 digits.")

def validate_chargeable(value):
    if value.lower() not in ['true', 'false', 'yes', 'no']:
        raise ValueError("Chargeable must be True/False or Yes/No.")

def validate_hours(hours):
    try:
        hours = float(hours)
        if hours <= 0 or hours > 8:
            raise ValueError("Hours must be between 0 and 8.")
    except ValueError:
        raise ValueError("Hours must be a number.")

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y/%m/%d')
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY/MM/DD")

def validate_zip_code(zip_code):
    if not re.match(r'^\d+$', zip_code):
        raise ValueError("Zip code must contain only digits.")

def validate_alphabets(value, field_name):
    if not re.match(r'^[a-zA-Z\s]+$', value):
        raise ValueError(f"{field_name} must contain only alphabets and spaces.")

def validate_address_field(value, field_name):
    if not re.match(r'^[a-zA-Z0-9\s\-_#/,]+$', value):
        raise ValueError(f"Invalid {field_name}. Only alphanumeric characters, spaces, and basic punctuation are allowed.")