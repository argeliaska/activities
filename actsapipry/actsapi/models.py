from django.db import models

STATUS = ['active', 'inactive']
STATUS_CHOICES = sorted((item, item) for item in STATUS)


class Property(models.Model):
    # id = models.IntegerField(primary_key=True, required=False)
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
    # id = models.IntegerField(primary_key=True, required=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    schedule = models.DateTimeField(auto_now_add=False, auto_now=False)
    title = models.TextField(blank=False, default='')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    status = models.CharField(max_length=35, blank=True, default='active')

    class Meta:
        # unique_together = ['property', 'schedule']
        ordering = ('property','schedule',)
        
    def __str__(self):
        act = self.__dict__
        return act["schedule"].strftime("%d/%m/%Y %H:%M") + " -> " + act["title"]