def validate_name(name):
    if len(name.split(' ')) != 3:
        raise Exception('Неправильно заполнены ФИО!')
    return name


def validate_phone(phone):
    if len(phone) != 11:
        raise Exception('Неправильный формат номера телефона!')
    return phone


def validate_email(email):
    if '@' not in email:
        raise Exception('Неправильный формат Email!')
    return email
