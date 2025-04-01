import random
import string

def generate_unique_short_code(existing_short_code):
    while True:
        new_short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if new_short_code != existing_short_code:
            return new_short_code