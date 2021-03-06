# Generated by Django 2.2.6 on 2019-11-15 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('start_time', models.TimeField()),
                ('day', models.CharField(max_length=15)),
                ('duration', models.IntegerField(default=2)),
                ('frequency', models.CharField(max_length=5)),
                ('priority', models.CharField(max_length=30)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SchoolActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('professor', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('group', models.CharField(max_length=10)),
                ('start_time', models.TimeField()),
                ('duration', models.IntegerField(default=2)),
                ('frequency', models.CharField(max_length=5)),
                ('priority', models.CharField(max_length=30)),
                ('type', models.CharField(max_length=30)),
                ('day', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('group', models.CharField(max_length=10)),
                ('photo_url', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserSchoolActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.SchoolActivity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.User')),
            ],
        ),
        migrations.CreateModel(
            name='UserExtraActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra_activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.ExtraActivity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.User')),
            ],
        ),
    ]
