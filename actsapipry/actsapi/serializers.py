from rest_framework import serializers
from .models import Property, Activity


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ['id', 'title', 'address', 'description', 'status']
        # fields = '__all__'

    def create(self, validated_data):
        """
        Crea un objeto Property en la base de datos y regresa su instancia
        """
        return Property.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza el objeto Property y regresa su instancia
        """
        instance.title = validated_data.get('title', instance.title)
        instance.address = validated_data.get('address', instance.address)
        instance.description = validated_data.get('description', instance.description)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        instance.disabled_at = validated_data.get('disabled_at', instance.disabled_at)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class ActivitySerializer(serializers.ModelSerializer):
    property = serializers.StringRelatedField()
    
    class Meta:
        model = Activity
        fields = ['id', 'title', 'schedule', 'status', 'property']

    def create(self, validated_data):
        """
        Crea un objeto Activity en la base de datos y regresa su instancia
        """
        return Activity.objects.create(**validated_data)

    def update(self, instance, validatd_data):
        """
        Actualiza el objeto Activity y regresa su instancia
        """
        instance.property_id = validatd_data('property_id', instance.property_id)
        instance.schedule = validatd_data('schedule', instance.schedule)
        instance.title = validatd_data.get('title', instance.title)
        instance.created_at = validatd_data.get('created_at', instance.created_at)
        instance.updated_at = validatd_data.get('updated_at', instance.updated_at)
        instance.status = validatd_data.get('status', instance.status)
        instance.save()
        return instance        