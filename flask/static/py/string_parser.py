def splitPKString(pkString):
    """
    Split a string of the form "U0,U1,U2" into a list of elements.
    """
    return pkString.split(",")

def replace_char(string, oldChar, newChar):
    """
    Replace all instances of oldChar in string with newChar.
    """
    return string.replace(oldChar, newChar)