import re

def all_emails(prompt):
    return re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", prompt)