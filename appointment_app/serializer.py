from rest_framework import serializers
from .models import *

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['time']
        read_only_fields = ['time']