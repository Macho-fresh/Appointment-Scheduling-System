from django.urls import path
from .views import *

urlpatterns = [
    path('create-provider-profile/', CreateProviderProfileView.as_view()),
    path('create-provider-availability/', CreateAvailabilityView.as_view()),
    path('create-appointment/', CreateAppointmentView.as_view()),
    # path('generate-slots/', GenerateSlotView.as_view()),
    path('edit-slots-appointment/', EditProviderSlotAndAvailabilityView.as_view()),
    path('complete-appointment/', CompletedAppointmentsView.as_view()),
    path('view-slots/', ViewSlotsView.as_view())
]
