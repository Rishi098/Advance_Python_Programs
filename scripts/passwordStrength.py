import argparse
import math
import re
import time

# Optional color support
try:
    from shutil import get_terminal_size
    COLORS = True
except ImportError:
    COLORS = False

def colorize(text, color):
    if not COLORS:
        return text
    colors = {
        "red": "\033[91m",
        "yellow": "\033[93m",
        "green": "\033[92m",
        "reset": "\033[0m"
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"

def password_entropy(password: str) -> float:
    """Estimate entropy (bits) based on character diversity and length."""
    charsets = [
        (r"[a-z]", 26),
        (r"[A-Z]", 26),
        (r"[0-9]", 10),
        (r"[^a-zA-Z0-9]", 33),
    ]
    pool = sum(size for pattern, size in charsets if re.search(pattern, password))
    if not pool:
        pool = 1
    entropy = len(password) * math.log2(pool)
    return entropy

def crack_time(entropy: float, guesses_per_second: float = 1e10) -> str:
    """Convert entropy to estimated brute-force crack time."""
    seconds = 2 ** (entropy - 1) / guesses_per_second
    units = [("seconds", 60), ("minutes", 60), ("hours", 24),
             ("days", 365), ("years", 1000)]
    for name, scale in units:
        if seconds < scale:
            return f"{seconds:.2f} {name}"
        seconds /= scale
    return f"{seconds:.2f} millennia"

def strength_rating(entropy: float) -> str:
    """Categorize strength based on entropy bits."""
    if entropy < 28:
        return colorize("Very Weak", "red")
    elif entropy < 36:
        return colorize("Weak", "yellow")
    elif entropy < 60:
        return colorize("Strong", "green")
    else:
        return colorize("Very Strong", "green")

def common_patterns(password: str) -> list[str]:
    """Check for simple patterns and dictionary words."""
    issues = []
    if password.lower() in {"password", "admin", "letmein", "123456", "qwerty"}:
        issues.append("Common password found.")
    if re.match(r"^[a-z]+[0-9]+$", password.lower()):
        issues.append("Predictable pattern (letters + numbers).")
    if password.isdigit():
        issues.append("Numeric-only password.")
    if len(password) < 8:
        issues.append("Too short (less than 8 chars).")
    return issues

def analyze(password: str):
    entropy = password_entropy(password)
    rating = strength_rating(entropy)
    time_est = crack_time(entropy)
    issues = common_patterns(password)

    print("\nPassword Analysis:")
    print("------------------")
    print(f"Password length: {len(password)}")
    print(f"Entropy: {entropy:.2f} bits")
    print(f"Estimated crack time: {time_est}")
    print(f"Strength: {rating}")
    if issues:
        print("\nIssues found:")
        for issue in issues:
            print(" - " + colorize(issue, "red"))
    else:
        print("\nNo major issues detected ✅")

def main():
    parser = argparse.ArgumentParser(description="Password Strength Analyzer")
    parser.add_argument("password", nargs="?", help="Password to analyze")
    args = parser.parse_args()

    if not args.password:
        try:
            import getpass
            args.password = getpass.getpass("Enter a password to analyze: ")
        except Exception:
            args.password = input("Enter a password to analyze: ")

    print("\nAnalyzing password, please wait...")
    time.sleep(0.3)
    analyze(args.password)

if __name__ == "__main__":
    main()
