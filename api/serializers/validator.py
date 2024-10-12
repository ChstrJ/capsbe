from django.core.validators import RegexValidator


required = RegexValidator(
    regex=r'^(?!\s*$).+',
    message="This {field} is required"  
)

one_to_ten = RegexValidator(
    regex = r'^(10|[1-9])$',
    message = "Rate must be 1 - 10 only"
)

format_09 = RegexValidator(
    regex = r'^09',
    message = "This must be in the format of '09.'"
)

numbers_only = RegexValidator(
    regex = r'\d+',
    message = "Numbers only"
)

letters_only = RegexValidator (
    regex = r'^[A-Za-z ]+$',
    message = "Symbols and numbers are not allowed."
)

must_contains_letters = RegexValidator(
    regex = r'.*[a-zA-Z]+.*',
    message = "Must contain letters"
)

letters_numbers_underscores = RegexValidator(
    regex = r'^[a-zA-Z0-9_]+$',
    message = "This can only have letters, numbers, and underscores"
)

time_pattern_12hr = RegexValidator(
    regex = r'^(0?[1-9]|1[0-2]):[0-5][0-9][APap][mM]$',
    message = "Time must be in the format HH:MM AM/PM."
)

time_pattern_24hr = RegexValidator(
    regex=r'^([01][0-9]|2[0-3]):[0-5][0-9]$',
    message="Invalid time format. Please use the 24-hour format (HH:MM)."
)