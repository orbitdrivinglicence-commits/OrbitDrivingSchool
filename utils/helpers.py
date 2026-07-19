from datetime import datetime


def current_date():
    """
    Returns current date in DD-MM-YYYY format.
    Example: 13-07-2026
    """
    return datetime.now().strftime("%d-%m-%Y")


def current_time():
    """
    Returns current time in HH:MM:SS format.
    """
    return datetime.now().strftime("%H:%M:%S")


def current_datetime():
    """
    Returns current date & time.
    Example: 13-07-2026 10:30:25
    """
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def clean_text(text):
    """
    Removes extra spaces.
    """
    if text is None:
        return ""

    return str(text).strip()


def is_number(value):
    """
    Checks whether value is a valid number.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


def format_currency(amount):
    """
    Returns amount with ₹ symbol.
    Example: ₹500.00
    """
    try:
        return f"₹{float(amount):,.2f}"
    except:
        return "₹0.00"
