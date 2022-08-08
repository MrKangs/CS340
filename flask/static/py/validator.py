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

def validate_exchangeorder_input(amountfilled, orderprice, fiatwallet, dogecoinwallet, ordertype, orderdirection):
    try:
        float(amountfilled)
        float(orderprice)
        if fiatwallet == "Select" or dogecoinwallet == "Select" or orderdirection == "Select" or ordertype == "Select":
            return False
        return True
    except ValueError:
        return False

def validate_dogecointransaction_input(amount, dogecoinwallet, direction):
    try:
        float(amount)
        if dogecoinwallet == "Select" or direction == "Select":
            return False
        return True
    except ValueError:
        return False