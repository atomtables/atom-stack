# Generated by Django 4.2.2 on 2023-06-29 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountman', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_visit',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
