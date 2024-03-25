from django.core.exceptions import ValidationError
import re

def validate_iranian_phone_number(value):
    pattern = r'^09\d{9}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid Iranian cellphone number')