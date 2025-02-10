from rest_framework import serializers

class PatientSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    age = serializers.IntegerField()
    gender = serializers.CharField(max_length=10)
    address = serializers.CharField(max_length=500)
    contact = serializers.CharField(max_length=20)
    medical_history = serializers.CharField()
