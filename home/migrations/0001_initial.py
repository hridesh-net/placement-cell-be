# Generated by Django 5.0.6 on 2024-06-12 09:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('10th', '10th'), ('12th', '12th'), ('Bachelors', 'Bachelors'), ('Masters', 'Masters'), ('PhD', 'PhD')], max_length=20)),
                ('marks_or_cgpa', models.FloatField()),
                ('year_of_passing', models.DateField()),
                ('board_or_university', models.CharField(max_length=255)),
                ('degree', models.CharField(max_length=255)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='educations', to='accounts.profile')),
            ],
        ),
    ]
