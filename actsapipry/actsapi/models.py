from django.db import models
from django.contrib.postgres.fields import JSONField
from datetime import datetime, date

ACTIVE_STATUS = 'active'
INACTIVE_STATUS = 'inactive'
CANCELLED_STATUS = 'canceled'
DONE_STATUS = 'done'

STATUS_CHOICES = [(ACTIVE_STATUS,ACTIVE_STATUS), (INACTIVE_STATUS,INACTIVE_STATUS)]
ACTIVITY_STATUS_CHOICES = [ACTIVE_STATUS, CANCELLED_STATUS, DONE_STATUS]


class Property(models.Model):
    # id = models.IntegerField(primary_key=True, verbose_name = "ID")
    title = models.CharField(max_length=255, blank=False, default='')
    address = models.TextField(blank=False, default='')
    description = models.TextField(blank=False, default='')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    disabled_at = models.DateTimeField(null=True)
    status = models.CharField(choices=STATUS_CHOICES, default='active', max_length=35)

    class Meta:
        ordering = ('created_at',)

    def __str__(self) -> str:
        return self.title


class Activity(models.Model):
    # id = models.IntegerField(primary_key=True, verbose_name = "ID")
    property1 = models.ForeignKey(Property, name="property", related_name='activities', on_delete=models.CASCADE)
    schedule = models.DateTimeField(auto_now_add=False, auto_now=False)
    title = models.TextField(blank=False, default='')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    status = models.CharField(max_length=35, blank=True, default='active')
    
    def _get_condition(self): 
        ahora = datetime.now()
        schedule = self.schedule
        hoy = date(ahora.year, ahora.month, ahora.day)
        scheduleday = date(schedule.year, schedule.month, schedule.day)
        condition = "Error"
        if self.status == DONE_STATUS:
            condition = "Finalizada"
        elif self.status == CANCELLED_STATUS:
            condition = "Cancelada"
        if self.status == ACTIVE_STATUS:
            if scheduleday >= hoy:
                condition = "Pendiente a realizar"
            else:
                condition = "Atrasada"
        return condition
   
    condition = property(_get_condition)

    class Meta:
        # unique_together = ['property', 'schedule']
        ordering = ('property','schedule',)
        
    def __str__(self):
        act = self.__dict__
        return act["schedule"].strftime("%d/%m/%Y %H:%M") + " -> " + act["title"]


class Survey(models.Model):
    # id = models.IntegerField(primary_key=True)
    activity = models.ForeignKey(Activity, related_name='survey', on_delete=models.CASCADE)
    answers = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        if self.id:
            return self.activity.__str__ + self.answers
        return ''