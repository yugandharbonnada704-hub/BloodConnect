import re

def validate_email(email):
    if not email:
        return False
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_phone(phone):
    if not phone:
        return False
    # Standard phone validation (matches 10 digits with optional +91 or 0 prefix)
    pattern = r'^(?:\+91|0)?[6-9]\d{9}$'
    return bool(re.match(pattern, phone))

def validate_blood_group(blood_group):
    valid_groups = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    return blood_group in valid_groups

def validate_donor_profile_data(data):
    errors = []
    
    # Required check
    required_fields = ['full_name', 'phone_number', 'state', 'district', 'city']
    for field in required_fields:
        if not data.get(field) or not str(data.get(field)).strip():
            errors.append(f"Field '{field}' is required.")

    # Age check
    age = data.get('age')
    if age is not None:
        try:
            age_int = int(age)
            if age_int < 18 or age_int > 65:
                errors.append("Age must be between 18 and 65 to register as a donor.")
        except (ValueError, TypeError):
            errors.append("Age must be a valid integer.")
            
    # Blood group check
    bg = data.get('blood_group')
    if bg and not validate_blood_group(bg):
        errors.append(f"Invalid blood group '{bg}'.")
        
    # Phone validation
    phone = data.get('phone_number')
    if phone and not validate_phone(phone):
        errors.append("Invalid phone number format.")
        
    # Email check
    email = data.get('email')
    if email and not validate_email(email):
        errors.append("Invalid email address.")
        
    return errors
