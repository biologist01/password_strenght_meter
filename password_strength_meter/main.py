import streamlit as st
import random
import string
import secrets

# Define custom scoring weights
weights = {
    "length": 2,
    "uppercase": 1,
    "lowercase": 1,
    "digit": 1,
    "special": 1
}
# Maximum possible score = 6

# Blacklist common weak passwords (all in lowercase for case-insensitive comparison)
blacklist = {"password", "123456", "password123", "qwerty", "letmein", "111111", "123123"}

def evaluate_password(password):
    score = 0
    feedback = []
    
    # Check against blacklist
    if password.lower() in blacklist:
        feedback.append("This password is too common and easily guessable. Please choose a different password.")
        return 0, "Blacklisted", feedback

    # Check for minimum length (at least 8 characters)
    if len(password) >= 8:
        score += weights["length"]
    else:
        feedback.append("Increase the length to at least 8 characters.")

    # Check for at least one uppercase letter
    if any(c.isupper() for c in password):
        score += weights["uppercase"]
    else:
        feedback.append("Include at least one uppercase letter.")

    # Check for at least one lowercase letter
    if any(c.islower() for c in password):
        score += weights["lowercase"]
    else:
        feedback.append("Include at least one lowercase letter.")

    # Check for at least one digit (0-9)
    if any(c.isdigit() for c in password):
        score += weights["digit"]
    else:
        feedback.append("Include at least one digit (0-9).")

    # Check for at least one special character from !@#$%^&*
    special_chars = "!@#$%^&*"
    if any(c in special_chars for c in password):
        score += weights["special"]
    else:
        feedback.append("Include at least one special character (!@#$%^&*).")

    # Determine strength level based on score
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    else:
        strength = "Strong"
        
    return score, strength, feedback

def generate_strong_password(length=12):
    """Generate a strong password ensuring at least one character from each required category."""
    if length < 8:
        length = 8
    
    # Ensure each category is represented
    upper = secrets.choice(string.ascii_uppercase)
    lower = secrets.choice(string.ascii_lowercase)
    digit = secrets.choice(string.digits)
    special = secrets.choice("!@#$%^&*")
    
    # Fill the remaining length with a random mix of all characters
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*"
    remaining = [secrets.choice(all_chars) for _ in range(length - 4)]
    
    # Combine and shuffle the list to avoid predictable patterns
    password_list = list(upper + lower + digit + special + "".join(remaining))
    random.shuffle(password_list)
    password = "".join(password_list)
    return password

# ----------------------------
# Streamlit User Interface
# ----------------------------
st.title("🔒 Password Strength Meter & Generator")

st.markdown("""
This app evaluates your password based on several security rules, provides suggestions for improvements, 
and can even generate a strong password for you!
""")

# Password input field
password_input = st.text_input("Enter your password:", type="password")

# Evaluate Password Button
if st.button("Evaluate Password"):
    if password_input:
        score, strength, suggestions = evaluate_password(password_input)
        st.write(f"**Password Strength:** {strength} (Score: {score} out of 6)")
        if strength == "Strong":
            st.success("Your password is strong. Great job!")
        elif strength == "Blacklisted":
            st.error("This password is blacklisted. Please choose a different password.")
        else:
            st.warning("Your password is weak. Consider the following improvements:")
            for suggestion in suggestions:
                st.write(f"- {suggestion}")
    else:
        st.info("Please enter a password to evaluate.")

st.markdown("---")

# Generate a Strong Password Button
if st.button("Generate a Strong Password"):
    generated_password = generate_strong_password(12)
    st.write("**Suggested Strong Password:**")
    st.code(generated_password)
