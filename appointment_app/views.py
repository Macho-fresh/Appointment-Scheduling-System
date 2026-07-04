from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework import status, response, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.views import Provider, NotProvider
from datetime import datetime, timedelta, date
from .serializer import *
from rest_framework.authentication import SessionAuthentication

# class CsrfExemptSessionAuthentication(SessionAuthentication):
#     def enforce_csrf(self, request):
#         return

class CreateProviderProfileView(APIView):
    permission_classes = [Provider]
    # authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        user = request.user
        specialization = request.data.get('specialization')
        bio = request.data.get('bio')
        appointment_duration = request.data.get('appointment_duration')
        timezone = request.data.get('timezone')

        ProviderProfile.objects.create(
            user = user,
            specialization = specialization,
            bio = bio,
            appointment_duration = appointment_duration,
            timezone = timezone
        )

        return Response ({
            'message': f'Profile for {user.username} has been created'
        }, status=status.HTTP_201_CREATED)


class CreateAvailabilityView(APIView):
    permission_classes = [Provider]

    def post(self, request):
        # provider = request.data.get('provider')
        user = request.user
        weekday = request.data.get('weekday')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        # availaility for each day of week 0 duplicates
        if Availability.objects.get(weekday=weekday):
            return Response({
                'error': f'Availability for {weekday} already exists'
            }, status=status.HTTP_409_CONFLICT)
        Availability.objects.create(
            provider = ProviderProfile.objects.get(user=user),
            weekday = weekday,
            start_time = start_time,
            end_time = end_time
        )

        return Response ({
            'message': f'Availability slots for {user.username} on {weekday} has been created'
        }, status=status.HTTP_201_CREATED)

