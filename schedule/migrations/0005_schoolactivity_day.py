# Generated by Django 2.2.6 on 2019-11-03 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_remove_schoolactivity_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolactivity',
            name='day',
            field=models.CharField(default='azi', max_length=30),
            preserve_default=False,
        ),
    ]