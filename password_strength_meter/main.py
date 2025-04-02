import re
from typing import Dict, List, Tuple

def check_password_strength(password: str) -> Tuple[int, List[str], List[str]]:
    """
    Check the strength of a password and return a score along with feedback.
    Returns: (score, strengths, weaknesses)
    """
    score = 0
    strengths = []
    weaknesses = []
    
    # Check length
    if len(password) >= 12:
        score += 2
        strengths.append("Good length (12+ characters)")
    elif len(password) >= 8:
        score += 1
        strengths.append("Acceptable length (8+ characters)")
    else:
        weaknesses.append("Password is too short (less than 8 characters)")
    
    # Check for numbers
    if re.search(r"\d", password):
        score += 1
        strengths.append("Contains numbers")
    else:
        weaknesses.append("No numbers")
    
    # Check for lowercase letters
    if re.search(r"[a-z]", password):
        score += 1
        strengths.append("Contains lowercase letters")
    else:
        weaknesses.append("No lowercase letters")
    
    # Check for uppercase letters
    if re.search(r"[A-Z]", password):
        score += 1
        strengths.append("Contains uppercase letters")
    else:
        weaknesses.append("No uppercase letters")
    
    # Check for special characters
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
        strengths.append("Contains special characters")
    else:
        weaknesses.append("No special characters")
    
    # Check for common patterns
    if re.search(r"(.)\1{2,}", password):
        weaknesses.append("Contains repeated characters")
    
    # Check for common words
    common_words = ["password", "123456", "qwerty", "admin", "letmein"]
    if any(word in password.lower() for word in common_words):
        weaknesses.append("Contains common words or patterns")
    
    return score, strengths, weaknesses

def get_strength_level(score: int) -> str:
    """Convert numerical score to strength level description."""
    if score >= 5:
        return "Strong"
    elif score >= 3:
        return "Medium"
    else:
        return "Weak"

def main():
    print("Password Strength Meter")
    print("=====================")
    
    while True:
        password = input("\nEnter a password to check (or 'q' to quit): ")
        
        if password.lower() == 'q':
            break
            
        score, strengths, weaknesses = check_password_strength(password)
        strength_level = get_strength_level(score)
        
        print("\nPassword Strength Analysis:")
        print(f"Score: {score}/7")
        print(f"Strength Level: {strength_level}")
        
        if strengths:
            print("\nStrengths:")
            for strength in strengths:
                print(f"✓ {strength}")
        
        if weaknesses:
            print("\nWeaknesses:")
            for weakness in weaknesses:
                print(f"✗ {weakness}")
        
        print("\n" + "="*50)

if __name__ == "__main__":
    main()
