# Generated by Django 2.0.4 on 2018-05-11 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_auto_20180511_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedpage',
            name='followed_categories',
            field=models.ManyToManyField(to='api.Category'),
        ),
    ]
