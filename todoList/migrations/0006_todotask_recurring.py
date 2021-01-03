# Generated by Django 3.1.4 on 2021-01-03 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoList', '0005_auto_20210102_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='todotask',
            name='recurring',
            field=models.CharField(choices=[('OC', 'Once'), ('DY', 'Daily'), ('WK', 'Weekly'), ('MN', 'Monthly'), ('YR', 'Yearly')], default='OC', max_length=2),
        ),
    ]
