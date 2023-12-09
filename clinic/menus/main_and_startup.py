from enum import Enum
from modules import io,table,models
from menus.admin_menu import admin_menu
from menus.doctor_menu import doctor_menu
from menus.patient_menu import patient_menu


class AccessLevel(Enum):
    """Provides access to
    some tables and their columns."""
    ADMIN = 0
    DOCTOR = 1
    PATIENT = 2
    UNKNOWN = 3


def print_startup_cmds(indent_contr):
    """Shows startup commands."""
    indent_contr.print_text(
        'Press "x" to stop program.\n\n'
        "Types of commands and their codes:\n"
        '1 - help;\n'
        '2 - sign in;\n'
        '3 - sign up as a patient.')


@io.loop()
def main_menu(indent_contr):
    """Provides such functions
    as sign in, sign up, go to
    some mode (admin,doctor,patient)."""
    result = startup_menu(indent_contr)
    if result.r_type == io.ResponseType.EXIST:
        return result

    access_lvl,_id = result.obj

    match access_lvl:
        case AccessLevel.ADMIN:
            indent_contr.print_text(
                "You was signed in as an administrator.")
            result = admin_menu(indent_contr,_id=_id)
        case AccessLevel.DOCTOR:
            indent_contr.print_text(
                "You was signed in as a doctor.")
            result = doctor_menu(indent_contr,_id=_id)
        case AccessLevel.PATIENT:
            indent_contr.print_text(
                "You was signed in as a patient.")
            result = patient_menu(indent_contr,_id=_id)

    return result


@io.loop(False,3,print_startup_cmds)
def startup_menu(indent_contr,code):
    """Tries to sign in or sign up.
    If it was succesful returns user
    access level (admin, doctor, patient, unknown),
    id of person in corresponded table
    (Admins, Doctors, Patients)."""
    
    email = indent_contr. \
        get_input_parameter('Email',str)
    password = indent_contr. \
        get_input_parameter('Password',str)

    u_ids = [entry.id for entry in models.User.select()]
    users = table.Table(u_ids,models.User,["email","password"],
        ["email","password"],True)

    match code:
        case 2:
            result = sign_in(users,email,password)

            access_lvl,_id = result

            if access_lvl == AccessLevel.UNKNOWN:
                raise Exception(
                    "Can't find any persons related with"
                    " this user. Try to sign up with this"
                    " email and password.")
            raise io.BackToPreviousException(
                "You was successfully signed in.\n"
                f'Your email: "{email}".',result)
        case 3:
            result = sign_up(indent_contr,users,
                                email,password)
            raise io.BackToPreviousException(
                "You was successfully sigined up.\n"
                f'Your email: "{email}".',result)


def sign_in(users,email,password):
    """Sign in as admin, doctor or
    a patient. If it was succesful
    returns user access level (admin,
    doctor,patient,unknown), id of person in
    corresponded table (Admins,Doctors,Patients)
    and email."""
    users.update_cached(table.Mode.FILTER,1,
                    start=email,end=email)
    users.update_cached(table.Mode.FILTER,2,
                    start=password,
                    end=password)
    cached = users.cached

    if len(cached) == 1:
        raise ValueError("Incorrect email or password.")
    _id = cached[1][0].number

    result = get_access_level(_id,users)
    return result


def sign_up(indent_contr,users,
            email,password):
    """Signs up into account as patient.
    Returns access level, id in the
    Patients table."""
    _id = users.add_entry(f"{email},{password}")
    users.remove_entry(_id)

    p_id = add_new_patient(indent_contr,users,
        email,password)
    return [AccessLevel.PATIENT,p_id]


def get_access_level(user_id,users):
    """Determines access level by user id.
    Returns level and id of person in the
    corresponded table."""
    a_ids = [entry.id for entry in models.Admin.select()]
    admins = table.Table(a_ids,models.Admin,["user"],[],False)
    admins.update_cached(table.Mode.FILTER,1,
        start=str(user_id),end=str(user_id))
    cached = admins.cached

    if len(cached) == 2:
        return [AccessLevel.ADMIN,
                cached[1][0].number]

    d_ids = [entry.id for entry in models.Doctor.select()]
    doctors = table.Table(d_ids,models.Doctor,["user"],[],False)
    doctors.update_cached(table.Mode.FILTER,1,
        start=str(user_id),end=str(user_id))
    cached = doctors.cached

    if len(cached) == 2:
        return [AccessLevel.DOCTOR,
                cached[1][0].number]

    p_ids = [entry.id for entry in models.Patient.select()]
    patients = table.Table(p_ids,models.Patient,["user"],[],False)
    patients.update_cached(table.Mode.FILTER,1,
        start=str(user_id),end=str(user_id))
    cached = patients.cached

    if len(cached) == 2:
        return [AccessLevel.PATIENT,
                cached[1][0].number]

    users.remove_entry(user_id)

    return [AccessLevel.UNKNOWN]


def add_new_patient(indent_contr,users,email,password):
    """Adds new patient. Returns patient id."""
    p_ids = [entry.id for entry in models.Patient.select()]
    patients = table.Table(p_ids,models.Patient,[
        "passport","date_of_birth","full_name",
        "place_of_residence","user"],
        ["passport","date_of_birth",
        "full_name","place_of_residence",
        "user"],True)
    passport = indent_contr. \
        get_input_parameter('Passport (series number)',str)
    date_of_birth = indent_contr. \
        get_input_parameter('Date of birth (dd.mm.yyyy)',str)
    full_name = indent_contr. \
        get_input_parameter('Full name',str)
    place_of_residence = indent_contr. \
        get_input_parameter(
            'Place of residence (country city street '
                'building apartment)',str)

    user_id = str(users.add_entry(f"{email},{password}"))

    patient_id = patients.add_entry(
        f"{passport},{date_of_birth},{full_name},"
        f"{place_of_residence},{user_id}")
    return patient_id
