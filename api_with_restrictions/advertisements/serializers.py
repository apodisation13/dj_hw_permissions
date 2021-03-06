from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at', )

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        creator = self.context["request"].user.id
        # print(creator)
        total_open = Advertisement.objects.filter(creator__id=creator, status='OPEN').count()
        # print(total_open)
        if total_open > 10:
            raise ValidationError({'detail': 'Можно иметь не более десяти открытых объявлений'})
        return data

    @staticmethod
    def validate_title(value):
        """проверить поле title - например на 50 символов, ОБЯЗАТЕЛЬНО РЕТЁРН"""
        if len(value) > 50:
            raise ValidationError('Нельзя больше 50 символов')
        return value

    @staticmethod
    def validate_description(value):
        """проверить поле description - например что нельзя мат, ОБЯЗАТЕЛЬНО РЕТЁРН"""
        if 'ХРЕН' in value:
            raise ValidationError('Нельзя мат')
        return value
