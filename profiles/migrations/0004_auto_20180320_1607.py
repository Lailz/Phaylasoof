# Generated by Django 2.0.3 on 2018-03-20 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20180320_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='clue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='profiles.Clue'),
        ),
    ]
