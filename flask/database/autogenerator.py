import random
import string

def generate_pk_userAccounts(number:int):
    pk_value = str("U" + str(number))
    number += 1
    return pk_value, number

def generate_pk_fiatWallets(number:int):
    pk_value = str("F" + str(number))
    number += 1
    return pk_value, number

def generate_pk_dogecoinWallets(number:int):
    pk_value = str("D" + str(number))
    number += 1
    return pk_value, number

def generate_pk_dogecoinTransactions(number:int):
    pk_value = str("T" + str(number))
    number += 1
    return pk_value, number

def generate_pk_exchangeOrders(number:int):
    pk_value = str("E" + str(number))
    number += 1
    return pk_value, number

def generate_external_wallet_id(redundant_set: set):
    while(True):
        value = ''.join(random.choices("abcdef" + string.digits, k=64))
        if not (value in redundant_set):
            redundant_set.add(value)
            break
    return value, redundant_set

def generate_transaction_hash(redundant_set: set):
    while(True):
        value = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=34))
        if not (value in redundant_set):
            redundant_set.add(value)
            break
    return value, redundant_set