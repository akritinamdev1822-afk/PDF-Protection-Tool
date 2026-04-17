import re
import random
import string

def check_password_strength(password):
    """
    Evaluates password strength.
    Returns a tuple: (Strength Label, Color for UI)
    """
    if not password:
        return "Empty", "gray"
        
    length = len(password)
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    
    score = sum([1 for x in (has_upper, has_lower, has_digit, has_special) if x])
    
    if length >= 8 and score >= 3:
        return "Strong", "green"
    elif length >= 6 and score >= 2:
        return "Medium", "orange"
    else:
        return "Weak", "red"

def generate_strong_password(length=16):
    """Generates a random, strong password that fulfills strict criteria."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    while True:
        password = ''.join(random.choice(characters) for i in range(length))
        if check_password_strength(password)[0] == "Strong":
            return password
