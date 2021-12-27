from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ACTIVE_STATUS, INACTIVE_STATUS, Property, Activity
from .serializers import PropertySerializer, ActivitySerializer, ActivityListSerializer
from django.http import Http404
from datetime import datetime, date, timedelta

class PropertyList(APIView):
    """
    Regresa el listado de todas las propiedades o crea una propiedad nueva
    """
    def get(self, request, format=None):
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyDetail(APIView):
    """
    Obtiene, actualiza o elimina una propiedad.
    """
    def get_object(self, pk):
        try:
            property = Property.objects.get(pk=pk)
            return property
        except Property.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        property = self.get_object(pk)
        serializer = PropertySerializer(property)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        property = self.get_object(pk)
        serializer = PropertySerializer(property, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request, pk, format=None):
        property = self.get_object(pk)
        property.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActivityList(APIView):
    """
    Regresa el listado de actividades agendadas
    """
    def get(self, request, format=None):

        hoy = datetime.now()
        dhoy = date(hoy.year, hoy.month, hoy.day)

        dia_desde = dhoy + timedelta(days=-4)
        dia_hasta = dhoy + timedelta(days=16)

        activities = Activity.objects.all().filter(schedule__date__gt=dia_desde, schedule__date__lte=dia_hasta)
        serializers = ActivityListSerializer(activities, many=True, context={'request': request})
        return Response(serializers.data)

    def post(self, request, format=None):
        actividad = request.data

        prop_id = actividad["property"]
        prop = Property.objects.get(id=prop_id)
        fecha = actividad["schedule"]

        if prop:
            if prop.status == INACTIVE_STATUS:
                return Response({"detail":"Propiedad inactiva"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    agendada = Activity.objects.get(property=prop_id, schedule=fecha)
                    if agendada:
                        return Response({"detail":"La propiedad tiene una actividad agendada para esa fecha y hora"}, status=status.HTTP_400_BAD_REQUEST)
                except Activity.DoesNotExist:
                    pass
        
        serializers = ActivitySerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivityDetail(APIView):
    """
    Obtiene, actualiza o elimina una actividad.
    """
    def get_object(self, pk):
        try:
            print("get_object activity entra", pk)
            activity = Activity.objects.get(pk=pk)
            print("get_object activity", activity)
            return activity
        except Activity.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        activity = self.get_object(pk)
        serializer = ActivitySerializer(activity)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        print("pk",pk)
        activity = self.get_object(pk)
        print("activity",activity)
        serializer = ActivitySerializer(activity, data=request.data)
        print("Serializer",serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        activity = self.get_object(pk)
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)