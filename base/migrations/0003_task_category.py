# Generated by Django 4.0.1 on 2023-08-24 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20210322_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='category',
            field=models.CharField(choices=[('İş', 'İş'), ('Gezi', 'Gezi'), ('Kişisel', 'Kişisel')], max_length=10, null=True),
        ),
    ]
