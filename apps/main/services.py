from rest_framework.response import Response
from .models import Appointment

def booked_up(book_date, book_time, doctor):
    """
    If time is already booked,
    shows response that time is occupied
    """

    entries = Appointment.objects.filter(doctor=doctor)
    if entries:
        for e in entries:
            if str(e.date) == str(book_date):
                if str(e.time) == str(e.TIME[int(book_time)][-1]):
                    return True
    else:
        return False

