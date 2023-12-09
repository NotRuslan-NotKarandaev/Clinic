"""Common functions."""
import datetime as dt
from enum import Enum
from modules import io,matrix,number
from modules import wrappers
from modules import table
from modules import models



def get_tables_related_to_appointments(*,d_id:int=-1,
                                       p_id:int=-1):
    """Returns Appointments, Doctors, Vocations,
    Users, Patients, Users tables with entries
    related to the doctor or the patient."""
    appointments = table.get_table_by_name("Appointments",False)
    names = appointments.fields_names_r.copy()
    names.insert(0,"ID")

    if p_id == -1:
        index = names.index("doctor")
        appointments.update_cached(table.Mode.FILTER,index,
            start=str(d_id),end=str(d_id))
        appointments.fields_names_w = \
            ["real_date","real_start","real_end","was_over"]
    else:
        index = names.index("patient")
        appointments.update_cached(table.Mode.FILTER,index,
            start=str(p_id),end=str(p_id))
        appointments.fields_names_w = \
            ["real_date","real_start","real_end"]
    cached = appointments.cached
    a_ids = list(map(
        lambda x: x.number,matrix.get_column(0,cached[1:])))
    appointments.ids = a_ids

    doctors,users,_,vocations = get_doctors_info()

    patients = table.get_table_by_name("Patients",False)
    patients.fields_names_w = []
    patients.fields_names_r = ["full_name"]

    return [appointments,doctors,vocations,users,patients,users]


def get_shedule(d_id:int):
    """Returns immutable Shedules with shedule of the doctor."""
    doctors = table.get_table_by_name("Doctors",False)

    s_id = doctors.get_wrapper(d_id,"shedule").number
    shedules = table.get_table_by_name("Shedules",False)
    shedules.fields_names_w = []
    shedules.ids = [s_id]
    return shedules


def get_first_unmarked_appointment(appointments):
    """Returns the first appointment ID for specified doctor
    which wasn't over."""
    appointments.update_cached(table.Mode.SORT,4,reverse=False)
    appointments.update_cached(table.Mode.SORT,3,reverse=False)
    appointments.update_cached(table.Mode.FILTER,8,
        start="0",end="0")
    a_id = appointments.cached[1][0].number

    appointments.update_cached()
    return a_id


def check_time(time,shedules,finished_ids,
               appointments):
    """Returns bool that indicates time is in
    valid time span."""

    intermediate = check_time_base(time,shedules)
    if intermediate is False:
        return False

    max_end = wrappers.Time("0:0:0")
    for _id in finished_ids:
        real_end = appointments.get_wrapper(_id.number,"real_end")
        max_end = max(max_end,real_end)

    return time > max_end


def check_time_base(time,shedules):
    """Returns bool that indicates time is in
    valid time span."""
    shedules.update_cached()
    *_,start,l_start,l_end,end = shedules.cached[1]
    if time < start:
        return False
    if l_start.value is None:
        if time <= end:
            return True
        return False
    if time < l_start:
        return True
    if time <= l_end:
        return False
    if time <= end:
        return True
    return False


def optimize_appointments(appointments,shedules):
    """Takes appointments table and shedules table for
    the particular doctor and tries to
    shift real starts and ends for all appointments
    which have not yet been completed
    and maybe dates so that the spans of appointments
    do not intersect each other and all real start
    times are as close as possible to the expected ones."""

    appointments.update_cached()
    dates = matrix.get_column(1,appointments.cached[1:])
    unique_dates = []
    for date in dates:
        if not date.date in \
            list(map(lambda x: x.date,unique_dates)):
            unique_dates.append(date)

    unique_dates.sort()

    for _id in appointments.ids:
        date = appointments.get_wrapper(_id,"date")
        appointments.update_field(
            _id,"real_date",date.value)

    d_index = 0

    while d_index < len(unique_dates):
        date = unique_dates[d_index]

        finished_ids = get_ids_of_appointments(
            appointments,date)
        unfinished_ids = get_ids_of_appointments(
            appointments,date,True)

        weights = [1,1]

        for _i in range(len(unfinished_ids[2:])):
            weights.append(weights[_i] + weights[_i + 1])

        weights = weights[::-1]

        respond = get_not_intersected_spans([],appointments,
                   unfinished_ids,weights,
                   finished_ids,shedules)
        if respond is None:
            _id = unfinished_ids[-1].number
            real_date = appointments.get_wrapper(_id,"real_date")
            weekday = real_date.date.weekday()
            days_in_week = shedules.cached[1][1].number
            _d = 8 - days_in_week if weekday + 1 == days_in_week \
                else 1
            real_date.date = real_date.date + dt.timedelta(days=_d)
            real_date.value = str(real_date)
            appointments.update_field(_id,"real_date",real_date.value)
            if not real_date.date in \
                list(map(lambda x: x.date,unique_dates)):
                unique_dates.append(real_date)
            unique_dates.sort()
            d_index = unique_dates.index(date)
        else:
            d_index += 1
            _,spans = respond
            for span,_id in zip(spans,unfinished_ids):
                appointments.update_field(
                    _id.number,"real_start",span[0].value)
                appointments.update_field(
                    _id.number,"real_end",span[1].value)


