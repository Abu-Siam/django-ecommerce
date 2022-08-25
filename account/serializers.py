import password as password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from django.utils.encoding import smart_str, force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from account.models import MyUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('phone','name','address','password')
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, attrs):
        return attrs

    def create(self, validate_data):
        return MyUser.objects.create_user(**validate_data)


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('phone','name','address','password')
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, attrs):
        return attrs

    def create(self, validate_data):
        return MyUser.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
    phone = serializers.IntegerField()
    class Meta:
        model = MyUser
        fields = ('phone','password')
        # extra_kwargs = {'password':{'write_only':True}}

    # def validate(self, attrs):
    #     return attrs
    #
    # def create(self, validate_data):
    #     return MyUser.objects.create_user(**validate_data)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('phone','name','address','password')

class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255,style ={'input_type':'password'},write_only= True)
    class Meta:
        model = MyUser
        fields = ('password',)

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            uid = self.context.get('uid')
            token = self.context.get('token')

            id = smart_str(urlsafe_base64_decode(uid))
            user = MyUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError('Token is invalid or expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError('Token is invalid or expired')

class UserPasswordResetEnterPhoneSerializer(serializers.ModelSerializer):
    phone = serializers.IntegerField()
    class Meta:
        model = MyUser
        fields = ('phone',)

    def validate(self, attrs):
        phone = attrs.get('phone')
        if MyUser.objects.filter(phone = phone).exists():
            user = MyUser.objects.get(phone=phone)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('encoded id', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('password reset token',token)
            link = " http://127.0.0.1:8000/api/user/change-password/" + uid + "/"+token +"/"
            print('link',link)
            return attrs
        else:
            raise ValidationError("Invalid user phone number")


class EditUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('phone','name','address','password')
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, attrs):
        phone = attrs.get('phone')
        if MyUser.objects.filter(phone = phone).exists():
            raise ValidationError("This phone number already is in use")

        else:
            pass
        return attrs

    def update(self, instance, validated_data):
        instance.phone = validated_data.get('phone', instance.phone)
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance