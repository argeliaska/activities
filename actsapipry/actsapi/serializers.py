from rest_framework import serializers
from .models import CANCELED_STATUS, Property, Activity, Survey


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
   
    class Meta:
        model = Activity
        fields = '__all__'

    def create(self, validated_data):
        """
        Crea un objeto Activity en la base de datos y regresa su instancia
        """
        return Activity.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza el objeto Activity y regresa su instancia
        """
        instance.property_id = validated_data('property_id', instance.property_id)
        instance.schedule = validated_data('schedule', instance.schedule)
        instance.title = validated_data.get('title', instance.title)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class PropertyInActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        exclude = ('description','status','created_at','updated_at','disabled_at')


class ActivityListSerializer(serializers.ModelSerializer):
    property = PropertyInActivitySerializer(read_only=True)
    survey = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Activity
        fields = ['id', 'schedule', 'title', 'created_at', 'status', 'condition', 'property', 'survey']

    
class CancelActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('status',)

    def update(self, instance, validated_data):
        """
        Actualiza el atributo 'status' del objeto Activity y regresa su instancia
        """
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class RescheduleActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('schedule',)

    def update(self, instance, validated_data):
        """
        Actualiza el atributo 'schedule' del objeto Activity y regresa su instancia
        """
        instance.status = validated_data.get('schedule', instance.schedule)
        instance.save()
        return instance