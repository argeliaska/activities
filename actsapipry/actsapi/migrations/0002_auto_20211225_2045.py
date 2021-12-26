# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-12-26 02:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('actsapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule', models.DateTimeField()),
                ('title', models.TextField(default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(blank=True, default='active', max_length=35)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='actsapi.Property')),
            ],
            options={
                'ordering': ('schedule',),
            },
        ),
        migrations.AlterUniqueTogether(
            name='activity',
            unique_together=set([('property', 'schedule')]),
        ),
    ]