def get_not_intersected_spans(spans,appointments,
      unfinished_ids,weights,
      finished_ids,shedules,
      percision = 250):
    """Returns not intersected spans whish
    are located as close as possible to
    preferred start values."""
    if len(unfinished_ids) == 0:
        return [0,spans]

    _id = unfinished_ids[0]
    start = appointments.get_wrapper(_id.number,"start")
    real_start = appointments.get_wrapper(_id.number,"real_start")
    real_end = appointments.get_wrapper(_id.number,"real_end")
    length,_ = real_end - real_start

    min_deltas_sum = 10**20
    result_spans = None
    for new_delta in range(- wrappers.Time.MAX_SECONDS + 1,
                           wrappers.Time.MAX_SECONDS,
                           percision):
        if new_delta < 0:
            new_delta_t = wrappers.Time.from_seconds(abs(new_delta))
            real_start,was_shifted = start - new_delta_t
        else:
            new_delta_t = wrappers.Time.from_seconds(new_delta)
            real_start,was_shifted = start + new_delta_t
        if was_shifted:
            continue
        real_end,was_shifted = real_start + length
        if was_shifted:
            continue

        if not (check_time(real_start,shedules, \
            finished_ids,appointments) and \
            check_time(real_end,shedules, \
            finished_ids,appointments)):
            continue

        new_span = [real_start,real_end]

        cont_flag = 0
        for span in spans:
            if not are_not_spans_intersected(new_span,span):
                cont_flag = 1
                break
        if cont_flag:
            continue

        c_spans = spans.copy()
        c_spans.append([real_start,real_end])

        respond = get_not_intersected_spans( \
            c_spans,appointments,unfinished_ids[1:], \
            weights[1:],finished_ids,shedules)
        if respond is None:
            continue

        c_sum,c_spans = respond
        c_sum += abs(new_delta) \
            * weights[0]
        if c_sum < min_deltas_sum:
            min_deltas_sum = c_sum
            result_spans = c_spans
    if result_spans is None:
        return None
    return [min_deltas_sum,result_spans]


def are_not_spans_intersected(span1,span2):
    """Checks if spans are not intersected."""
    return (span1[0] > span2[1]) or (span1[1] < span2[0])


def get_ids_of_appointments(appointments,date:wrappers.Date=None,
                            unfinished=False):
    """Returns IDs of unfinished of finished appointments.
    IDs sorted in ascending order."""

    if unfinished:
        appointments.update_cached(table.Mode.FILTER,8,start="0",end="0")
    else:
        appointments.update_cached(table.Mode.FILTER,8,start="1",end="1")
    if not date is None:
        appointments.update_cached(
            table.Mode.FILTER,3,start=date.value,end=date.value)

    appointments.update_cached(table.Mode.SORT,0,reverse=False)

    ids = matrix.get_column(0,appointments.cached[1:])

    appointments.update_cached()

    return ids


def get_doctors_info():
    """Returns Doctors, Users, Shedules, Vocations
    tables with entries that match doctors."""
    doctors = table.get_table_by_name("Doctors",False)
    doctors.fields_names_w = []
    doctors.fields_names_r = ["full_name",
        "average_appointment_time"]

    shedules = table.get_table_by_name("Shedules",False)
    shedules.fields_names_w = []
    shedules.fields_names_r = \
        ["start","lunch_start","lunch_end","end"]

    vocations = table.get_table_by_name("Vocations",False)
    vocations.fields_names_w = []
    vocations.fields_names_r = ["name"]

    users = table.get_table_by_name("Users",False)
    users.fields_names_w = []
    users.fields_names_r = ["email"]
    return [doctors,users,shedules,vocations]