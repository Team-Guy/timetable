# Generated by Django 2.2.6 on 2019-12-06 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20191126_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='preference',
            name='fridayMax',
            field=models.IntegerField(default=12),
        ),
        migrations.AddField(
            model_name='preference',
            name='mondayMax',
            field=models.IntegerField(default=12),
        ),
        migrations.AddField(
            model_name='preference',
            name='thursdayMax',
            field=models.IntegerField(default=12),
        ),
        migrations.AddField(
            model_name='preference',
            name='tuesdayMax',
            field=models.IntegerField(default=12),
        ),
        migrations.AddField(
            model_name='preference',
            name='wednesdayMax',
            field=models.IntegerField(default=12),
        ),
    ]
