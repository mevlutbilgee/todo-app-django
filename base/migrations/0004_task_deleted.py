# Generated by Django 4.0.1 on 2023-08-27 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_task_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]