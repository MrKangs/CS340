def validate_user_input(email):
    if "@" in email and "." in email:
        return True
    else:
        return False

def validate_fiatwallet_input(fiatwalletbalance):
    try:
        float(fiatwalletbalance)
        return True
    except ValueError:
        return False

def validate_dogecoinwallet_input(dogecoinbalance):
    try:
        float(dogecoinbalance)
        return True
    except ValueError:
        return False

def validate_exchangeorder_input(amountfilled, orderprice):
    try:
        float(amountfilled)
        float(orderprice)
        return True
    except ValueError:
        return False

def validate_dogecointransaction_input(amount):
    try:
        float(amount)
        return True
    except ValueError:
        return False