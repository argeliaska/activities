from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ACTIVE_STATUS, CANCELED_STATUS, INACTIVE_STATUS, Property, Activity, Survey
from .serializers import PropertySerializer, ActivitySerializer, \
                         ActivityListSerializer, CancelActivitySerializer, \
                         RescheduleActivitySerializer, SurveySerializer
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

        if request.data:
            params = request.data

            status = params.get("status")
            fecha_ini = params.get("fecha_ini")
            fecha_fin = params.get("fecha_fin")

            if status:
                activities = Activity.objects.all().filter(status=status)
            elif fecha_ini and fecha_fin:
                activities = Activity.objects.all().filter(schedule__date__gt=fecha_ini, schedule__date__lt=fecha_fin)
            elif status and fecha_ini and fecha_fin:
                activities = Activity.objects.all().filter(status=status,schedule__date__gt=fecha_ini, schedule__date__lt=fecha_fin)
            serializers = ActivityListSerializer(activities, many=True, context={'request': request})
            return Response(serializers.data)

        else:
            hoy = datetime.now()
            dhoy = date(hoy.year, hoy.month, hoy.day)

            dia_desde = dhoy + timedelta(days=-4)
            dia_hasta = dhoy + timedelta(days=16)

            activities = Activity.objects.all().filter(schedule__date__gt=dia_desde, schedule__date__lt=dia_hasta)
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
                    agendada = Activity.objects.get(property=prop_id, schedule=fecha, status=ACTIVE_STATUS)
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
            activity = Activity.objects.get(pk=pk)
            return activity
        except Activity.DoesNotExist:
            raise Http404


    def get(self, request, pk):
        activity = self.get_object(pk)
        serializer = ActivitySerializer(activity)
        return Response(serializer.data)


    def put(self, request, pk, format=None):        
        activity = self.get_object(pk)
        serializer = ActivitySerializer(activity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        activity = self.get_object(pk)
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CancelActivity(APIView):
    """
    Actualiza el status de una actividad.
    """
    def get_object(self, pk):
        try:
            activity = Activity.objects.get(pk=pk)
            return activity
        except Activity.DoesNotExist:
            raise Http404

    def patch(self, request, pk):
        activity = self.get_object(pk=pk)
        data = {"status": CANCELED_STATUS}
        serializer = CancelActivitySerializer(activity, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RescheduleActivity(APIView):
    """
    Actualiza el status de una actividad.
    """
    def get_object(self, pk):
        try:
            activity = Activity.objects.get(pk=pk)
            return activity
        except Activity.DoesNotExist:
            raise Http404

    def patch(self, request, pk):
        activity = self.get_object(pk=pk)
        if activity.status == CANCELED_STATUS:
            return Response({"detail":"Actividad cancelada, imposible reagendar"}, status=status.HTTP_400_BAD_REQUEST)
        elif activity.status == ACTIVE_STATUS:
            serializer = RescheduleActivitySerializer(activity, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SurveyDetail(APIView):
    """
    Obtiene y muestra la encuesta de satisfacción
    """
    def get_object(self, pk):
        try:
            survey = Survey.objects.get(pk=pk)
            return survey
        except Survey.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        survey = self.get_object(pk)
        serializer = SurveySerializer(survey)
        return Response(serializer.data)