from django.db import models
from django.conf import settings

class ProviderProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=50)
    bio = models.CharField(max_length=150)
    appointment_duration = models.TimeField()

    TIMEZONES = {
        'PST': 'PST',
        'EST': 'EST',
        'AST': 'AST',
        'GMT': 'GMT',
        'CAT': 'CAT'
    }

    timezone = models.CharField(choices=TIMEZONES)
    # is_available = models.BooleanField(defult=True)

class Availability(models.Model):
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE)
    WEEKDAY = {
        'Monday': 'Monday',
        'Tuesday': 'Tuesday',
        'Wednesday': 'Wednesday',
        'Thursday': 'Thursday',
        'Friday': 'Friday',
        'Saturday': 'Saturday',
        'Sunday': 'Sunday'
    }
    weekday = models.CharField(choices=WEEKDAY)
    start_time = models.TimeField()
    end_time = models.TimeField()

class Appointment(models.Model):
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    STATUS = {
        'Confirmed': 'Confirmed',
        'Cancelled': 'Cancelled',
        'Completed': 'Completed'
    }
    status = models.CharField(choices=STATUS)

class AvailableSlots(models.Model):
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    time = models.TimeField()
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)

    WEEKDAY = {
        'Monday': 'Monday',
        'Tuesday': 'Tuesday',
        'Wednesday': 'Wednesday',
        'Thursday': 'Thursday',
        'Friday': 'Friday',
        'Saturday': 'Saturday',
        'Sunday': 'Sunday'
    }
    weekday = models.CharField(choices=WEEKDAY)
    Taken = models.BooleanField(default=False)