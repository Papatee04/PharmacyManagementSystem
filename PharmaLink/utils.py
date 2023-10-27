from .models import CustomUser

def is_admin(user):
    return user.user_type == '1' or user.is_superuser

def is_pharmacist(user):
    return user.user_type == '2'

def is_doctor(user):
    return user.user_type == '3'

def is_patient(user):
    is_patient = user.user_type == '5'
    print('user type is ' + str(user.user_type))  # Convert user.user_type to a string
    if is_patient:
        print('Success: User is a patient.')
    else:
        print('Fail: User is not a patient.')
    return is_patient

def is_doctor_or_pharma(user):
    return user.user_type == '3' or user.user_type == '2'