# Generated by Django 2.0.4 on 2018-05-11 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_auto_20180511_2200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedpage',
            name='followed_users',
        ),
        migrations.AddField(
            model_name='feedpage',
            name='categories',
            field=models.ManyToManyField(to='api.Category'),
        ),
        migrations.AlterField(
            model_name='feedpage',
            name='followed_categories',
            field=models.ManyToManyField(to='api.FollowCategory'),
        ),
    ]
