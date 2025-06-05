from sympy.core.numbers import Float, Integer

def strip(text):
    '''strip trailing spaces and return text'''
    try:
        result = text.lstrip().rstrip()
        return result
    except (ValueError, TypeError):
        return None

def round_up(value, n=5):
    '''round up value to n decimal places'''
    if isinstance(value, float):
        return round(value, n)
    elif isinstance(value, str):
        return round_up(float(value), n)
    elif isinstance(value, Float) or isinstance(value, Integer):
        try:
            return round_up(float(value), n)
        except:
            return "improper data type"
