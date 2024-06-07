from rest_framework import serializers

from .models import User, MyUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('user_email', 'user_password')




class UsersSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MyUser
        fields = ['email', 'password']

    def create(self, validated_data):
        user = MyUser.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user