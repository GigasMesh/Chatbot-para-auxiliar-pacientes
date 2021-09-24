import datetime as dt
from pycep_correios import get_address_from_cep, WebService, exceptions

def inputTypeVerification(message, type):
    # Possible types:
    # 0 - Full name
    # 1 - Birth date
    # 2 - Sex
    # 3 - CEP
    # symptoms - Interval
    if type == 0:
        return fullNameValidation(message)
    elif type == 1:
        return dateValidation(message)
    elif type == 2:
        return sexValidation(message)
    elif type == 3:
        return cepValidation(message)
    elif type == 'symptoms':
        return intervalValidation(message,0,4)


def fullNameValidation(message):
    # Aaa Bbb Ccc
    if message.replace(" ", "").isalpha() and len(message) > 3:
        return True
    else:
        return False

def dateValidation(message):
    # DD/MM/AAAA
    try:
        dt.datetime.strptime(message, '%d/%m/%Y')
    except ValueError:
        return False
    return True

def sexValidation(message):
    # Feminino/Masculino/M/F
    messageCap = message.capitalize()
    if messageCap == "Feminino" or messageCap == "Masculino" or messageCap == "M" or messageCap == "F":
        return True
    return False

def cepValidation(message):
    # five digits - hifen - three digits
    try:
        get_address_from_cep(message, webservice=WebService.APICEP)
    except exceptions.InvalidCEP:
        return False
    except exceptions.CEPNotFound:
        return False
    return True

def intervalValidation(message, limit1, limit2):
    symptomOption = int(message)
    if symptomOption >= limit1 and symptomOption <= limit2:
        return True
    return False
