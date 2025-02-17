# Generated by Django 3.1.4 on 2021-01-08 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todoList', '0007_todotask_created_next'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('list_name', models.CharField(max_length=255)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
            ],
        ),
        migrations.AddField(
            model_name='todotask',
            name='task_list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='todoList.tasklist'),
        ),
    ]
