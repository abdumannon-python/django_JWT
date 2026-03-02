from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from rest_framework import serializers
from .models import User
from rest_framework.exceptions import ValidationError
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'


class RegisterSerializers(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,required=True)
    conf_password=serializers.CharField(write_only=True,required=True)
    class Meta:
        model=User
        fields=('username', 'password','conf_password', 'email', 'first_name', 'last_name')



    def validate_username(self,username):
        if len(username)<6:
            raise ValidationError({'message':'Username kamida 7 belgidan iborat bolishi kerek'})
        elif not username.isalnum():
            raise ValidationError({'message':'username da ortiqcha belgi bolmasligi kerak '})
        elif username[0].isdigit():
            raise ValidationError({'message':'username raqam bilan boshlanmasin '})
        return username


    def create(self,validated_data):
        validated_data.pop('conf_password')
        user=User.objects.create_user(**validated_data)
        return user

class ProfilSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('username',  'email', 'first_name', 'last_name')

    def validate_username(self,username):
        user_query = User.objects.filter(username=username)

        if self.instance:
            user_query = user_query.exclude(pk=self.instance.pk)
        if user_query.exists():
            raise ValidationError({'message':'Bu username band'})
        if len(username)<6:
            raise ValidationError({'message':'Username kamida 7 belgidan iborat bolishi kerek'})
        elif not username.isalnum():
            raise ValidationError({'message':'username da ortiqcha belgi bolmasligi kerak '})
        elif username[0].isdigit():
            raise ValidationError({'message':'username raqam bilan boshlanmasin '})
        return username

    def validate_email(self,email):
        user_query = User.objects.filter(email=email)

        if self.instance:
            user_query = user_query.exclude(pk=self.instance.pk)

        if user_query.exists():
            raise ValidationError({'message': 'Bu email band'})
        return email
    def update(self, instance, validated_data):
        instance.username=validated_data.get('username',instance.username)
        instance.email=validated_data.get('email',instance.email)
        instance.first_name=validated_data.get('first_name',instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance



