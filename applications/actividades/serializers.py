from rest_framework import serializers
from .models import DailyTasks

class DailyTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTasks
        fields = '__all__'
        read_only_fields = ('created', 'modified')

    def validate(self, data):
        # Validar que endTime sea mayor que startTime
        if data.get('startTime') and data.get('endTime'):
            if data['startTime'] > data['endTime']:
                raise serializers.ValidationError("La hora de término debe ser posterior a la hora de inicio.")
        
        # Validar que overTime no sea negativo
        if data.get('overTime') and data['overTime'] < 0:
            raise serializers.ValidationError("Las horas extra no pueden ser negativas.")
            
        return data