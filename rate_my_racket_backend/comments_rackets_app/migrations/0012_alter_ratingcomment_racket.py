# Generated by Django 4.0.4 on 2022-04-24 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments_rackets_app', '0011_topracketcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratingcomment',
            name='racket',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rating_comment', to='comments_rackets_app.racket'),
        ),
    ]
