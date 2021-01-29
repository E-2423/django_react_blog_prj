from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Profile
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password



class UserSerializers(serializers.ModelSerializer):
    model = User
    fields = (
        "username",
        "email"
    )
    
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password], style={'input_type':'password'}
    )
    password2 = serializers.CharField(
        write_only=True, required=True,  style={'input_type':'password'}
    )
    
    model = User
    fields = (
        "username",
        "email",
        "password",
        "password2",
    )