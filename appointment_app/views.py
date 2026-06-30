from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from rest_framework import status, response, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.views import Provider
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

        Availability.objects.create(
            provider = ProviderProfile.objects.get(user=user),
            weekday = weekday,
            start_time = start_time,
            end_time = end_time
        )

        return Response ({
            'message': f'Availability slots for {user.username} has been created'
        }, status=status.HTTP_201_CREATED)

class CreateAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user = request.data.get('user')
        provider = request.data.get('provider')
        start_date_time = request.data.get('start_date_time')
        end_date_time = request.data.get('end_date_time')

        appointments = Appointment.objects.get(start_date_time = start_date_time, end_date_time = end_date_time)
        appointment_duration = ProviderProfile.objects.get(provider=provider).appointment_duration
        start_dt = datetime.strptime(start_date_time, '%Y-%m-%d %H:%M:%S')
        end_dt = datetime.strptime(end_date_time, '%Y-%m-%d %H:%M:%S')
        ap_dt = timedelta(hours=appointment_duration.hour, minutes=appointment_duration.minute, seconds=appointment_duration.second)
        if (start_dt - end_dt) > ap_dt:
            return Response({
                'error': f'please make sure the duration is not more than {appointment_duration}'
            }, status=status.HTTP_400_BAD_REQUEST)
        if appointments.status == 'Confirmed':
            return Response ({
                'message': 'Appointment already exists for another user'
            })
        if appointments.status == 'Completed':
            return Response ({
                'message': 'Appointment is completed, book for another day'
            })
        
        if appointments.DoesNotExist or appointments.status == 'Cancelled':
            Appointment.objects.create(
                user = user,
                provider = provider,
                start_date_time = start_date_time,
                end_date_time = end_date_time
            )

        appointments.status = 'Confirmed'
        slot = AvailableSlots.objects.get(user=None, Taken=False)
        if slot:
            slot.user = request.user
            slot.save()

            return Response ({
                'message': f'Appointment for {user.username} has been created start time: {start_date_time} end time: {end_date_time}'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': f'Slots for {start_date_time.date()} have been booked'
        })

class GenerateSlotView(generics.GenericAPIView):
    serializer_class = SlotSerializer
    permision_classes = [Provider]
    def create(self, request):
        weekday = request.data.get('weekday')
        provider = Provider.objects.get(user=request.user)
        appointment_duration = provider.appointment_duration
        availability = Availability.objects.get(provider=provider, weekday=weekday)
        if AvailableSlots.objects.filter(provider=provider, weekday=weekday):
            return Response({
                'error': f'Slots for {provider} on {weekday} have been generated'
            })
        available_slots = [availability.start_time]
        serializer = SlotSerializer.get(available_slots, many=True)


        for i in range(50):
            c = availability.len() - 1
            current_index = available_slots[c]
            added_time = current_index + timedelta(hours=appointment_duration.hour, minutes=appointment_duration.minute, seconds=appointment_duration.second)
            available_slots.append(added_time)
            if available_slots[-1] > availability.end_time:
                available_slots.pop()
                return
        return Response({
            'message': f'slots for {weekday}: {serializer.data}'
        }, status=status.HTTP_201_CREATED)
        
    

class EditProviderSlotAndAvailabilityView(APIView):
    permission_classes = [Provider]
    def post(self, request):
        availability = request.data.get('availability')
        weekday = request.data.get('weekday')
        unavailable_slot = request.data.get('unavailable_slot')
        start_date_time = request.data.get('start_date_time')
        end_date_time = request.data.get('end_date_time')

        
        appointments = Appointment.objects.get(start_date_time = start_date_time, end_date_time = end_date_time)
        appointments.status = 'Cancelled'
        provider = Provider.objects.get(user=request.user)
        slot = AvailableSlots.objects.get(provider = provider, slot = unavailable_slot, weekday = weekday)
        slot.Taken = True

class CompletedAppointmentsView(APIView):
    permission_classes = [Provider]
    def post(self, request):
        appointment_id = request.data.get('id')
        appointment = Appointment.objects.get(id = appointment_id)
        appointment.status = 'Completed'
        appointment.save()

class ViewSlotsView(generics.GenericAPIView):
    serializer_class = SlotSerializer
    permission_classes = [IsAuthenticated]

    def post(self,  request):
        provider = request.data.get('provider')
        slot_id = request.data.get('slot_id')

        if request.user == provider:
            slot = AvailableSlots.objects.get(id=slot_id, provider=provider)
            serializer = SlotSerializer.get(slot, many=True)

            return Response({
                'message': serializer.data
            })
        
        return Response({
            'error': 'You are not the provider for this slot'
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