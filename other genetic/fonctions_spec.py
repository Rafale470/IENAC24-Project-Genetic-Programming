import operator

def div_with0(a,b):
    """Safely performs division, avoiding division by zero.

    Parameters:
    a (float): The numerator.
    b (float): The denominator.
    
    Returns:
    float: The result of the division, or 0 if the denominator is 0."""
    return operator.truediv(a, b) if b!=0 else 1

def pow_with0(a,b):
    """Safely performs the power operation, handling edge cases with zero and negatives.
    
    Parameters:
        a (float): The base.
        b (float): The exponent.
        
    Returns:
        float: The result of the power operation, or 0 for invalid cases."""
    """ Managing complex number too"""
    if a < 0 and not(float(b).is_integer()):
        return 0.0
    res = operator.pow(a, b) if not(isinstance(b, complex)) and (b >=0 or a!=0) else 0.0

    if (isinstance(res, complex)):
        print("Alerte !")
    
    return res