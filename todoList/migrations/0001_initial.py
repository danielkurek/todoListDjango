# Generated by Django 3.1.4 on 2020-12-05 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=50)),
                ('tag_color', models.CharField(max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='ToDoTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_title', models.CharField(max_length=255)),
                ('create_date', models.DateTimeField(verbose_name='date created')),
                ('due_date', models.DateTimeField()),
                ('task_description', models.TextField()),
                ('completed', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='TaskTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='todoList.tag')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='todoList.todotask')),
            ],
        ),
    ]
