# Generated by Django 4.0.4 on 2022-04-21 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments_rackets_app', '0007_categoryrating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='overallracketrating',
            name='points',
            field=models.FloatField(default=0),
        ),
    ]