class CreateAppointmentView(APIView):
    permission_classes = [NotProvider]

    def post(self, request):
        user = request.user
        provider = request.data.get('provider')
        provider_user = request.data.get('provider_user')
        start_date_time = request.data.get('start_date_time')
        end_date_time = request.data.get('end_date_time')
        weekday = request.data.get('weekday')
        try:
            appointments = Appointment.objects.get(start_date_time = start_date_time, end_date_time = end_date_time)
        except Appointment.DoesNotExist:
            pass
        appointment_duration = ProviderProfile.objects.get(user=provider).appointment_duration
        start_dt = datetime.strptime(start_date_time, '%Y-%m-%d %H:%M:%S')
        end_dt = datetime.strptime(end_date_time, '%Y-%m-%d %H:%M:%S')
        ap_dt = timedelta(hours=appointment_duration.hour, minutes=appointment_duration.minute, seconds=appointment_duration.second)
        a_start = Availability.objects.get(provider=provider_user, weekday=weekday).start_time
        a_end = Availability.objects.get(provider=provider_user, weekday=weekday).end_time
        # t_start = timedelta(hours=a_start.hour, minutes=a_start.minute, seconds=a_start.second)
        # t_end = timedelta(hours=a_end.hour, minutes=a_end.minute, seconds=a_end.second)

        if((start_dt.time()) < (a_start)):
            return Response({
                'error': f'please make sure the duration is not less than{a_start}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if (start_dt.time())>a_start and end_dt>a_end:
            return Response({
                'error': f'Slots for {start_dt.date()} have been booked'
            })
        if((end_dt.time()) > a_end):
            return Response({
                'error': f'please make sure the end time is not after than {a_end}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if (end_dt - start_dt) > ap_dt:
            return Response({
                'error': f'please make sure the duration is not more than {appointment_duration}'
            }, status=status.HTTP_400_BAD_REQUEST)

        exists = Appointment.objects.filter(start_date_time=start_date_time,end_date_time=end_date_time,status='Confirmed')

        if exists.exists():
            return Response ({
                'message': 'Appointment already exists for another user'
            })
        

        exists = Appointment.objects.filter(start_date_time=start_date_time,end_date_time=end_date_time,status='Completed')

        if exists.exists():
            return Response ({
                'message': 'Appointment is completed, book for another day'
            })
        
        
        provider_u = ProviderProfile.objects.get(id=provider_user)
        
        exists = Appointment.objects.filter(start_date_time=start_date_time,end_date_time=end_date_time).exists()
        if not exists:
            Appointment.objects.create(
                user = user,
                provider = provider_u,
                start_date_time = start_date_time,
                end_date_time = end_date_time,
                status = 'Confirmed'
            )
            
                

        provider_u = ProviderProfile.objects.get(id=provider_user)
        f_time = (end_dt - start_dt)
        # datetime.isoformat()
        AvailableSlots.objects.create(
            provider = provider_u,
            user = user,
            start_time = start_dt,
            end_time = end_dt, 
            time = f'{f_time}',
            weekday = weekday,
            Taken = True
        )
        return Response ({
        'message': f'Appointment for {user.username} has been created start time: {start_date_time} end time: {end_date_time}'
    }, status=status.HTTP_201_CREATED)


    # request to create appointment
    # {
    #   "provider": 3,
    #   "provider_user": 1,
    #   "start_date_time": "2026-07-01 08:30:00",
    #   "end_date_time": "2026-07-01 09:00:00",
    #   "weekday": "Monday"
    # }
                

# class GenerateSlotView(generics.GenericAPIView):
#     serializer_class = SlotSerializer
#     permision_classes = [Provider]
#     def post(self, request):
#         weekday = request.data.get('weekday')
#         provider = ProviderProfile.objects.get(user=request.user)
#         appointment_duration = provider.appointment_duration
#         availability = Availability.objects.get(provider=provider, weekday=weekday)
#         if AvailableSlots.objects.filter(provider=provider, weekday=weekday):
#             return Response({
#                 'error': f'Slots for {request.user} on {weekday} have been generated'
#             })
#         available_slots = [availability.start_time]
#         serializer = SlotSerializer.get(available_slots, many=True)


#         for i in range(50):
#             c = availability.len() - 1
#             current_index = available_slots[c]
#             added_time = current_index + timedelta(hours=appointment_duration.hour, minutes=appointment_duration.minute, seconds=appointment_duration.second)
#             available_slots.append(added_time)
#             if available_slots[-1] > availability.end_time:
#                 available_slots.pop()
#                 return
#         return Response({
#             'message': f'slots for {weekday}: {serializer.data}'
#         }, status=status.HTTP_201_CREATED)
        
    

class EditProviderSlotAndAvailabilityView(APIView):
    permission_classes = [Provider]
    serializer_class = AppointmentSerializer

    def post(self, request):
        # availability = request.data.get('availability')
        weekday = request.data.get('weekday')
        # unavailable_slot = request.data.get('unavailable_slot')
        start_date_time = request.data.get('start_date_time')
        end_date_time = request.data.get('end_date_time')

        
        appointments = Appointment.objects.get(start_date_time = start_date_time, end_date_time = end_date_time)
        if appointments.status != 'Confirmed':
            return Response({
                'message': f'All appointments from {start_date_time} - {end_date_time} have been cancelled or completed'
            })
        if not appointments:
            return Response({
                'messsage': 'Appointment does not exist'
                }) 
        appointments.status = 'Cancelled'
        provider = Provider.objects.get(user=request.user)
        slot = AvailableSlots.objects.get(provider = provider, weekday = weekday)
        serializer = AppointmentSerializer(appointments)
        slot.user = provider
        # if the owner of a slot is the provider then that slot has been cancelled
        return Response({
        'message': serializer.data
        })
        

class CompletedAppointmentsView(generics.GenericAPIView):
    permission_classes = [Provider]
    serializer_class = AppointmentSerializer
    def post(self, request):
        
        provider_profile = ProviderProfile.objects.get(user=request.user)
        appointment_id = request.data.get("appointment_id")


        appointment = Appointment.objects.get(id=appointment_id, provider = provider_profile)
        appointment.status = 'Completed'
        appointment.save()
        serializer = AppointmentSerializer(appointment)


        return Response({
            'message': serializer.data   
        })

class ViewSlotsView(generics.GenericAPIView):
    serializer_class = SlotSerializer
    permission_classes = [Provider]

    def post(self,  request):
  
        provider_profile = ProviderProfile.objects.get(user=request.user)
        
        slot = AvailableSlots.objects.filter(provider=provider_profile)
        serializer = SlotSerializer(slot, many=True)

        return Response({
            'message': serializer.data
        })
        
      


# view availability for particular provider
# return error is provider is not avaialable for selected time 
# automaticaly generate availabity slots for users to see eg 9:30, 10:000 and if its been booked it be removed from the list

# ------------------ when booking appointments check the following ------------
# verify provider exists
# verify provider works that day
# verify slot exists
# verify slot hasn't already been booked

# also a user cannot book more than the appointment time for a provider
# cancel appointment
# reschedule
# provider can see their appointments for the day

# also users cannot book appointments ifor the past
# provider cannot book themselves
# if appointment is complete, cancel it
# providers manage avaiability