from rest_framework import serializers
from .models import User


class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','password','role','is_verified')

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user