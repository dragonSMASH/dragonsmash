# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dragon',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DragonEffect',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Effect',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Egg',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('username', models.CharField(unique=True, max_length=25)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,15}$', message="Phone number must be entered in the format: '+999999999'.                 Up to 15 digits allowed.")])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326)),
                ('time', models.DateTimeField()),
                ('money', models.IntegerField()),
                ('user', models.OneToOneField(to='api.User')),
            ],
        ),
        migrations.CreateModel(
            name='UserDragon',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('experience', models.IntegerField()),
                ('last_laid', models.DateTimeField()),
                ('dragon', models.ForeignKey(to='api.Dragon')),
                ('user', models.ForeignKey(to='api.User')),
            ],
        ),
        migrations.AddField(
            model_name='egg',
            name='dragon',
            field=models.ForeignKey(to='api.UserDragon'),
        ),
        migrations.AddField(
            model_name='egg',
            name='lays_dragon_type',
            field=models.ForeignKey(to='api.Dragon'),
        ),
        migrations.AddField(
            model_name='egg',
            name='user',
            field=models.ForeignKey(to='api.User'),
        ),
        migrations.AddField(
            model_name='dragoneffect',
            name='dragon',
            field=models.ForeignKey(to='api.UserDragon'),
        ),
        migrations.AddField(
            model_name='dragoneffect',
            name='effect',
            field=models.ForeignKey(to='api.Effect'),
        ),
        migrations.AddField(
            model_name='dragoneffect',
            name='user',
            field=models.ForeignKey(to='api.User'),
        ),
    ]
